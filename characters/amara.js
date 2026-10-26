// Amara — personnage principal BabyDashNow, dessiné entièrement en SVG.
// Le visage est construit à partir de pièces (yeux, sourcils, bouche) pour que
// chaque expression soit un simple jeu de paramètres, facile à animer.
const C = require('./palette');

// Repère du portrait : viewBox 0 0 600 800, tête centrée vers (302, 250).
const EYES = { near: { x: 278, y: 242, s: 1 }, far: { x: 340, y: 240, s: 0.86 } };

const EXPRESSIONS = {
  calme:     { eyes: ['open', 'open'], look: [2, 0], brows: [0, 0, 0], mouth: 'smile' },
  tendre:    { eyes: ['soft', 'soft'], look: [0, 4], brows: [-3, 2, 0], mouth: 'soft' },
  concentree:{ eyes: ['half', 'half'], look: [4, 1], brows: [4, -2, 0], mouth: 'press' },
  oups:      { eyes: ['wide', 'wide'], look: [0, 0], brows: [-9, -7, 0], mouth: 'o' },
  clin:      { eyes: ['open', 'wink'], look: [1, 0], brows: [0, 0, 4], mouth: 'smirk' },
  fatiguee:  { eyes: ['tired', 'tired'], look: [0, 2], brows: [-2, 3, 0], mouth: 'soft' },
  soulagee:  { eyes: ['closed', 'closed'], look: [0, 0], brows: [-4, 2, 0], mouth: 'smile' },
  fiere:     { eyes: ['proud', 'proud'], look: [2, -1], brows: [-2, -3, 0], mouth: 'grin' },
};

function almond(x, y, s, open) {
  const w = 22 * s, h = 12 * open;
  return `M ${x - w} ${y} C ${x - w * 0.55} ${y - h * 1.15} ${x + w * 0.5} ${y - h * 1.2} ${x + w} ${y - h * 0.15}` +
    ` C ${x + w * 0.5} ${y + h * 0.75} ${x - w * 0.5} ${y + h * 0.8} ${x - w} ${y} Z`;
}

function eye(id, { x, y, s }, type, [lx, ly]) {
  const lidLine = (open) => {
    const w = 22 * s, h = 12 * open;
    return `<path d="M ${x - w - 2} ${y + 1} C ${x - w * 0.55} ${y - h * 1.15} ${x + w * 0.5} ${y - h * 1.2} ${x + w + 3} ${y - h * 0.2} l 5 -4"` +
      ` fill="none" stroke="${C.hair}" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>`;
  };
  if (type === 'closed' || type === 'wink') {
    // Paupière fermée : un arc doux (soulagement) ou un arc plus marqué (clin d'œil).
    const w = 21 * s, dip = type === 'wink' ? -7 : 5;
    return `<path d="M ${x - w} ${y} Q ${x} ${y + dip} ${x + w} ${y - 1}" fill="none" stroke="${C.hair}"` +
      ` stroke-width="3.6" stroke-linecap="round"/><path d="M ${x + w} ${y - 1} l 5 -3" stroke="${C.hair}" stroke-width="3" stroke-linecap="round"/>`;
  }
  const open = { open: 1, soft: 0.72, half: 0.6, wide: 1.35, tired: 0.55, proud: 0.75 }[type];
  const irisR = type === 'wide' ? 8.5 : 10;
  const d = almond(x, y, s, open);
  let out = `<clipPath id="${id}"><path d="${d}"/></clipPath>` +
    `<path d="${d}" fill="${C.eyeWhite}"/>` +
    `<g clip-path="url(#${id})">` +
    `<circle cx="${x + lx}" cy="${y + ly}" r="${irisR}" fill="${C.iris}"/>` +
    `<circle cx="${x + lx}" cy="${y + ly}" r="${irisR * 0.48}" fill="#120C09"/>` +
    `<circle cx="${x + lx + 3}" cy="${y + ly - 3}" r="2.4" fill="#fff"/>` +
    `</g>` + lidLine(open);
  if (type === 'tired') {
    out += `<path d="M ${x - 14 * s} ${y + 9} Q ${x} ${y + 14} ${x + 14 * s} ${y + 8}" fill="none" stroke="${C.skinShade}" stroke-width="2" stroke-linecap="round" opacity="0.7"/>`;
  }
  return out;
}

