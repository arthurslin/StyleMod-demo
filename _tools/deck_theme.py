"""Theme the site after the StyleMod presentation: midnight indigo, violet and electric blue."""
p = 'index.html'
s = open(p, encoding='utf-8').read()
def R(a, b):
    global s
    assert a in s, a
    s = s.replace(a, b)

start = s.index('  :root {\n    color-scheme: light;')
end = s.index('  *, *::before, *::after { box-sizing: border-box; }')
s = s[:start] + '''  /* Colors from the StyleMod deck: midnight background, violet (#7b00ff) and
     electric blue (#002aff) glows, white type, soft grey (#b5b5b7) secondary text. */
  :root {
    color-scheme: dark;
    --bg: #07051a; --surface: #120c33; --sunken: #1a1245; --ink: #ffffff; --muted: #b5b5b7;
    --line: #2b2470; --line-strong: #5a56d6; --accent: #7d95ff; --accent-dark: #b3c0ff; --accent-soft: #1e1660;
    --on-ink: #07051a; --on-accent: #ffffff; --soft-ink: #dcdbe8; --hover: #1a1245; --swatch-line: rgba(255, 255, 255, .3);
    --lay: #ecebf4; --card-line: rgba(0, 42, 255, .6);
    --violet: #7b00ff; --electric: #002aff;
    --glow: radial-gradient(1100px 620px at 88% -12%, rgba(123, 0, 255, .38), transparent 60%),
            radial-gradient(900px 560px at -12% 108%, rgba(0, 42, 255, .32), transparent 60%);
    --display: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
    --serif: var(--display);
    --script: "Great Vibes", "Snell Roundhand", cursive;
    --sans: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    --radius: 10px;
  }
  :root[data-theme="light"] {
    color-scheme: light;
    --bg: #f5f4ff; --surface: #ffffff; --sunken: #ebe9fb; --ink: #0d005e; --muted: #4a4868;
    --line: #d6d3f2; --line-strong: #6d6aa8; --accent: #2a2ad6; --accent-dark: #0d005e; --accent-soft: #e6e4ff;
    --on-ink: #ffffff; --on-accent: #ffffff; --soft-ink: #26215a; --hover: #ffffff; --swatch-line: rgba(13, 0, 94, .25);
    --card-line: rgba(0, 42, 255, .35);
    --glow: radial-gradient(1100px 620px at 88% -12%, rgba(123, 0, 255, .12), transparent 60%),
            radial-gradient(900px 560px at -12% 108%, rgba(0, 42, 255, .1), transparent 60%);
  }
''' + s[end:]
R('''    margin: 0; background: var(--bg); color: var(--ink);''', '''    margin: 0; background: var(--glow), var(--bg); background-attachment: fixed; color: var(--ink);''')
R('''  h1, h2, h3, h4 { font-family: var(--serif); font-weight: 500;''', '''  h1, h2, h3, h4 { font-family: var(--display); font-weight: 300; letter-spacing: -.01em;''')
R('''  .site-head { border-bottom: 1px solid var(--line); background: var(--bg); }''', '''  .site-head { border-bottom: 1px solid var(--line); background: transparent; }''')
R('''  .brand { font-family: var(--serif); font-size: 1.3rem; letter-spacing: .01em; }
  .brand b { font-weight: 500; color: var(--accent); }''', '''  .brand { font-family: var(--script); font-size: 2rem; line-height: 1; color: var(--ink); }
  .brand small { display: block; margin: 2px 0 0 26px; font-size: 1rem; }''')
R('''    <div class="brand">Style<b>Mod</b> Outfit Builder</div>''', '''    <div class="brand" aria-label="StyleMod, Styled By You">StyleMod,<small>Styled By You</small></div>''')
R('''  .btn.primary { background: var(--accent); border-color: var(--accent); color: var(--on-accent); font-weight: 600; }''',
  '''  .btn.primary { background: linear-gradient(90deg, var(--violet), var(--electric)); border-color: transparent; color: #fff; font-weight: 600; }''')
R('''  .card { background: var(--surface); border: 1px solid var(--line);''', '''  .card { background: var(--surface); border: 1px solid var(--card-line);''')
R('''<title>StyleMod Outfit Builder</title>''', '''<title>StyleMod Outfit Builder</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Great+Vibes&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">''')
R('''<h1 class="intro-title" tabindex="-1">Outfits built from what you tell us.</h1>''', '''<h1 class="intro-title" tabindex="-1">Your Style. Your Preferences. Your Rules.</h1>''')
# Dark by default, like the deck; the toggle still offers a light version.
R('''paintTheme(window.matchMedia("(prefers-color-scheme: dark)").matches);''', '''document.documentElement.dataset.theme = "dark";
paintTheme(true);''')
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
