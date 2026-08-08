# Design System Reference

This skill produces HTML decks in a specific design language. Don't deviate from these tokens —
the consistency across slides is what makes the deck feel polished.

## Frame

- **Slide size**: exactly `1280 × 720 px` (16:9). Hard-coded. Don't change.
- **Body background**: `#2a2a2a` (dark gray, makes white slides pop)
- **Slide background**: `#ffffff`
- **Slide gap**: `30px` between slides
- **Slide border**: `1px solid #D0D0D0` plus `box-shadow: 0 8px 32px rgba(0,0,0,0.5)`

## Color Palette

Use these named colors only. Don't introduce new ones unless absolutely necessary.

| Role | Hex | Usage |
|------|-----|-------|
| Primary blue | `#2563EB` | Accents, section titles, item-id, takeaway border, em text, bullet markers |
| Pale blue (deep) | `#DBEAFE` | Active diagram nodes, highlight cards |
| Pale blue (light) | `#EFF6FF` | Takeaway box background, secondary diagram nodes |
| Ink dark | `#0F172A` | Primary headings (h1, action-title, section-title, takeaway text) |
| Ink body | `#1A2538` | Body text, table cell content |
| Mid gray | `#555` | Subtitles, lead-in text, footer right side |
| Light gray | `#F5F5F4` | Cover bottom band, table th background |
| Faint gray | `#FAFAFA` | Diagram container background |
| Border light | `#E5E5E5` | Table row borders |
| Border medium | `#D0D0D0` | Page header/footer borders, slide borders, diagram borders |
| Mid muted | `#9CA3AF` | Inactive diagram elements (dashed) |
| Faint muted | `#888` / `#999` | Footer text, very low-priority labels |
| Slide-meta gray | `#aaa` | `.slide-meta` labels above a slide (optional, outside the frame) |
| Warning orange | `#D97706` | accent-warn class — risks, problems, caution |
| Diff red | `#DC2626` | Newly added content (with #FEE2E2 background) |
| Diff bg | `#FEE2E2` | Tag background for "added on date" markers |
| Diff row bg | `#FEF2F2` | Highlighting whole rows that were added later |

## Typography

Three fonts loaded from Google Fonts. Each has a specific role.

### `Noto Sans JP` (default body font)
- Block body, table cells, lead-in, subtitle
- Weights used: 400 (regular), 500 (medium), 600 (semibold), 700 (bold)

### `Noto Serif JP` (heading font)
- Cover h1 (46px)
- Action title (22px)
- Section title (17px)
- Section divider title
- This is the "premium" feel — only for actual headings, not labels.

### `Inter` (English/Latin font)
- Category labels (cover): 12px, letter-spacing 0.3em, uppercase
- Item ID: 11px, letter-spacing 0.2em
- Section labels: 10px, letter-spacing 0.25em, uppercase
- Diagram titles: 10px, letter-spacing 0.2em, uppercase
- Page footer: 10px, letter-spacing 0.1em
- Takeaway label: 10px, letter-spacing 0.2em
- Date and org on cover: 14px, letter-spacing 0.05-0.08em

### Letter-spacing pattern
English Inter labels always have generous letter-spacing (0.1em to 0.3em). This is deliberate —
it makes them feel like badges/labels, not body text. Don't reduce these values.

## Spacing System

The deck uses a 7-step spacing scale, mostly in multiples of 4px:

- **2px** — micro-gap between bullet items (`li margin-bottom: 2px`)
- **6px** — block-heading bottom margin
- **8-10px** — section-title border bottom padding, diagram-title bottom margin
- **12-14px** — content-block bottom margin, section-title margin-bottom, takeaway padding
- **16-22px** — page-body padding-top, page-header padding
- **40px** — page-body horizontal padding, two-col gap
- **70-100px** — cover-top horizontal padding, vertical margin

When in doubt: 8/12/16/24/40 are the safe spacing values.

## Bullet Style

- Bullets use the em-dash character `―` (NOT bullet •, NOT hyphen -)
- Bullet color: `#2563EB` (primary blue)
- Bullet positioning: `padding-left: 16px; position: relative;` with `::before { left: 0 }`
- Don't change the dash to anything else. The em-dash bullet is signature to this style.

## Inline Highlighting

Use sparingly — too much loses impact:

- `<span class="em">…</span>` inside `.action-title` → blue text (the emphasis word in the headline)
- `<span class="accent-em">…</span>` in body → blue, weight 500 (positive emphasis)
- `<span class="accent-warn">…</span>` in body → orange, weight 500 (risk/warning)
- `<strong>` → bold, inherits color (use for crucial nouns)

## Slide Composition Rule of Thumb

A typical slide has (**measured values**, 1-line action-title + 1-line lead-in):

1. **page-header** — **128px** (item-id + priority badge + action-title + lead-in)
2. **page-body** — **549px**; usable content area **519px** after its 14+12px padding
3. **page-footer** — **41px**

These three together must fit in 720px. The page-body is the only flexible region, and it is
`overflow:hidden` — anything past 519px is clipped without warning.

A two-line action-title (>53 full-width chars) moves this to 159 / 518 / 41.

## What This Style Is NOT

To preserve the look, avoid:
- Multiple bright accent colors (purple, green, etc.) — stick to blue + orange + red(diff)
- Heavy drop shadows on inner elements
- Rounded corners larger than 2px (`border-radius` is mostly 0 in this design)
- Background gradients
- Decorative emojis or icon fonts (this is a serious business document)
- Image backgrounds (everything is type and svg)
