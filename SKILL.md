---
name: slide-deck-html
description: Build professional, fixed-frame (1280×720) HTML presentation decks from meeting minutes, requirements documents, transcripts, or Excel data. The output is a single HTML file (all CSS inlined; web fonts loaded from Google Fonts) with multiple stacked slides in a specific corporate-document style — blue accents, Noto Serif JP headings, two-column layouts, info-tables, inline SVG diagrams. Use this skill whenever the user wants a stakeholder-facing 資料 / スライド / ブリーフィング資料 / HTML deck / プレゼン資料 from raw input — including phrases like "資料化して", "HTMLにまとめて", "スライドにして", "v9と同じスタイル", "前回と同じ資料スタイル", "既存デッキ風", or any request to convert meeting transcripts / 議事録 / 横断管理表 / 仕様書 into a structured visual deliverable. Even when the user doesn't explicitly say "HTML", if the request is to organize multi-topic source material into a presentation-style deliverable for clients or executives, default to using this skill. Do NOT use it for short summaries that fit in a single chat message, for editing existing styled HTML files where the user only wants minor text changes, for non-Japanese decks unless the user explicitly requests, or for Word/PowerPoint output (use docx/pptx skills instead).
---

# slide-deck-html
> 🇯🇵 **スライドデッキHTML（ビジュアル基盤）** — 議事録／要件／文字起こし／Excel から固定枠1280×720のHTMLプレゼンを作る土台テンプレート。（フォルダ名 `slide-deck-html` が呼び出しIDのため英語のまま）

This skill produces a single HTML file containing multiple `1280×720` slides in a
specific corporate document style. The style was developed for enterprise stakeholder
materials (the "v9 deck") and is well-suited for:

- Meeting minutes structured for stakeholder review
- Requirements documents with action items, risks, and confirmations
- Multi-topic technical proposals (one topic = 4-6 slides)
- Excel-table-based status / cross-cutting management views, narrated as a deck

The output is a **single HTML file** that opens in any browser, scrolls vertically through the
deck, and can be exported to PDF (browser print — `@page` is set, so one slide becomes one
1280×720 page) or imported into PowerPoint via a separate conversion step.

One caveat worth stating to the user up front: the file inlines all its CSS but **loads fonts
from Google Fonts over the network**. In a closed environment the Noto Serif JP headings fall
back to a generic serif and the layout shifts slightly — silently, with no error. Say so when
the deck is destined for a closed network or email distribution.

---

## Workflow Overview

The work proceeds in four phases. Don't skip phases — quality drops fast when you do.

### Phase 1 — Read the source

Before writing any HTML, fully read whatever the user gave you (meeting transcript, requirements
doc, Excel sheet, prior version of the deck). Identify:

- **Topics**: distinct work items / issues / sections that each deserve their own slide cluster
- **For each topic**: the goal, the background/premise, the key decisions or proposed actions,
  the risks, and the open questions for stakeholders
- **Cross-cutting metadata**: target audience, date, organization, project name (for cover and footer)
- **Any prior version**: if the user provides v(N), they likely want v(N+1) — preserve structure,
  reflect new content, and consider adding `diff-tag` markers for what changed

If the source is sparse or you can't identify clear topics, ask the user before proceeding.

### Phase 2 — Outline the deck

Before generating slides, list the slides you plan to produce, in order. For each, specify:

- Slide type (cover / summary / detail / table / questions / divider)
- The action-title (one sentence with `<em>` emphasis)
- The lead-in (one sentence of context)
- Rough content list (what bullets, what diagram, what table rows)

Show this outline to the user and confirm before generating HTML, especially for decks longer
than 10 slides. This saves a lot of rework.

For each major topic, the canonical 5-slide pattern is:

| # | Slide type | Purpose |
|---|------------|---------|
| 1 | summary    | One-slide overview with goal + premise + scope diagram |
| 2 | detail (1/N) | First sub-requirement: 課題 → 対策 |
| 3 | detail (2/N) | Second sub-requirement (if any) |
| 4 | table      | 実装方針・リスク matrix (仕様 rows + リスク rows) |
| 5 | questions  | 確認事項 — questions for stakeholders |

