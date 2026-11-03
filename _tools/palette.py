import re
p = 'index.html'
s = open(p, encoding='utf-8').read()

light = {
    '--swatch-line': 'rgba(42, 52, 41, .25)', '--soft-ink': '#3a4438', '--lay': '#eae5d9',
    '--bg': '#f4f1ea', '--surface': '#fbf9f4', '--sunken': '#eae5d9', '--ink': '#2a3429', '--muted': '#535a4e',
    '--line': '#d5cfc0', '--line-strong': '#7e7f6f', '--accent': '#3f5a3c', '--accent-dark': '#2a3429', '--accent-soft': '#e3e6d6',
}
head, rest = s.split('@media (prefers-color-scheme: dark)', 1)
for k, v in light.items():
    head, n = re.subn(re.escape(k) + r': [^;]+;', f'{k}: {v};', head, count=1)
    assert n == 1, k

dark = {
    '#1a1714': '#171c16', '#24201c': '#20261f', '#2e2924': '#2a3129', '#f4eee5': '#f4f1ea', '#bdb2a4': '#b9bdae',
    '#40392f': '#3b4339', '#8f8475': '#868c7b', '#f0a27c': '#b4c79a', '#f8c3a7': '#d0ddbb', '#40281c': '#2f3b2b',
    '#2a1309': '#1a2118', '#e6d8ca': '#dde0d0', 'rgba(244, 238, 229, .35)': 'rgba(244, 241, 234, .35)',
}
for a, b in dark.items():
    assert a in rest, a
    rest = rest.replace(a, b)
rest = rest.replace('dialog::backdrop { background: rgba(33, 28, 24, .5); }', 'dialog::backdrop { background: rgba(42, 52, 41, .5); }')
open(p, 'w', encoding='utf-8', newline='').write(head + '@media (prefers-color-scheme: dark)' + rest)
print('ok')
