const jsdom = require('jsdom');
const { JSDOM } = jsdom;
const fs = require('fs');

const html = fs.readFileSync('public/index.html', 'utf8');
const script = fs.readFileSync('public/script.js', 'utf8');

const dom = new JSDOM(html, { runScripts: 'outside-only', resources: 'usable', url: 'http://localhost' });
const window = dom.window;
const document = window.document;

window.Chart = class { constructor() { return { destroy: () => {} }; } };
window.Chart.register = () => {};
window.matchMedia = () => ({ matches: false, addEventListener: () => {} });
window.fetch = async () => ({ ok: true, json: async () => ({ logs: {}, foodLogs: {} }) });
window.URL = { createObjectURL: () => '' };

try {
  dom.window.eval(script);
  console.log('Script evaluated without uncaught exceptions.');
} catch (e) {
  console.error('EVAL ERROR:', e.message, e.stack);
}