Topics with only one sub-requirement collapse to 4 slides (skip the extra detail). Very simple
topics may collapse to 3 slides (summary + table + questions).

### Phase 3 — Generate the HTML

Start from `assets/template_base.html` (the empty shell with all CSS). Then for each slide,
copy the appropriate template from `assets/`:

- `slide_cover.html` — first slide of the deck
- `slide_summary.html` — topic overview with optional diagram
- `slide_detail_twocol.html` — detailed requirements
- `slide_table.html` — implementation policy + risks
- `slide_questions.html` — confirmation items
- `slide_section_divider.html` — chapter break (optional, for 3+ topics)

Replace placeholders carefully. The placeholder format is `{{NAME}}` and each template has a
guide comment at the bottom explaining what each placeholder expects.

Read these references when you need them:

- `references/design_system.md` — colors, fonts, spacing, dos and don'ts
- `references/content_strategy.md` — how to structure source material into slides; density rules
- `references/svg_diagrams.md` — five canonical SVG diagram patterns to embed inline

#### Need a diagram beyond the five SVG patterns?

Use the **`/diagram-parts-html`** workflow (`../diagram-parts-html/SKILL.md`) — the in-house
「図解パーツ標準仕様書」with 40 fixed figure types (比較 / マトリクス / ロジックツリー / 工程フロー /
ロードマップ / ファネル / スイムレーン / KPI / ウォーターフォール / リスクマップ / 3案比較 / RACI /
課題管理表 / エグゼクティブサマリー …). It returns an HTML fragment wrapped in
`<div class="dgs-scope">…</div>` that you drop into a slide's content area.

Three things to respect:

- That standard ships its own CSS (~58KB). **Never transcribe it by hand and never excerpt
  "just the types used so far"** — a trimmed stylesheet renders later figures as bare, unstyled
  divs, which is easy to miss until you open the file. Inject it with the script instead:

  ```bash
  python3 ../diagram-parts-html/scripts/inject_css.py <deck>.html
  ```

  It is idempotent, so run it **every time you add a figure**, not once at the start.
  (The `dgs-scope` wrapper keeps it from leaking into the deck's own styles.)
- Before delivering, run the standard's verifier and fix anything it reports:

  ```bash
  python3 ../diagram-parts-html/scripts/verify_html.py <deck>.html
  ```

- Its accent-color rule is **one accent per screen** — count it per slide, not per deck.
  This means the **orange** accent inside `dgs-scope` only; the deck's own `#2563EB` is a structural
  color and is not counted. (`verify_html.py` counts the orange one for you, per `.slide`.)
  Note that 19 of the 40 figure types carry a built-in accent, so **two figures on one slide often
  violates the rule** — check before pairing them.

Stick to `references/svg_diagrams.md` for simple inline schematics; reach for
`/diagram-parts-html` when the figure is a recognized consulting-deck type.

### Phase 4 — Validate and deliver

**Two verifiers, two jobs. Run both — neither one covers the other's ground.**

| What it checks | Script |
|---|---|
| **The deck itself** — `.slide` is 1280×720, `page-body` silently truncating content, `P.<n>` sequence, footer-left consistency, bullet characters other than `―`, colors absent from `design_system.md` | `scripts/verify_deck.py` |
| **The figures** (`dgs-scope`) and document-wide leftovers — standard CSS present *in full*, no surviving `{{PLACEHOLDER}}` or template guide text, `rowspan` holds a number, one-accent-per-slide inside figures | `../diagram-parts-html/scripts/verify_html.py` |

```bash
python3 scripts/verify_deck.py <deck>.html                        # always
python3 ../diagram-parts-html/scripts/verify_html.py <deck>.html  # always (it also
                                                                  # catches {{…}} in
                                                                  # figure-free decks)
```

Deliver only when **both** print `OK`. Don't eyeball either one.

**Why `verify_deck.py` exists.** `.slide` and `.page-body` are `overflow:hidden`, so content past
720px is **silently cut off** — no scrollbar, no error, no visible breakage. A deck whose table
lost its last row looks perfect apart from the missing row. The old instruction "check that no
scrollbar appears" was an empty check: `.slide`'s `scrollHeight` always equals its `clientHeight`
no matter what you cram in. `.page-body` is where the truncation is measurable, and that is what
`verify_deck.py` measures with headless Chrome.

**Still your job** (neither script judges it):

- **The deck's own blue.** `#2563EB` is this deck's *structural* color (item-id, section titles,
  bullets, takeaway, table headers). It is not counted as an "accent" — the one-per-slide rule
  applies only to the orange accent inside `dgs-scope` figures.
- Whether the content is *right* — density that technically fits but reads as crammed, item-id
  wording, whether each slide earns its place.

Then run through this checklist:

#### Density check (most common failure mode)
- [ ] `verify_deck.py` reports no `[分量超過]` (this replaces the old "no scrolling" eyeball check)
- [ ] No more than 6-10 bullets total per detail slide
- [ ] Total cell-lines in a table slide ≤ 13 (see `content_strategy.md` — "10 rows" and
      "3-line cells" cannot both hold)
- [ ] No more than 8 questions on a confirmation slide
- [ ] All content blocks have breathing room (not crammed edge to edge)

#### Style consistency check
- [ ] `verify_deck.py` reports no `[ページ番号]` / `[フッター]` / `[箇条書き]` / `[配色]`
- [ ] item-id format is consistent (e.g., always `NO.<X> — <subtitle>`) — not machine-checked

#### Content quality check
- [ ] Every action-title has an `<em>` emphasis on the most important phrase
- [ ] Every lead-in adds context the action-title doesn't already have
- [ ] Every takeaway box says one specific thing, not a generic platitude
- [ ] No two slides repeat the same information without good reason

If any check fails, fix it before delivering.

#### Output location
Save the final HTML to `/mnt/user-data/outputs/<descriptive_name>.html` and use `present_files`
to share it with the user.

---

## Quick-Start Pattern: Single-Topic Deck

For a deck covering one focused topic (e.g., a single proposal, a single meeting's outcomes),
the minimum viable structure is:

```
1. Cover                           (slide_cover.html)
2. サマリー                          (slide_summary.html with diagram)
3. 詳細要件                          (slide_detail_twocol.html)
4. 実装方針・リスク                   (slide_table.html)
5. 確認事項                          (slide_questions.html)
```

5 slides. About 20-30 minutes of careful work. This is the template to reach for when the user
gives a relatively contained piece of source material.

## Quick-Start Pattern: Multi-Topic Deck (the "v9" pattern)

For decks covering multiple work items or issues:

```
1. Cover                                                  (slide_cover.html)
For each topic (sorted by priority):
  N. サマリー                                              (slide_summary.html)
  N+1. 詳細要件 (1/N)                                       (slide_detail_twocol.html)
  N+2. 詳細要件 (2/N)         [if needed]                   (slide_detail_twocol.html)
  N+3. 実装方針・リスク                                       (slide_table.html)
  N+4. 確認事項                                             (slide_questions.html)
```

10-50+ slides. A multi-day effort. Skim the source, outline first, get user buy-in on the
outline, then generate.

---

## Common Mistakes and How to Avoid Them

### Mistake: Cramming too much into a slide
**Symptom**: Bullets get cut off, footer overlaps content, or you're tempted to shrink fonts.
**Fix**: Split into another slide. The deck pays for breathing room with clarity.

### Mistake: Treating action-title as a section name
**Symptom**: action-title says things like "クーポン機能について" or "本件のまとめ"
**Fix**: Action-title is a *decision* or *recommendation*, not a section name. Rewrite it as a
sentence stating what will happen / what's been decided.

### Mistake: Inventing new colors or fonts
**Symptom**: Slides start using purple, green, or pink accents.
**Fix**: Stick to the 14 named colors. The whole deck's polish comes from rigorous restraint.

### Mistake: Markdown-style bullets
**Symptom**: Output uses `<li>` with default disc bullets, or `*` markdown.
**Fix**: All bullets must use `block-body ul` which renders the blue em-dash `―`. The CSS does
this automatically — just use `<ul><li>...</li></ul>` inside `block-body`.

### Mistake: Skipping the outline phase
**Symptom**: You generate 30 slides and then realize the structure is wrong.
**Fix**: For decks >10 slides, always outline first and get user confirmation before
generating HTML.

### Mistake: Ignoring the source material's natural structure
**Symptom**: You impose an outline that doesn't match what's actually in the source.
**Fix**: Let the source tell you the topics. If the meeting minutes have 5 distinct issue
sections, that's probably 5 topics in the deck.

### Mistake: Inventing facts
**Symptom**: To fill a 詳細要件 slide, you make up numbers, decisions, or risks.
**Fix**: If the source doesn't say it, don't put it on the slide. Mark gaps with `?` or put
them in 確認事項 instead. The deck's value depends on accurately reflecting what's actually in
the source.

---

## Variations and Extensions

### Updating an existing deck (v(N) → v(N+1))

When the user provides a previous version of the deck plus new meeting notes:

1. Read both — identify what's changed
2. Use `diff-tag` markers (`<span class="diff-tag">5/12 追加</span>`) on new content
3. Use `diff-row` class on table rows that are new
4. Optionally use the standalone red callout pattern (see content_strategy.md) for major
   additions
5. Keep all unchanged slides as-is — don't restyle just because you can

### Reducing the deck for a different audience

If the user says "短くして" or "エグゼクティブ向けに", consider:
- Drop 詳細要件 slides; keep only summary + table + questions per topic
- Compress to 1 slide per topic if possible
- Replace detailed bullets with takeaway-only boxes
- Move 確認事項 to a single end-of-deck consolidated slide

### Outputting only a single topic from a multi-topic deck

If the user wants just one topic's slides extracted, simply isolate that topic's slide range,
renumber pages, and adjust the cover/title.

---

## When to Push Back

- If the source is too sparse to fill the canonical 5-slide pattern, don't pad with filler.
  Tell the user the source needs more context, or collapse to a 2-3 slide minideck.
- If the user asks you to use this style for content that fundamentally doesn't fit (e.g.,
  a creative writing piece, a tutorial walkthrough), suggest a different output format.
- If you don't have enough about the audience or purpose, ask.

---

## Known defects

Before relying on a guideline in this skill, check [BACKLOG.md](BACKLOG.md) — it records what is
measured-and-broken versus what is merely documented. The headline: `.slide` and `.page-body` are
`overflow:hidden`, so **anything that does not fit is silently deleted**. `scripts/verify_deck.py`
now detects that (and five other silent failures), but the underlying `overflow:hidden` design is
unchanged — never assume a slide is fine because it looks fine.

---

## File Layout (when packaged)

```
slide-deck-html/
├── SKILL.md                           ← this file
├── BACKLOG.md                         ← known defects / open issues
├── assets/
│   ├── template_base.html             ← shell with full CSS, paste slides into <slides-container>
│   ├── slide_cover.html               ← cover slide template
│   ├── slide_summary.html             ← topic overview (two-col + diagram)
│   ├── slide_detail_twocol.html       ← detailed requirements
│   ├── slide_table.html               ← implementation policy + risks
│   ├── slide_questions.html           ← confirmation items
│   └── slide_section_divider.html     ← chapter break (optional)
├── scripts/
│   ├── verify_deck.py                 ← ★Phase 4: deck-body delivery gate (headless Chrome)
│   └── selftest_verify_deck.py        ← proves each check actually stops broken input
└── references/
    ├── design_system.md               ← colors, fonts, spacing, restraint rules
    ├── content_strategy.md            ← source material → slide mapping; density rules
    └── svg_diagrams.md                ← five canonical SVG diagram patterns
```

`scripts/` depends on nothing outside this folder. The figure verifier lives in the sibling
`diagram-parts-html/scripts/` — see the table in Phase 4 for which one checks what.