function brow({ x, y, s }, [inner, outer, raise], side) {
  const w = 21 * s, by = y - 24;
  // side = 'near' (gauche, intérieur à droite) ou 'far' (droite, intérieur à gauche)
  const ix = side === 'near' ? x + w * 0.8 : x - w * 0.8;
  const ox = side === 'near' ? x - w : x + w;
  const r = side === 'far' ? raise : 0;
  return `<path d="M ${ix} ${by + inner - r} Q ${x} ${by - 7 - r} ${ox} ${by + 3 + outer - r}" fill="none"` +
    ` stroke="${C.hair}" stroke-width="${5.5 * s}" stroke-linecap="round"/>`;
}

function mouth(type) {
  const x = 318, y = 308;
  switch (type) {
    case 'smile':
      return `<path d="M ${x - 24} ${y - 6} Q ${x - 4} ${y - 4} ${x + 24} ${y - 9} Q ${x + 6} ${y + 18} ${x - 24} ${y - 6} Z" fill="${C.lip}"/>` +
        `<path d="M ${x - 24} ${y - 6} Q ${x} ${y + 6} ${x + 24} ${y - 9}" fill="none" stroke="${C.lipDark}" stroke-width="2.6" stroke-linecap="round"/>`;
    case 'soft':
      return `<path d="M ${x - 17} ${y - 2} Q ${x} ${y - 5} ${x + 17} ${y - 3} Q ${x + 2} ${y + 9} ${x - 17} ${y - 2} Z" fill="${C.lip}"/>` +
        `<path d="M ${x - 17} ${y - 2} Q ${x} ${y + 2} ${x + 17} ${y - 3}" fill="none" stroke="${C.lipDark}" stroke-width="2.2" stroke-linecap="round"/>`;
    case 'press':
      return `<path d="M ${x - 13} ${y} Q ${x} ${y - 3} ${x + 13} ${y + 1}" fill="none" stroke="${C.lipDark}" stroke-width="3.2" stroke-linecap="round"/>`;
    case 'o':
      return `<ellipse cx="${x}" cy="${y + 2}" rx="9" ry="11" fill="${C.lipDark}"/><ellipse cx="${x}" cy="${y + 2}" rx="9" ry="11" fill="none" stroke="${C.lip}" stroke-width="3"/>`;
    case 'smirk':
      return `<path d="M ${x - 18} ${y} Q ${x + 2} ${y + 2} ${x + 22} ${y - 9} Q ${x + 6} ${y + 12} ${x - 18} ${y} Z" fill="${C.lip}"/>` +
        `<path d="M ${x - 18} ${y} Q ${x + 4} ${y + 4} ${x + 22} ${y - 9}" fill="none" stroke="${C.lipDark}" stroke-width="2.4" stroke-linecap="round"/>`;
    case 'grin':
      return `<path d="M ${x - 24} ${y - 5} Q ${x} ${y - 7} ${x + 24} ${y - 8} Q ${x + 4} ${y + 20} ${x - 24} ${y - 5} Z" fill="${C.lipDark}"/>` +
        `<path d="M ${x - 20} ${y - 4} Q ${x} ${y - 5} ${x + 20} ${y - 6} Q ${x + 2} ${y + 3} ${x - 20} ${y - 4} Z" fill="#FBF6EE"/>` +
        `<path d="M ${x - 24} ${y - 5} Q ${x} ${y - 9} ${x + 24} ${y - 8}" fill="none" stroke="${C.lip}" stroke-width="3" stroke-linecap="round"/>`;
  }
}

// Petites boucles qui tombent des tempes.
function tendril(x, y, dir, n) {
  let d = `M ${x} ${y}`;
  for (let i = 0; i < n; i++) d += ` c ${-10 * dir} 8 ${10 * dir} 18 ${-1 * dir} 26 c ${-8 * dir} 6 ${-12 * dir} -5 ${-3 * dir} -8`;
  return `<path d="${d}" fill="none" stroke="${C.hair}" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>`;
}

