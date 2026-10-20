// Export the exact same answer as the browser download. Node built-ins only.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = __dirname;
const app = fs.readFileSync(path.join(root, 'app.js'), 'utf8');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const launch = html.match(/<details class="launch-copy[\s\S]*?<\/details>/)[0]
  .match(/<p>[\s\S]*?<\/p>/g).map(p=>p.replace(/<[^>]*>/g, '')).join(' ');
const segments = [
  app.slice(app.indexOf('const cases = ['), app.indexOf("let selectedCase=")),
  app.slice(app.indexOf('const prompts={'), app.indexOf("let currentPrompt=")),
  app.slice(app.indexOf('function summaryText()'), app.indexOf('function download(')),
  fs.readFileSync(path.join(root, 'answer-text.js'), 'utf8')
];
const context = vm.createContext({launch});
vm.runInContext(segments.join('\n'), context);
const result = vm.runInContext('fullAnswerText(launch)', context);
const output = path.join(root, '..', 'Ответ на тестовое — Руссмаркет.txt');
fs.writeFileSync(output, result);
console.log(`Created ${output} (${Buffer.byteLength(result)} bytes)`);
