// Bibou — le bébé co-personnage, emmailloté, avec sa mèche rebelle.
// Repère : viewBox 0 0 300 300, tête centrée en (150, 118).
const C = require('./palette');

const REACTIONS = ['fascine', 'boude', 'content', 'dort'];

function eyes(type) {
  const L = 124, R = 176, y = 124;
  if (type === 'dort' || type === 'content') {
    // Yeux fermés : arc vers le bas qui dort, arc vers le haut quand il rit.
    const d = type === 'dort' ? 5 : -7;
    return [L, R].map((x) => `<path d="M ${x - 11} ${y} Q ${x} ${y + d} ${x + 11} ${y}" fill="none"` +
      ` stroke="${C.hair}" stroke-width="3.6" stroke-linecap="round"/>`).join('');
  }
  const r = type === 'fascine' ? 15 : 12;
  return [L, R].map((x) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#1A120E"/>` +
    `<circle cx="${x + 4}" cy="${y - 4}" r="${r * 0.32}" fill="#fff"/>` +
    `<circle cx="${x - 3}" cy="${y + 4}" r="${r * 0.14}" fill="#fff"/>`).join('');
}

function brows(type) {
  if (type !== 'boude') return '';
  return `<path d="M 112 102 L 134 108 M 188 102 L 166 108" stroke="${C.hair}" stroke-width="3.4" stroke-linecap="round"/>`;
}

function mouth(type) {
  const x = 150, y = 152;
  switch (type) {
    case 'fascine': return `<ellipse cx="${x}" cy="${y + 2}" rx="6" ry="7" fill="${C.lipDark}"/>`;
    case 'boude': return `<path d="M ${x - 12} ${y + 4} Q ${x} ${y - 6} ${x + 12} ${y + 4}" fill="none" stroke="${C.lipDark}" stroke-width="3.6" stroke-linecap="round"/>` +
      `<path d="M ${x - 6} ${y + 6} Q ${x} ${y + 10} ${x + 6} ${y + 6}" fill="none" stroke="${C.lip}" stroke-width="2.4" stroke-linecap="round"/>`;
    case 'content': return `<path d="M ${x - 16} ${y - 4} Q ${x} ${y + 22} ${x + 16} ${y - 4} Z" fill="${C.lipDark}"/>` +
      `<ellipse cx="${x}" cy="${y + 8}" rx="7" ry="4" fill="${C.blush}"/>`;
    case 'dort': return `<ellipse cx="${x}" cy="${y + 2}" rx="4" ry="5" fill="${C.lipDark}"/>`;
  }
}

function baby(type = 'fascine') {
  const arms = type === 'content'
    ? `<path d="M 92 196 C 74 176 68 158 76 150" fill="none" stroke="${C.swaddleShade}" stroke-width="22" stroke-linecap="round"/>
       <path d="M 208 196 C 226 176 232 158 224 150" fill="none" stroke="${C.swaddleShade}" stroke-width="22" stroke-linecap="round"/>
       <circle cx="76" cy="146" r="11" fill="${C.skin}"/><circle cx="224" cy="146" r="11" fill="${C.skin}"/>`
    : '';
  return `<g class="bibou">
    <path d="M 70 300 C 60 230 90 176 150 172 C 210 176 240 230 230 300 Z" fill="${C.swaddle}" stroke="${C.swaddleShade}" stroke-width="4"/>
    <path d="M 196 190 C 224 214 234 260 228 300 L 200 300 C 210 260 206 220 196 190 Z" fill="${C.swaddleShade}" opacity="0.8"/>
    <path d="M 82 214 C 120 230 180 230 218 214" fill="none" stroke="${C.sage}" stroke-width="5" stroke-linecap="round"/>
    <path d="M 150 230 C 140 260 128 284 120 300" fill="none" stroke="${C.swaddleShade}" stroke-width="4" stroke-linecap="round"/>
    ${arms}
    <ellipse cx="90" cy="124" rx="12" ry="15" fill="${C.skin}"/>
    <ellipse cx="210" cy="124" rx="12" ry="15" fill="${C.skin}"/>
    <circle cx="150" cy="118" r="62" fill="${C.skin}"/>
    <path d="M 190 70 C 214 96 216 150 186 172 C 204 140 204 100 190 70 Z" fill="${C.skinShade}" opacity="0.25"/>
    <path d="M 146 58 C 140 40 152 28 166 32 C 178 36 176 50 166 52 C 158 54 156 46 162 44" fill="none" stroke="${C.hair}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M 128 62 C 134 54 142 52 148 56" fill="none" stroke="${C.hair}" stroke-width="3.4" stroke-linecap="round"/>
    <ellipse cx="114" cy="146" rx="14" ry="9" fill="${C.blush}" opacity="0.3"/>
    <ellipse cx="186" cy="146" rx="14" ry="9" fill="${C.blush}" opacity="0.3"/>
    ${eyes(type)}
    ${brows(type)}
    <path d="M 146 140 Q 150 144 154 140" fill="none" stroke="${C.skinShade}" stroke-width="2.6" stroke-linecap="round"/>
    ${mouth(type)}
  </g>`;
}

function portrait(type = 'fascine') {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">${baby(type)}</svg>`;
}

module.exports = { baby, portrait, REACTIONS };
