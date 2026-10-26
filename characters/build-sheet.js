// Génère la planche personnage (HTML) : Amara en pied, ses 8 expressions, Bibou et ses 4 réactions.
// Usage : node characters/build-sheet.js > characters/out/planche.html
const amara = require('./amara');
const bibou = require('./bibou');

const LABELS = {
  calme: 'Calme', tendre: 'Tendre', concentree: 'Concentrée', oups: 'Oups',
  clin: "Clin d'œil", fatiguee: 'Fatiguée', soulagee: 'Soulagée', fiere: 'Fière',
  fascine: 'Fasciné', boude: 'Boude', content: 'Content', dort: 'Dort',
};

// Recadrage sur le visage d'Amara (tête agrandie dans le portrait).
const face = (expr) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="185 20 260 370">` +
  `<g transform="translate(-30 -8) scale(1.1)">${amara.head(expr, 'x-' + expr)}</g></svg>`;

const tile = (svg, label) => `<figure>${svg}<figcaption>${label}</figcaption></figure>`;

const html = `<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Planche Amara et Bibou</title>
<style>
  body { margin: 0; background: #E9E2D2; font-family: Georgia, serif; color: #2A2624; }
  main { width: 1200px; padding: 48px 56px; box-sizing: border-box; }
  h1 { font-weight: 400; font-size: 44px; margin: 0; }
  h1 em { color: #367620; }
  .kicker { font: 600 13px/1 system-ui, sans-serif; letter-spacing: .18em; color: #367620; text-transform: uppercase; }
  h2 { font-weight: 400; font-size: 26px; margin: 40px 0 16px; }
  .top { display: grid; grid-template-columns: 420px 1fr; gap: 40px; align-items: start; margin-top: 24px; }
  .hero svg { width: 420px; height: auto; background: #EFE9DC; border-radius: 210px 210px 16px 16px; }
  .grid { display: grid; gap: 16px; }
  .g4 { grid-template-columns: repeat(4, 1fr); }
  figure { margin: 0; background: #EFE9DC; border-radius: 16px; padding: 8px 8px 12px; text-align: center; }
  figure svg { width: 100%; height: auto; display: block; }
  figcaption { font: 500 14px system-ui, sans-serif; margin-top: 6px; }
</style></head><body><main>
  <div class="kicker">BabyDashNow · Monday Minute</div>
  <h1>Amara <em>&amp; Bibou</em></h1>
  <div class="top">
    <div class="hero">${amara.portrait('calme', 'hero')}</div>
    <div>
      <h2 style="margin-top:0">Expressions d'Amara</h2>
      <div class="grid g4">${Object.keys(amara.EXPRESSIONS).map((e) => tile(face(e), LABELS[e])).join('')}</div>
      <h2>Bibou</h2>
      <div class="grid g4">${bibou.REACTIONS.map((r) => tile(bibou.portrait(r), LABELS[r])).join('')}</div>
    </div>
  </div>
</main></body></html>`;

process.stdout.write(html);
