#!/usr/bin/env python3
"""
Minimal ISO-BMFF / QuickTime tools for carrying the iPhone's own Dolby Vision RPUs into a re-encoded HLG file.

* read_samples(path): per-track sample table (decode order) with file offsets, sizes, decode/composition times.
* source_rpus(path): {display_index: RPU NAL bytes} for the video track, honouring the edit list (matches
  ffmpeg's displayed frame numbering).
* inject(path_in, path_out, rpu_for_frame, dovi): rewrite the file so every video sample ends with its RPU NAL
  (the HEVC/Dolby Vision rule: the RPU is the last NAL of the access unit), add a dvvC box to the hvc1 sample
  entry, and lay samples out interleaved with one sample per chunk. Pixel data is copied byte-for-byte.
"""
import struct

CONTAINERS = {b"moov", b"trak", b"mdia", b"minf", b"stbl", b"edts", b"dinf", b"udta"}


class Box:
    def __init__(self, typ, payload=b"", children=None):
        self.typ, self.payload, self.children = typ, payload, children

    def serialize(self):
        body = b"".join(c.serialize() for c in self.children) if self.children is not None else self.payload
        size = 8 + len(body)
        if size < 2 ** 32:
            return struct.pack(">I4s", size, self.typ) + body
        return struct.pack(">I4sQ", 1, self.typ, size + 8) + body

    def find(self, typ):
        for c in self.children or []:
            if c.typ == typ:
                return c
        return None


def parse_boxes(data, start=0, end=None):
    end = len(data) if end is None else end
    out, pos = [], start
    while pos + 8 <= end:
        size, typ = struct.unpack(">I4s", data[pos:pos + 8])
        hdr = 8
        if size == 1:
            size = struct.unpack(">Q", data[pos + 8:pos + 16])[0]; hdr = 16
        elif size == 0:
            size = end - pos
        body = data[pos + hdr:pos + size]
        if typ in CONTAINERS:
            out.append(Box(typ, children=parse_boxes(data, pos + hdr, pos + size)))
        else:
            out.append(Box(typ, payload=body))
        pos += size
    return out


def _full(b):
    return b.payload[0], b.payload[4:]


def track_tables(trak):
    mdia = trak.find(b"mdia"); minf = mdia.find(b"minf"); stbl = minf.find(b"stbl")
    hdlr = mdia.find(b"hdlr").payload[8:12]
    mdhd = mdia.find(b"mdhd").payload
    ver = mdhd[0]
    timescale = struct.unpack(">I", mdhd[12:16] if ver == 0 else mdhd[20:24])[0]

    def entries(typ, fmt, n_fields):
        b = stbl.find(typ)
        if b is None:
            return []
        _, p = _full(b)
        cnt = struct.unpack(">I", p[:4])[0]
        sz = struct.calcsize(fmt)
        return [struct.unpack(fmt, p[4 + i * sz:4 + (i + 1) * sz]) for i in range(cnt)]
    stsz = stbl.find(b"stsz"); _, p = _full(stsz)
    fixed, cnt = struct.unpack(">II", p[:8])
    sizes = [fixed] * cnt if fixed else list(struct.unpack(f">{cnt}I", p[8:8 + 4 * cnt]))
    stco = stbl.find(b"stco") or stbl.find(b"co64")
    _, p = _full(stco)
    n = struct.unpack(">I", p[:4])[0]
    chunk_off = list(struct.unpack(f">{n}{'I' if stco.typ == b'stco' else 'Q'}", p[4:4 + n * (4 if stco.typ == b'stco' else 8)]))
    stsc = entries(b"stsc", ">III", 3)
    stts = entries(b"stts", ">II", 2)
    ctts_b = stbl.find(b"ctts")
    ctts = []
    if ctts_b is not None:
        v, p = _full(ctts_b)
        c = struct.unpack(">I", p[:4])[0]
        ctts = [struct.unpack(">Ii" if v == 1 else ">II", p[4 + 8 * i:12 + 8 * i]) for i in range(c)]
    # sample -> offset
    offsets = []
    for ci, off in enumerate(chunk_off):
        chunk_no = ci + 1
        spc = None
        for first, per, _ in stsc:
            if first <= chunk_no:
                spc = per
        for _ in range(spc):
            offsets.append(off); off += sizes[len(offsets) - 1]
    dts, t = [], 0
    for c, d in stts:
        for _ in range(c):
            dts.append(t); t += d
    cto = []
    for c, o in ctts:
        cto += [o] * c
    if not cto:
        cto = [0] * len(dts)
    elst = None
    edts = trak.find(b"edts")
    if edts is not None and edts.find(b"elst") is not None:
        v, p = _full(edts.find(b"elst"))
        c = struct.unpack(">I", p[:4])[0]
        ents = [struct.unpack(">Iii" if v == 0 else ">Qqi", p[4 + i * (12 if v == 0 else 20):4 + (i + 1) * (12 if v == 0 else 20)]) for i in range(c)]
        elst = ents
    return dict(handler=hdlr, timescale=timescale, sizes=sizes, offsets=offsets[:len(sizes)], dts=dts, cto=cto,
                stbl=stbl, elst=elst, trak=trak)