// Chignon bouclé : des cercles serrés + des reflets en arcs.
function bun(cx, cy) {
  const curls = [];
  const rings = [[0, 1, 26], [30, 7, 22], [54, 12, 19]];
  for (const [r, n, size] of rings) {
    for (let i = 0; i < n; i++) {
      const a = (i / n) * Math.PI * 2 + r * 0.05;
      curls.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r * 0.82, size]);
    }
  }
  return curls.map(([x, y, s]) =>
    `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${s}" fill="${C.hair}"/>`).join('') +
    curls.map(([x, y, s]) =>
      `<path d="M ${(x - s * 0.5).toFixed(1)} ${(y + s * 0.1).toFixed(1)} a ${s * 0.5} ${s * 0.5} 0 0 1 ${s * 0.7} ${-s * 0.4}"` +
      ` fill="none" stroke="${C.hairLight}" stroke-width="2.2" stroke-linecap="round"/>`).join('');
}

function head(expr = 'calme', id = 'a') {
  const e = typeof expr === 'string' ? EXPRESSIONS[expr] : expr;
  const face = 'M 238 196 C 232 252 246 300 288 330 C 304 341 322 341 338 329 C 364 302 374 262 370 212 C 364 170 334 150 302 150 C 270 150 242 168 238 196 Z';
  return `<g class="amara-head">
    ${bun(304, 82)}
    <path d="M 290 330 L 284 398 L 336 398 L 330 326 Z" fill="${C.skin}"/>
    <path d="M 290 330 C 304 346 322 346 332 334 L 333 356 C 318 362 302 360 289 350 Z" fill="${C.skinShade}" opacity="0.45"/>
    <path d="${face}" fill="${C.skin}"/>
    <path d="M 340 160 C 372 180 378 250 360 296 C 350 316 340 326 330 332 C 352 300 362 250 354 200 C 350 180 346 170 340 160 Z" fill="${C.skinShade}" opacity="0.25"/>
    <ellipse cx="240" cy="246" rx="11" ry="19" fill="${C.skin}"/>
    <path d="M 240 236 C 246 242 246 254 241 258" fill="none" stroke="${C.skinShade}" stroke-width="2.4" stroke-linecap="round"/>
    <circle cx="238" cy="266" r="4.5" fill="${C.gold}"/>
    <path d="M 234 226 C 226 158 262 124 304 124 C 350 124 380 160 372 216 C 364 194 348 182 330 178 C 312 174 292 174 272 180 C 254 188 242 202 234 226 Z" fill="${C.hair}"/>
    <path d="M 262 150 C 280 140 310 138 332 146 M 252 166 C 268 156 290 152 306 154" fill="none" stroke="${C.hairLight}" stroke-width="2.2" stroke-linecap="round"/>
    <path d="M 254 124 C 262 108 290 112 304 112 C 318 110 348 106 356 122 C 362 136 346 144 304 144 C 266 146 248 138 254 124 Z" fill="${C.sage}"/>
    <path d="M 270 116 C 274 126 274 134 270 142 M 300 112 C 304 122 304 134 300 144 M 330 112 C 334 122 334 132 332 142" fill="none" stroke="${C.sageDark}" stroke-width="2.6" stroke-linecap="round"/>
    <path d="M 256 130 C 280 140 330 140 354 128" fill="none" stroke="${C.sageDark}" stroke-width="2" opacity="0.6"/>
    ${tendril(238, 214, 1, 4)}
    ${tendril(368, 210, -1, 3)}
    <ellipse cx="276" cy="276" rx="17" ry="10" fill="${C.blush}" opacity="0.22"/>
    <ellipse cx="350" cy="274" rx="12" ry="9" fill="${C.blush}" opacity="0.2"/>
    <path d="M 316 250 C 318 266 326 280 324 288 C 318 293 309 292 304 287" fill="none" stroke="${C.skinShade}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    <g class="amara-eyes">
      ${eye(id + '-en', EYES.near, e.eyes[0], e.look)}
      ${eye(id + '-ef', EYES.far, e.eyes[1], e.look)}
    </g>
    ${brow(EYES.near, e.brows, 'near')}
    ${brow(EYES.far, e.brows, 'far')}
    ${mouth(e.mouth)}
  </g>`;
}

