# SVG Diagram Patterns

The deck embeds inline SVG diagrams inside `.diagram` containers. These are the canonical
patterns extracted from v9. Use them as templates and adapt to your content.

## Container Setup

Always wrap SVG in this container:

```html
<div class="diagram">
  <div class="diagram-title">{{ENGLISH_LABEL}}</div>
  <svg viewBox="0 0 500 290" class="svg-diagram" preserveAspectRatio="xMidYMid meet">
    <!-- SVG content -->
  </svg>
</div>
```

The `viewBox` standard is `0 0 500 H` where H = height. Common heights:
- 150 — simple before/after or 2-step flow
- 180 — 3-stage vertical flow
- 230 — scope-breakdown box stacks
- 290 — hierarchy trees, full diagrams

## Color Convention for SVG

Match the design system:
- **Active/primary nodes**: `fill="#DBEAFE" stroke="#2563EB" stroke-width="1.5"` (or 2 for emphasis)
- **Secondary nodes**: `fill="#fff" stroke="#2563EB" stroke-width="1.5"`
- **Inactive/future nodes**: `fill="#F5F5F4" stroke="#9CA3AF" stroke-width="1" stroke-dasharray="4,3"`
- **Lines/connectors**: `stroke="#2563EB" stroke-width="1.2"` (active) or `stroke="#9CA3AF"` (inactive)
- **Text inside nodes**: `fill="#1A2538" font-weight="600"` for primary, `fill="#555"` for secondary
- **Sub-text/captions**: `font-size="9" fill="#555"` or `fill="#888"` for muted

## Pattern 1: Hierarchy Tree (3 levels, branching)

Use for org charts, store hierarchies, data hierarchies.

```html
<svg viewBox="0 0 500 290" class="svg-diagram" preserveAspectRatio="xMidYMid meet">
  <!-- Top -->
  <rect x="180" y="15" width="140" height="42" fill="#DBEAFE" stroke="#2563EB" stroke-width="1.5"/>
  <text x="250" y="35" text-anchor="middle" font-size="12" fill="#1A2538" font-weight="600">{{TOP_NAME}}</text>
  <text x="250" y="49" text-anchor="middle" font-size="9" fill="#555">{{TOP_NOTE}}</text>

  <!-- Branch lines from top -->
  <line x1="250" y1="57" x2="250" y2="80" stroke="#2563EB" stroke-width="1.2"/>
  <line x1="120" y1="80" x2="380" y2="80" stroke="#2563EB" stroke-width="1.2"/>
  <line x1="120" y1="80" x2="120" y2="100" stroke="#2563EB" stroke-width="1.2"/>
  <line x1="380" y1="80" x2="380" y2="100" stroke="#2563EB" stroke-width="1.2"/>

  <!-- Mid level (left) -->
  <rect x="50" y="100" width="140" height="42" fill="#fff" stroke="#2563EB" stroke-width="1.5"/>
  <text x="120" y="120" text-anchor="middle" font-size="11" fill="#1A2538" font-weight="600">{{MID_LEFT_NAME}}</text>
  <text x="120" y="134" text-anchor="middle" font-size="9" fill="#555">{{MID_LEFT_NOTE}}</text>

  <!-- Mid level (right) -->
  <rect x="310" y="100" width="140" height="42" fill="#fff" stroke="#2563EB" stroke-width="1.5"/>
  <text x="380" y="120" text-anchor="middle" font-size="11" fill="#1A2538" font-weight="600">{{MID_RIGHT_NAME}}</text>
  <text x="380" y="134" text-anchor="middle" font-size="9" fill="#555">{{MID_RIGHT_NOTE}}</text>

  <!-- Lower level under mid-left -->
  <line x1="120" y1="142" x2="120" y2="165" stroke="#2563EB" stroke-width="1.2"/>
  <rect x="50" y="165" width="140" height="42" fill="#fff" stroke="#2563EB" stroke-width="1.5"/>
  <text x="120" y="184" text-anchor="middle" font-size="11" fill="#1A2538" font-weight="600">{{LOW_NAME}}</text>
  <text x="120" y="198" text-anchor="middle" font-size="9" fill="#555">{{LOW_NOTE}}</text>

  <!-- Caption -->
  <line x1="30" y1="230" x2="470" y2="230" stroke="#D0D0D0" stroke-dasharray="3,3"/>
  <text x="250" y="250" text-anchor="middle" font-size="11" fill="#0F172A" font-weight="600">{{CAPTION_LINE_1}}</text>
  <text x="250" y="270" text-anchor="middle" font-size="10" fill="#555">{{CAPTION_LINE_2}}</text>
</svg>
```

## Pattern 2: Before / After (with arrow between)

Use for migrations, redesigns, changes.

