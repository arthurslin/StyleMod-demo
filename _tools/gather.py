"""Collect openly licensed candidate photos and build contact sheets for manual review."""
import json, os, re, time, urllib.parse, urllib.request, html, io, sys
from concurrent.futures import ThreadPoolExecutor
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image, ImageDraw

OUT = '_cand'
UA = 'StyleModDemo/0.1 (concept mockup; https://github.com/arthurslin/StyleMod-demo)'
OK = {'cc0', 'pdm', 'by', 'by-sa'}
QUERIES = {
  'crop': 'crop top woman street style', 'tank': 'ribbed tank top', 'polo': 'knit polo shirt',
  'tee': 'white t-shirt person', 'oxford': 'oxford button shirt man', 'sweater': 'knit sweater fashion',
  'overtee': 'oversized t-shirt', 'sweatshirt': 'sweatshirt street style', 'blouse': 'satin blouse fashion',
  'wide': 'wide leg trousers fashion', 'cargo': 'cargo pants street style', 'jeans': 'straight jeans street style',
  'wjeans': 'baggy jeans street style', 'joggers': 'jogger pants fashion', 'skirt': 'midi skirt street style',
  'pleat': 'pleated skirt fashion', 'track': 'track pants street style', 'chunky': 'chunky sneakers',
  'sneaker': 'white sneakers', 'runner': 'running shoes', 'loafer': 'leather loafers', 'boot': 'chelsea boots',
  'sandal': 'block heel sandals', 'blazer': 'oversized blazer street style', 'trench': 'trench coat street style',
  'chore': 'work jacket canvas', 'bag': 'crossbody bag', 'scarf': 'wool scarf', 'cap': 'baseball cap',
  'beanie': 'beanie hat', 'seoul': 'Seoul Fashion Week street style', 'seoul2': 'Seoul Fashion Week model',
  'korean': 'Korean street fashion', 'hongdae': 'Seongsu Hongdae fashion street style',
}

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()

def strip(text):
    return html.unescape(re.sub(r'<[^>]+>', '', text or '')).strip()

def commons(q):
    url = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode({
        'action': 'query', 'format': 'json', 'generator': 'search', 'gsrnamespace': 6, 'gsrlimit': 8,
        'gsrsearch': q + ' filetype:bitmap', 'prop': 'imageinfo', 'iiprop': 'url|extmetadata',
        'iiurlwidth': 500, 'iiextmetadatafilter': 'LicenseShortName|Artist'})
    res = []
    for p in json.loads(get(url)).get('query', {}).get('pages', {}).values():
        i = p['imageinfo'][0]; m = i['extmetadata']
        lic = m.get('LicenseShortName', {}).get('value', '')
        if not re.match(r'(CC0|Public domain|CC BY(-SA)? \d)', lic): continue
        res.append(dict(title=p['title'][5:], img=i['thumburl'], page=i['descriptionurl'], license=lic,
                        creator=strip(m.get('Artist', {}).get('value', ''))[:80], source='Wikimedia Commons'))
    return res

def openverse(q):
    url = 'https://api.openverse.org/v1/images/?' + urllib.parse.urlencode({
        'q': q, 'license_type': 'commercial,modification', 'page_size': 8, 'mature': 'false'})
    res = []
    for r in json.loads(get(url)).get('results', []):
        if r['license'] not in OK: continue
        res.append(dict(title=r['title'] or '', img=r['url'], page=r['foreign_landing_url'],
                        license=f"{r['license'].upper()} {r['license_version'] or ''}".strip(),
                        creator=(r.get('creator') or '')[:80], source=r['source']))
    return res

def fetch(c):
    try:
        im = Image.open(io.BytesIO(get(c['img']))).convert('RGB')
        im.thumbnail((640, 640))
        im.save(c['file'], quality=80)
        return True
    except Exception:
        return False

os.makedirs(OUT, exist_ok=True)
catalog = {}
for key, q in QUERIES.items():
    cands = []
    for fn in (commons, openverse):
        try: cands += fn(q)
        except Exception as e: print('ERR', key, fn.__name__, e)
        time.sleep(3.2)
    for n, c in enumerate(cands):
        c['id'] = f'{key}{n}'; c['file'] = f'{OUT}/{c["id"]}.jpg'
    with ThreadPoolExecutor(6) as ex:
        ok = list(ex.map(fetch, cands))
    catalog[key] = [c for c, y in zip(cands, ok) if y]
    print(key, len(catalog[key]), flush=True)

json.dump(catalog, open(f'{OUT}/catalog.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# Contact sheets, 8 keys per sheet, labelled with candidate ids.
keys = list(catalog)
for s in range(0, len(keys), 6):
    rows = keys[s:s + 6]
    W, H = 170, 200
    sheet = Image.new('RGB', (W * 8, H * len(rows)), 'white')
    d = ImageDraw.Draw(sheet)
    for y, key in enumerate(rows):
        for x, c in enumerate(catalog[key][:8]):
            im = Image.open(c['file']); im.thumbnail((W - 6, H - 22))
            sheet.paste(im, (x * W + 3, y * H + 18))
            d.text((x * W + 3, y * H + 3), c['id'], fill='red')
    sheet.save(f'{OUT}/sheet{s // 6}.jpg', quality=82)
print('done')
