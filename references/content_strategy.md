# Content Strategy: Source Material → Deck Structure

The hardest part of producing this deck is NOT styling — it's deciding what goes on which slide.
Bad content structure looks bad regardless of design. This reference walks through how to map
typical source materials (meeting minutes, requirements docs, Excel tables) into the deck pattern.

## The "Per-Topic" Structure

The deck's signature pattern is **one major topic = 5-6 slides** in this exact order:

1. **サマリー / Summary** — the topic on one slide (goal, premise, scope) with a takeaway
2. **詳細要件 (1/N) / Detail** — broken into 課題 → 対策 per requirement
3. **詳細要件 (2/N) / Detail** — continuation if needed
4. **実装方針・リスク / Policy + Risks** — table with 仕様 rows + リスク rows
5. **確認事項 / Confirmation** — table of questions for stakeholders

A single deck typically has:
- 1 cover slide
- N topics × 5-6 slides each
- Optional section dividers between topics (skip for shorter decks)

So 5 topics = 1 + 5×5 + 4 = 30 slides typical.

## Reading Source Material

When given meeting minutes, requirements docs, or Excel data, identify these elements:

### From meeting minutes
- **Decisions made** → action-titles (one per topic)
- **Background/context** → lead-in lines
- **Open questions** → 確認事項 slide content
- **Risks/concerns mentioned** → 実装方針・リスク table risk rows
- **Specific spec items** → 仕様 table rows
- **Diagrams drawn or described** → SVG diagrams

### From requirements / spec docs
- **Section headings** → topic groupings (one topic per major heading)
- **Requirement statements ("〜を可能にする", "〜が必要")** → action-titles
- **Background sections** → lead-in or 課題 block
- **Constraints / non-functionals** → リスク rows or 仕様 rows
- **TODOs / 検討事項** → 確認事項 slide

### From Excel tables / spreadsheets
- **Column headers** → table th in 実装方針・リスク slide
- **Row groupings** → 仕様 vs リスク rowspan groups
- **Status / priority columns** → priority badge on slide header, priority cell in confirmation table
- **Issue + 現状 + 対策 + 評価 columns** → typical structure for two-col detail slides

## Writing the Action-Title (the headline of each slide)

This is the most important sentence on the slide. It should be **one specific, declarative
sentence stating what will be done or decided**, with the most important phrase wrapped in
`<span class="em">`.

### Good action-titles
- 「店舗単位でのクーポン配布を可能にする<span class="em">独自のクーポン機能</span>を新規開発し、マルチテナント化後も継続利用可能な設計とする」
- 「インフラは<span class="em">Lambda中心構成 → ECS Fargate 等</span>に再設計し、将来のSDK化を見据えたアーキテクチャとする」
- 「5つの領域で仕様を改修 ― 最大のリスクは<span class="em">既存データの移行設計</span>と<span class="em">サテライト店舗の特殊仕様</span>」

### Bad action-titles (avoid)
- 「クーポン機能について」 — too vague, no decision/action
- 「新しいクーポン機能を作ります」 — too informal, lacks specificity
- 「店舗単位クーポンの仕様、データ構造、CMS変更、アプリ変更、バッチ処理について整理する」 — too many things; pick one

### Pattern templates
- "〜を可能にする<em>Xを新規開発</em>し、〜とする"
- "<em>X → Y</em>に再設計し、〜を実現する"
- "<N>つの領域で改修 ― 最大のリスクは<em>X</em>"
- "<N>領域<M>項目について、<em>クライアント名</em>に方針確認をお願いしたい"

### Action-title length (measured)

The action-title is 22px / line-height 1.4 across 1200px. **Up to 53 full-width chars it stays on
one line; at 54 it wraps to two**, which grows the header from 128px to 159px and shrinks the body
from 549px to 518px. A two-line title costs you roughly one table row. Keep titles ≤53 chars unless
you have budgeted the space.

## Writing the Lead-In (small gray text under the title)

One sentence (~50-80 chars). Provides the *why* or *context* the action-title doesn't have.
Should answer "why is this slide important now?" without repeating the title.