```html
<svg viewBox="0 0 500 150" class="svg-diagram" preserveAspectRatio="xMidYMid meet">
  <!-- Before (left, gray) -->
  <rect x="10" y="20" width="200" height="110" fill="#F5F5F4" stroke="#9CA3AF" stroke-width="1"/>
  <text x="110" y="40" text-anchor="middle" font-size="11" fill="#555" font-weight="600">{{BEFORE_LABEL}}</text>
  <rect x="40" y="55" width="140" height="25" fill="#fff" stroke="#9CA3AF" stroke-width="1"/>
  <text x="110" y="72" text-anchor="middle" font-size="10" fill="#555">{{BEFORE_NAME}}</text>
  <text x="110" y="100" text-anchor="middle" font-size="9" fill="#888">{{BEFORE_NOTE_1}}</text>
  <text x="110" y="115" text-anchor="middle" font-size="9" fill="#888">{{BEFORE_NOTE_2}}</text>

  <!-- Arrow -->
  <line x1="215" y1="75" x2="280" y2="75" stroke="#2563EB" stroke-width="2" marker-end="url(#arr-1)"/>
  <text x="247" y="68" text-anchor="middle" font-size="10" fill="#2563EB" font-weight="600">{{ARROW_LABEL}}</text>

  <!-- After (right, blue) -->
  <rect x="285" y="20" width="200" height="110" fill="#DBEAFE" stroke="#2563EB" stroke-width="2"/>
  <text x="385" y="40" text-anchor="middle" font-size="11" fill="#1A2538" font-weight="700">{{AFTER_LABEL}}</text>
  <rect x="305" y="55" width="160" height="22" fill="#fff" stroke="#2563EB" stroke-width="1"/>
  <text x="385" y="70" text-anchor="middle" font-size="10" fill="#1A2538">{{AFTER_NAME}}</text>
  <text x="385" y="93" text-anchor="middle" font-size="9" fill="#2563EB">{{AFTER_NOTE_1}}</text>
  <text x="385" y="108" text-anchor="middle" font-size="9" fill="#2563EB">{{AFTER_NOTE_2}}</text>
  <text x="385" y="123" text-anchor="middle" font-size="9" fill="#2563EB">{{AFTER_NOTE_3}}</text>

  <defs>
    <marker id="arr-1" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#2563EB"/>
    </marker>
  </defs>
</svg>
```

NOTE: Each diagram needs a unique marker id. If you have multiple diagrams on the same slide
(or across the deck), use `arr-2`, `arr-3`, etc. to avoid conflicts.

## Pattern 3: Scope Stack (vertical priority/scope boxes)

Use to show what's in scope vs. out of scope, or priority tiers.

```html
<svg viewBox="0 0 500 230" class="svg-diagram" preserveAspectRatio="xMidYMid meet">
  <!-- Tier 1 (deep blue, primary scope) -->
  <rect x="20" y="15" width="460" height="55" fill="#DBEAFE" stroke="#2563EB" stroke-width="2"/>
  <text x="40" y="38" font-size="11" fill="#1A2538" font-weight="700">{{TIER1_TITLE}}</text>
  <text x="40" y="55" font-size="9" fill="#2563EB">{{TIER1_NOTE}}</text>

  <!-- Tier 2 (light blue, secondary) -->
  <rect x="20" y="85" width="460" height="55" fill="#EFF6FF" stroke="#2563EB" stroke-width="1.5"/>
  <text x="40" y="108" font-size="11" fill="#1A2538" font-weight="600">{{TIER2_TITLE}}</text>
  <text x="40" y="125" font-size="9" fill="#555">{{TIER2_NOTE}}</text>

  <!-- Tier 3 (gray dashed, out of scope) -->
  <rect x="20" y="155" width="460" height="55" fill="#F5F5F4" stroke="#9CA3AF" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="40" y="178" font-size="11" fill="#555" font-weight="600">{{TIER3_TITLE}}</text>
  <text x="40" y="195" font-size="9" fill="#888">{{TIER3_NOTE}}</text>
</svg>
```

## Pattern 4: Sequential Flow (horizontal steps)

Use for process flows, pipelines, sequences.

Adapt Pattern 2 by chaining multiple before-style boxes with arrows between them. Reduce
each box width to fit 3-4 boxes in 500px viewBox.

## Pattern 5: Current vs. Future (with timeline)

Use for "this slice now, this other slice later" type diagrams.

```html
<svg viewBox="0 0 500 180" class="svg-diagram" preserveAspectRatio="xMidYMid meet">
  <!-- Current scope (full color) -->
  <rect x="20" y="20" width="460" height="50" fill="#DBEAFE" stroke="#2563EB" stroke-width="2"/>
  <text x="40" y="42" font-size="11" fill="#1A2538" font-weight="700">{{CURRENT_LABEL}}</text>
  <text x="40" y="58" font-size="9" fill="#555">{{CURRENT_NOTE}}</text>

  <!-- Down arrow with "future" annotation -->
  <line x1="250" y1="75" x2="250" y2="100" stroke="#9CA3AF" stroke-width="1.5"
        marker-end="url(#arr-future)" stroke-dasharray="4,3"/>
  <text x="260" y="92" font-size="9" fill="#9CA3AF">将来</text>

  <!-- Future scope (dashed gray) -->
  <rect x="20" y="105" width="460" height="50" fill="#F5F5F4" stroke="#9CA3AF" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="40" y="127" font-size="11" fill="#555" font-weight="600">{{FUTURE_LABEL}}</text>
  <text x="40" y="143" font-size="9" fill="#888">{{FUTURE_NOTE}}</text>

  <defs>
    <marker id="arr-future" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#9CA3AF"/>
    </marker>
  </defs>
</svg>
```

## SVG Sizing Tips

- All `text` elements should have `text-anchor="middle"` if centered, default if left-aligned
- Box height should be ~40-55px to fit two text lines comfortably
- Font sizes inside SVG: 12px (labels in active boxes), 11px (titles), 10px (secondary), 9px (notes/captions)
- Always use `preserveAspectRatio="xMidYMid meet"` so the diagram scales correctly
- Avoid excessive node counts. If you need >8 nodes, you're probably overloading one diagram
  — split it across two slides.

## Diagram Title (the small uppercase label above the SVG)

This is the `.diagram-title` text — short, English, all-caps.

Examples:
- `STORE HIERARCHY`
- `INFRA MIGRATION`
- `SCOPE BREAKDOWN`
- `FUTURE SDK`
- `AUTH FLOW`
- `DATA PIPELINE`
- `MIGRATION PATH`

Keep these to 1-3 words. They function as section labels for the visual.