def read_file(path):
    data = open(path, "rb").read()
    boxes = parse_boxes(data)
    moov = next(b for b in boxes if b.typ == b"moov")
    traks = [c for c in moov.children if c.typ == b"trak"]
    return data, boxes, moov, [track_tables(t) for t in traks]


def nals(sample, length_size=4):
    pos, out = 0, []
    while pos + length_size <= len(sample):
        n = int.from_bytes(sample[pos:pos + length_size], "big")
        out.append(sample[pos + length_size:pos + length_size + n]); pos += length_size + n
    return out


def source_rpus_ff(path):
    """{pts_seconds: RPU NAL bytes}, keyed by ffmpeg's own presentation timestamps (edit list applied exactly
    as ffmpeg's decoder/trim filter sees it). Packets are located by file position, so bytes are exact."""
    import json, subprocess
    pk = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                    "packet=pts_time,pos,size", "-of", "json", path],
                                   capture_output=True, text=True).stdout)["packets"]
    data = open(path, "rb").read()
    out = {}
    for p in pk:
        if p.get("pts_time") in (None, "N/A"):
            continue
        smp = data[int(p["pos"]):int(p["pos"]) + int(p["size"])]
        r = [n for n in nals(smp) if n and (n[0] >> 1) & 0x3F == 62]
        if r:
            out[float(p["pts_time"])] = r[-1]
    return out


def source_rpus(path):
    """(Superseded by source_rpus_ff.) List of RPU NAL bytes in composition order."""
    data, _, _, tabs = read_file(path)
    v = next(t for t in tabs if t["handler"] == b"vide")
    cts = [d + o for d, o in zip(v["dts"], v["cto"])]
    order = sorted(range(len(cts)), key=lambda i: cts[i])
    media_start = 0
    if v["elst"]:
        for seg_dur, mtime, rate in v["elst"]:
            if mtime >= 0:
                media_start = mtime; break
    disp = [i for i in order if cts[i] >= media_start]
    out = []
    for i in disp:
        s = data[v["offsets"][i]:v["offsets"][i] + v["sizes"][i]]
        r = [n for n in nals(s) if (n[0] >> 1) & 0x3F == 62]
        out.append(r[-1] if r else None)
    return out


def dvvc_box(profile=8, level=7, compat=4):
    b0 = 1; b1 = 0
    bits = (profile << 9) | (level << 3) | (1 << 2) | (0 << 1) | 1     # rpu=1, el=0, bl=1
    payload = bytes([b0, b1]) + struct.pack(">H", bits) + bytes([compat << 4]) + bytes(19)
    return Box(b"dvvC", payload=payload)


def _replace(parent, typ, new):
    for i, c in enumerate(parent.children):
        if c.typ == typ:
            parent.children[i] = new; return
    parent.children.append(new)


