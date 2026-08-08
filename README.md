# slide-deck-html

A Claude skill for producing professional 1280×720 fixed-frame HTML presentation decks from
meeting minutes, requirements documents, transcripts, or Excel data.

## What this skill produces

A single HTML file containing multiple stacked slides in a specific corporate
document style — blue accents, Noto Serif JP headings, two-column layouts, info-tables, inline
SVG diagrams.

**One file, but not offline-proof.** The deck is one `.html` with all CSS inlined — no sidecar
assets — but it pulls Noto Sans JP / Noto Serif JP / Inter from Google Fonts at open time. On a
closed network, or when the file is opened from an email attachment without internet, the
headings fall back to a generic serif and the layout shifts by a few pixels. Nothing errors; it
just looks different. If the deck must survive a closed environment, embed the fonts as base64
(Japanese fonts need subsetting) or accept the fallback deliberately.

The style was originally developed for enterprise stakeholder materials and is
well-suited for stakeholder-facing 資料 / プレゼン / ブリーフィング.

## How to install

This is a Claude skill folder. To use it:

1. Zip the entire `slide-deck-html/` folder
2. Upload to Claude (claude.ai → Skills → Add skill, or via API)

**If you want the 図解パーツ (40-type diagram) integration, install `diagram-parts-html` too.**
`SKILL.md` calls `../diagram-parts-html/scripts/inject_css.py` and `.../verify_html.py` by
relative path, so the two folders must sit side by side:

```
workflows/
├── slide-deck-html/
└── diagram-parts-html/
```

Installing `slide-deck-html/` alone still works for plain decks, but the diagram steps will fail
to find the scripts — and the failure mode is the one SKILL.md warns hardest about: someone hand-
copies an excerpt of the standard CSS, and the figures render as unstyled blank divs with no
error.
3. The skill will then trigger automatically on relevant requests

## How it works

When you ask Claude to "資料化して" / "HTMLにまとめて" / "スライド作って" / "v9と同じスタイルで"
on top of meeting minutes, transcripts, requirements docs, or Excel data, this skill activates
and walks Claude through:

1. Read the source material thoroughly
2. Outline the slide structure (and confirm with you for long decks)
3. Generate slides using templates from `assets/`
4. Validate the output against a quality checklist

## Folder structure

```
slide-deck-html/
├── SKILL.md                   ← skill instructions (Claude reads this)
├── README.md                  ← this file
├── assets/
│   ├── template_base.html     ← shell with full CSS
│   ├── slide_cover.html       ← cover slide template
│   ├── slide_summary.html     ← topic overview (two-col + diagram)
│   ├── slide_detail_twocol.html  ← detailed requirements
│   ├── slide_table.html       ← implementation policy + risks
│   ├── slide_questions.html   ← confirmation items
│   └── slide_section_divider.html  ← chapter break (optional)
└── references/
    ├── design_system.md       ← colors, fonts, spacing rules
    ├── content_strategy.md    ← source → slide mapping; density rules
    └── svg_diagrams.md        ← five canonical SVG diagram patterns
```

## What the deck looks like

- 1280×720px slides stacked vertically on a dark gray (#2a2a2a) page
- Per-topic 5-slide pattern: summary → detail → detail → policy/risk table → confirmation
- Em-dash (―) blue bullets, blue accent (#2563EB), Noto Serif JP for headings, Inter for English labels
- Print-ready: opens in any browser; browser print gives **one slide per page** at 1280×720
  (`@page` + `break-after` are set in `template_base.html`). Verified with headless Chrome:
  3 slides → 3 pages, MediaBox 960×540pt. Without those rules the same deck printed as
  2 US-Letter pages with slides cut across the boundary.

## What it's NOT for

- Short summaries that fit in a chat message (just answer in chat)
- Editing existing styled HTML where you only want minor text changes
- Word/PowerPoint output (use docx/pptx skills instead)
- English-primary decks (the typography assumes Japanese-primary)
