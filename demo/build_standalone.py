"""Bundle local assets into one offline HTML file. No build dependencies."""
from pathlib import Path
import base64
import re
import argparse

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path, default=ROOT.parent / 'Руссмаркет — AI-сводка.html')
OUTPUT = parser.parse_args().output.resolve()
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

def data_uri(path):
    mime = {'.png': 'image/png', '.svg': 'image/svg+xml', '.ttf': 'font/ttf'}[path.suffix]
    return f'data:{mime};base64,' + base64.b64encode(path.read_bytes()).decode('ascii')

html = (ROOT / 'index.html').read_text()
css = '\n'.join((ROOT / name).read_text() for name in ['styles.css', 'refinements.css', 'readability.css', 'commercial.css', 'palettes.css', 'service.css', 'devices-vendor.css', 'motion-devices.css', 'matching.css', 'inverted.css'])
for match in set(re.findall(r'assets/[^\'"\)]+', css)):
    css = css.replace(match, data_uri(ROOT / match))
html = html.replace('<link rel="stylesheet" href="styles.css">', f'<style>{css}</style>')
html = html.replace('<link rel="stylesheet" href="refinements.css">', '')
html = html.replace('<link rel="stylesheet" href="readability.css">', '')
html = html.replace('<link rel="stylesheet" href="commercial.css">', '')
html = html.replace('<link rel="stylesheet" href="palettes.css">', '')
html = html.replace('<link rel="stylesheet" href="service.css">', '')
html = html.replace('<link rel="stylesheet" href="devices-vendor.css">', '')
html = html.replace('<link rel="stylesheet" href="motion-devices.css">', '')
html = html.replace('<link rel="stylesheet" href="matching.css">', '')
html = html.replace('<link rel="stylesheet" href="inverted.css">', '')
html = html.replace('<script src="answer-text.js"></script>', '<script>' + (ROOT / 'answer-text.js').read_text() + '</script>')
html = html.replace('<script src="app.js"></script>', '<script>' + (ROOT / 'app.js').read_text() + '</script>')
for match in set(re.findall(r'src="(assets/[^\"]+)"', html)):
    html = html.replace(f'src="{match}"', f'src="{data_uri(ROOT / match)}"')
licenses = '\n\n'.join((ROOT / 'assets' / file).read_text() for file in ['Manrope-OFL.txt', 'NotoSansDisplay-OFL.txt', 'Devices-LICENSE.txt'])
html = html.replace('</body>', '<!-- Font licenses (SIL OFL):\n' + licenses.replace('--', '—') + '\n-->\n</body>')
OUTPUT.write_text('\n'.join(line.rstrip() for line in html.splitlines()) + '\n')
print(f'Created {OUTPUT} ({OUTPUT.stat().st_size:,} bytes)')