def inject(path_in, path_out, rpu_for_frame, dovi=(8, 7, 4), extra_boxes=(), hvcc_extra_nals=()):
    data, boxes, moov, tabs = read_file(path_in)
    samples = []                                                    # (time_sec, track_idx, sample_idx, bytes)
    for ti, t in enumerate(tabs):
        if t["handler"] == b"vide":
            cts = [d + o for d, o in zip(t["dts"], t["cto"])]
            rank = {i: r for r, i in enumerate(sorted(range(len(cts)), key=lambda i: cts[i]))}
        for si in range(len(t["sizes"])):
            s = data[t["offsets"][si]:t["offsets"][si] + t["sizes"][si]]
            if t["handler"] == b"vide":
                rpu = rpu_for_frame(rank[si])
                if rpu is not None:
                    s = s + len(rpu).to_bytes(4, "big") + rpu
            samples.append((t["dts"][si] / t["timescale"], ti, si, s))
    samples.sort(key=lambda x: (x[0], x[1]))
    # new sample tables (one sample per chunk), placeholder offsets
    per_track = {ti: [] for ti in range(len(tabs))}
    for _, ti, si, s in samples:
        per_track[ti].append((si, len(s)))
    for ti, t in enumerate(tabs):
        stbl = t["stbl"]
        sizes = [sz for _, sz in sorted(per_track[ti])]
        _replace(stbl, b"stsz", Box(b"stsz", payload=struct.pack(">I", 0) + struct.pack(">II", 0, len(sizes)) + struct.pack(f">{len(sizes)}I", *sizes)))
        _replace(stbl, b"stsc", Box(b"stsc", payload=struct.pack(">I", 0) + struct.pack(">I", 1) + struct.pack(">III", 1, 1, 1)))
        stbl.children = [c for c in stbl.children if c.typ not in (b"stco", b"co64")]
        stbl.children.append(Box(b"co64", payload=struct.pack(">I", 0) + struct.pack(">I", len(sizes)) + bytes(8 * len(sizes))))
        if t["handler"] == b"vide":
            stsd = stbl.find(b"stsd")
            p = stsd.payload
            entry_size = struct.unpack(">I", p[8:12])[0]
            entry = p[8:8 + entry_size]
            fmt = entry[4:8]
            # sample entry: 8 hdr + 78 visual sample entry fields, then child boxes
            kids = parse_boxes(entry, 8 + 78, entry_size)
            if hvcc_extra_nals:
                for k in kids:
                    if k.typ == b"hvcC":
                        k.payload = hvcc_add_nals(k.payload, hvcc_extra_nals)
            drop = {b"dvcC", b"dvvC"} | {b.typ for b in extra_boxes}
            kids = [k for k in kids if k.typ not in drop]
            kids.append(dvvc_box(*dovi))
            kids.extend(extra_boxes)
            body = entry[8:8 + 78] + b"".join(k.serialize() for k in kids)
            new_entry = struct.pack(">I4s", 8 + len(body), fmt) + body
            stsd.payload = p[:8] + new_entry + p[8 + entry_size:]
    ftyp = next(b for b in boxes if b.typ == b"ftyp")
    head = ftyp.serialize()
    moov_bytes = moov.serialize()
    mdat_hdr = 16                                                   # 64-bit mdat header
    base = len(head) + len(moov_bytes) + mdat_hdr
    # fill co64 offsets in sample order per track
    offs = {ti: {} for ti in range(len(tabs))}
    pos = base
    for _, ti, si, s in samples:
        offs[ti][si] = pos; pos += len(s)
    for ti, t in enumerate(tabs):
        co = t["stbl"].find(b"co64")
        o = [offs[ti][si] for si in sorted(offs[ti])]
        co.payload = struct.pack(">I", 0) + struct.pack(">I", len(o)) + struct.pack(f">{len(o)}Q", *o)
    moov_bytes2 = moov.serialize()
    assert len(moov_bytes2) == len(moov_bytes)
    with open(path_out, "wb") as f:
        f.write(head); f.write(moov_bytes2)
        total = mdat_hdr + sum(len(s) for *_, s in samples)
        f.write(struct.pack(">I4sQ", 1, b"mdat", total))
        for *_, s in samples:
            f.write(s)


def sample_entry_box(path, typ):
    """Copy a box (e.g. b'amve') from the source video sample entry, unchanged."""
    _, _, _, tabs = read_file(path)
    v = next(t for t in tabs if t["handler"] == b"vide")
    p = v["stbl"].find(b"stsd").payload
    es = struct.unpack(">I", p[8:12])[0]
    for k in parse_boxes(p[8:8 + es], 8 + 78, es):
        if k.typ == typ:
            return k
    return None


def hvcc_arrays(h):
    pos = 22; n = h[pos]; pos += 1; arrs = []
    for _ in range(n):
        hdr = h[pos]; cnt = struct.unpack(">H", h[pos + 1:pos + 3])[0]; pos += 3; nl = []
        for _ in range(cnt):
            l = struct.unpack(">H", h[pos:pos + 2])[0]; nl.append(h[pos + 2:pos + 2 + l]); pos += 2 + l
        arrs.append([hdr, nl])
    return h[:22], arrs


def hvcc_add_nals(h, nals_to_add):
    """Append NAL units (e.g. an Ambient Viewing Environment prefix-SEI) to the matching hvcC arrays."""
    head, arrs = hvcc_arrays(h)
    for nal in nals_to_add:
        t = (nal[0] >> 1) & 0x3F
        a = next((a for a in arrs if a[0] & 0x3F == t), None)
        if a is None:
            arrs.append([t, [nal]])
        elif nal not in a[1]:
            a[1].append(nal)
    out = bytearray(head) + bytes([len(arrs)])
    for hdr, nl in arrs:
        out += bytes([hdr]) + struct.pack(">H", len(nl))
        for nal in nl:
            out += struct.pack(">H", len(nal)) + nal
    return bytes(out)


def source_hvcc_sei(path, payload_type=0x94):
    _, _, _, tabs = read_file(path)
    v = next(t for t in tabs if t["handler"] == b"vide")
    p = v["stbl"].find(b"stsd").payload
    es = struct.unpack(">I", p[8:12])[0]
    h = next(k for k in parse_boxes(p[8:8 + es], 8 + 78, es) if k.typ == b"hvcC").payload
    _, arrs = hvcc_arrays(h)
    return [n for hdr, nl in arrs for n in nl if (n[0] >> 1) & 0x3F == 39 and n[2] == payload_type]