### Good lead-ins
- 「A社は『マルチテナント化の第1テナント』ではなく『既存拠点のもう一拠点』として扱う方針。」
- 「現行の『全店舗共通配布』から『店舗単位判定』への拡張。」
- 「CMS・アプリ・バッチの3系統に変更が影響する。既存全店舗共通クーポンの移行方針が鍵。」

## Density Rules (CRITICAL — must fit 720px)

The fixed slide height is unforgiving. Here's what fits:

### Two-column detail slide
- Each column: **2-3 content-blocks** OR **1 takeaway + 1-2 content-blocks**
- Each content-block: **2-5 bullets** (1 line each ideally, 2 lines max)
- Total bullets per slide: roughly **6-10**
- If you have more, split into 詳細要件 (2/N)

### Table slide
Count **total cell-lines**, not rows — the two limits below cannot both be maxed out.
Measured against the real 549px body (1-line action-title):

| Rows × lines/cell | Table height | Fits? |
|---|---|---|
| 12 rows × 1 line | 476px | yes |
| 14 rows × 1 line | 550px | **no — 3 cells clipped** |
| 10 rows × 2 lines | 600px | **no — 5 cells clipped** |
| 12 rows × 2 lines | 714px | **no — 9 cells clipped** |
| 8 rows × 3 lines | 487px | yes |

- Safe rule: **total cell-lines ≤ 13** (12 rows if 1-line cells, 8 rows if 2-3 line cells)
- Same conversion applies to the questions slide (12 questions × 1 line fits; 10 × 3 lines clips 8 cells)
- More content → split into multiple table slides

### Confirmation slide
- **5-8 questions max**
- Each question: 1-2 lines

### Summary slide
- Left column: 2 content-blocks + 1 takeaway
- Right column: 1 diagram (SVG ~290px tall) OR 2 content-blocks

## Splitting Logic: When to make a new slide

Make a new slide when **any** of these happen:
- Total content overflows 720px. **You will NOT see a scrollbar** — `.slide` and `.page-body`
  are `overflow:hidden`, so the excess is silently clipped and the bottom rows simply vanish.
  Detect it by measuring `.page-body` (`scrollHeight > clientHeight`) or by looking at the render.
- A single topic has more than 5 distinct sub-points
- You're forced to make font size smaller than the design system specifies
- The lead-in starts having to summarize multiple disconnected points

It's better to have **N+1 slides where each is breathable** than N slides where each is cramped.

## Topic Ordering in Multi-Topic Decks

When the source covers multiple work items (like v9 with NO.22, NO.1, NO.2, NO.3...):

1. **Order by priority/dependency**, not by ID number
2. Items with "必須" priority before "高" before "中" before "低"
3. Foundation/blocker items before items that depend on them
4. Within same priority: shortest topic first (helps reader gain momentum)

## Adding "Diff" Markers for Updates

When the deck is updated after a meeting and you want to flag what's new:

```html
<!-- Inline in a list -->
<li>
  ★ <span class="diff-tag">5/12 追加</span>
  <span class="diff-new"><strong>移行戦略</strong>: 新環境を完全に別環境として構築…</span>
</li>

<!-- Highlighting a whole row -->
<tr class="diff-row">
  <td class="row-label diff-cell">★ 特設店舗の扱い</td>
  <td class="diff-cell">★ 特設店舗向けクーポンは本フェーズでは対象外…</td>
</tr>

<!-- Standalone callout -->
<div class="diff-new" style="margin-top:8px; padding:8px 10px; background:#FEF2F2;
     border-left:3px solid #DC2626; font-size:11px; line-height:1.6;">
  ★ <span class="diff-tag">5/12 追加</span>
  <strong>追加の論点</strong>: ………
</div>
```

Use `★` as a visual anchor for added items so they're easy to spot.

## Footer Convention

The footer-left text should be **identical across the entire deck**, e.g.
`PROJECT NAME / SYSTEM REQUIREMENTS`.

The footer-right should be `P.<sequential page number>` starting from `P.1` for the cover
(or `P.2` if you skip numbering the cover).