// Corps du portrait : cardigan ouvert, t-shirt col V, mains dans les poches.
function body() {
  return `<g class="amara-body">
    <path d="M 258 397 L 362 397 L 310 480 Z" fill="${C.skin}"/>
    <path d="M 214 404 L 260 398 L 310 476 L 360 398 L 404 404 L 414 668 L 206 668 Z" fill="${C.tee}"/>
    <path d="M 260 398 L 310 476 L 360 398" fill="none" stroke="${C.teeShade}" stroke-width="5" stroke-linejoin="round"/>
    <path d="M 214 404 C 236 520 236 600 230 668 L 206 668 Z" fill="${C.teeShade}"/>
    <path d="M 206 660 L 414 660 L 424 800 L 196 800 Z" fill="${C.trousers}"/>
    <path d="M 206 660 L 414 660 L 415 684 L 205 684 Z" fill="${C.trousersShade}"/>
    <path d="M 312 684 L 314 800" stroke="${C.trousersShade}" stroke-width="3"/>
    <path d="M 262 398 C 214 396 176 410 162 446 C 146 540 150 680 168 800 L 252 800 C 244 660 236 520 262 398 Z" fill="${C.taupe}"/>
    <path d="M 358 398 C 406 396 444 410 458 446 C 474 540 470 680 452 800 L 368 800 C 376 660 384 520 358 398 Z" fill="${C.taupe}"/>
    <path d="M 262 398 C 240 520 244 660 252 800 L 264 800 C 256 660 252 520 270 400 Z" fill="${C.taupeShade}"/>
    <path d="M 358 398 C 380 520 376 660 368 800 L 356 800 C 364 660 368 520 350 400 Z" fill="${C.taupeShade}"/>
    <path d="M 168 446 C 142 520 140 610 158 700 L 210 708 C 214 620 214 530 206 470 C 196 452 182 444 168 446 Z" fill="${C.taupeShade}"/>
    <path d="M 452 446 C 478 520 480 610 462 700 L 410 708 C 406 620 406 530 414 470 C 424 452 438 444 452 446 Z" fill="${C.taupeShade}"/>
    <path d="M 158 690 L 210 698 L 208 722 L 156 714 Z" fill="${C.taupeDark}"/>
    <path d="M 462 690 L 410 698 L 412 722 L 464 714 Z" fill="${C.taupeDark}"/>
    <path d="M 166 694 L 165 716 M 176 696 L 175 718 M 186 697 L 185 719 M 196 698 L 195 720 M 454 694 L 455 716 M 444 696 L 445 718 M 434 697 L 435 719 M 424 698 L 425 720" stroke="${C.taupe}" stroke-width="2"/>
    <path d="M 186 720 C 184 744 196 760 212 758 C 224 756 226 740 222 724 Z" fill="${C.skin}"/>
    <path d="M 434 720 C 436 744 424 760 408 758 C 396 756 394 740 398 724 Z" fill="${C.skin}"/>
    <path d="M 208 730 C 214 738 214 748 210 752" fill="none" stroke="${C.skinShade}" stroke-width="2" stroke-linecap="round"/>
    <path d="M 412 730 C 406 738 406 748 410 752" fill="none" stroke="${C.skinShade}" stroke-width="2" stroke-linecap="round"/>
    <path d="M 200 708 C 196 640 200 520 214 420 M 420 708 C 424 640 420 520 406 420" fill="none" stroke="${C.taupeDark}" stroke-width="2" opacity="0.35"/>
  </g>`;
}

function portrait(expr = 'calme', id = 'a') {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 800">${body()}<g transform="translate(-30 -8) scale(1.1)">${head(expr, id)}</g></svg>`;
}

module.exports = { head, body, portrait, EXPRESSIONS };
