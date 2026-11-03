"""Presentation branch: reduce the quiz to three one-tap questions."""
p = 'index.html'
s = open(p, encoding='utf-8').read()
def R(a, b):
    global s
    assert a in s, a
    s = s.replace(a, b)

R('const STEP_COUNT = 5;', 'const STEP_COUNT = 3;')
R('''budget: [100, 400], sustainable: false, durable: false, trend: false, kstyle: false,''', '''budget: [100, 800], sustainable: false, durable: false, trend: true, kstyle: false,
  favorite: "",''')

start = s.index('const STEP_VIEWS = {')
end = s.index('function budgetLabel() {')
s = s[:start] + '''const STEP_VIEWS = {
  1: () => ({
    title: "Pick a color",
    hint: "We'll build your outfits around it.",
    body: `<fieldset class="section"><legend class="sr">Favorite color</legend>
        <div class="color-picks">${ALL.map(c => `<label class="color-pick"><input type="radio" name="favorite" value="${c}" ${answers.favorite === c ? "checked" : ""}><span><i style="background:${COLORS[c].hex}" aria-hidden="true"></i>${COLORS[c].label}</span></label>`).join("")}</div>
      </fieldset>`
  }),
  2: () => ({
    title: "Who are we dressing?",
    hint: "This sets the section and the dummy. We never infer it.",
    body: `<fieldset class="section"><legend class="sr">Section</legend>
        <div class="opts">${Object.entries(DEPTS).map(([k, v]) => option("radio", "dept", k, v, "", answers.dept === k)).join("")}</div>
      </fieldset>`
  }),
  3: () => ({
    title: "Where are you headed?",
    hint: "Pick the one that fits best.",
    body: `<fieldset class="section"><legend class="sr">Occasion</legend>
        <div class="opts">${Object.entries(OCCASIONS).map(([k, v]) => option("radio", "occasion", k, v, "", answers.occasions[0] === k)).join("")}</div>
      </fieldset>`
  })
};

''' + s[end:]

# Intro
R('<p class="eyebrow">Five quick questions</p>', '<p class="eyebrow">Three quick questions</p>')
R('''      <li><b>1</b> Occasion and vibe</li>
      <li><b>2</b> Color palette</li>
      <li><b>3</b> Body shape and fit goals (optional)</li>
      <li><b>4</b> Budget and shopping preferences</li>
      <li><b>5</b> Review and consent</li>
''', '''      <li><b>1</b> Pick a color</li>
      <li><b>2</b> Choose a section</li>
      <li><b>3</b> Pick an occasion</li>
''')

# Answers
R('''  else if (input.type === "radio") answers[input.name] = input.value;
''', '''  else if (input.name === "favorite") {
    answers.favorite = input.value;
    answers.palettes = [COLORS[input.value].family];
  } else if (input.name === "occasion") answers.occasions = [input.value];
  else if (input.type === "radio") answers[input.name] = input.value;
''')

# The chosen color leads the outfit.
R('''  if (item.photo) total += 3;
''', '''  if (item.photo) total += 3;
  if (item.color === a.favorite && (item.slot === "top" || item.slot === "bottom")) total += 7;
''')

# Require only the color; the other two have sensible defaults.
R('''  next()   {
    if (view < STEP_COUNT) { view += 1; render(); return; }''', '''  next()   {
    if (view === 3 && !answers.occasions.length) answers.occasions = ["casual"];
    if (view < STEP_COUNT) { view += 1; render(); return; }''')

R('''  .note { margin-top: 12px;''', '''  .color-picks { display: grid; grid-template-columns: repeat(auto-fill, minmax(92px, 1fr)); gap: 10px; }
  .color-pick { position: relative; cursor: pointer; }
  .color-pick input { position: absolute; opacity: 0; inset: 0; width: 100%; height: 100%; margin: 0; cursor: pointer; }
  .color-pick span { display: flex; flex-direction: column; align-items: center; gap: 6px; padding: 10px 4px; border: 1px solid var(--line-strong); border-radius: var(--radius); background: var(--surface); font-size: .9rem; }
  .color-pick i { width: 42px; height: 42px; border-radius: 50%; border: 1px solid var(--swatch-line); }
  .color-pick input:checked + span { border-color: var(--accent); box-shadow: inset 0 0 0 2px var(--accent); background: var(--accent-soft); font-weight: 600; }
  .color-pick input:focus-visible + span { outline: 3px solid var(--accent); outline-offset: 2px; }
  .note { margin-top: 12px;''')
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
