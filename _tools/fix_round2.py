import re, urllib.request
from PIL import Image
UA = {'User-Agent': 'Mozilla/5.0 (StyleMod demo)'}
def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
        return r.read()

c = open('credits.html', encoding='utf-8').read()
for sid, pid, slug in [
    ('chunky-snk', '1758702701300-372126112cb4', 'a-hand-holds-a-sneaker-over-its-reflection-Sq3VpbHaHcs'),
    ('runner', '1625860191460-10a66c7384fb', 'white-nike-low-top-sneakers-jVerIoX3y7c'),
    ('over-tee', '1716951735063-3d60c2c288e4', 'a-group-of-four-t-shirts-with-the-word-comfort-on-them-3h-390a18dE'),
]:
    open(f'images/{sid}.jpg', 'wb').write(get(f'https://images.unsplash.com/photo-{pid}?w=520&h=650&fit=crop&crop=entropy&fm=jpg&q=70'))
    label = sid.replace('-', ' ')
    c, n = re.subn(r'<a href="[^"]+">' + label + '</a>', f'<a href="https://unsplash.com/photos/{slug}">{label}</a>', c)
    assert n == 1, sid
open('credits.html', 'w', encoding='utf-8').write(c)

W = 180
sheet = Image.new('RGB', (W * 3, 225), 'white')
for i, sid in enumerate(['chunky-snk', 'runner', 'over-tee']):
    im = Image.open(f'images/{sid}.jpg'); im.thumbnail((W, 225)); sheet.paste(im, (i * W, 0))
sheet.save('_tools/review2.jpg', quality=85)

p = 'index.html'
s = open(p, encoding='utf-8').read()
def R(a, b):
    global s
    assert a in s, a
    s = s.replace(a, b)
R('''  const allowed = CATALOG.filter(item => matches(item) && !a.avoid.includes(item.color));
  if (allowed.length) return allowed;
''', '''  const allowed = CATALOG.filter(item => matches(item) && !a.avoid.includes(item.color));
  const forOccasion = allowed.filter(item => item.occ.includes(ctx.occasion));
  if (forOccasion.length) return forOccasion;
  if (allowed.length) return allowed;
''')
R('''<i style="background:${COLORS[item.color].hex}" aria-hidden="true"></i>${COLORS[item.color].label}</figcaption>''', '''<i style="background:${COLORS[item.color].hex}" aria-hidden="true"></i>Yours: ${COLORS[item.color].label}</figcaption>''')
R('''Real photos show the style. Your color is marked on each one.''', '''Photos show the style, which may be in a different color. Your color is marked on each one.''')
R('''  @media (min-width: 640px) {
    .card { padding: 22px; }''', '''  @media (min-width: 560px) and (max-width: 879px) {
    .lay { grid-template-columns: repeat(4, 1fr); }
  }
  @media (min-width: 640px) {
    .card { padding: 22px; }''')
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
