# Layout

One slide. Widescreen 13.333 x 7.5 in by default; the 2004 original is 10 x 7.5.

## Quadrant positions

Scot Dietz's original spirals counter-clockwise from the bottom left: history
at the foot of the page, the climb above it. Do not rearrange this into a
normal reading grid.

```
+-------------------------------+-------------------------------+
| iv) Other ...                 | iii) Core Strategies          |
|     Things to Think About     |      Most Sig. Accomplishments|
|     Questions to Ponder       |      Most Sig. Shortfalls     |
|     Decisions to Make         |      How's it going building /|
|     Actions to Take           |        improving processes?   |
|   [Conference Call Topics]    |   [Core Strategies #1-#6]     |
+-------------------------------+-------------------------------+
|   KPI #1 ... #4               |   Year: Annual Plan           |
|   Status Update each          |   Theme:                      |
|                               |   SMART Goal #1 ... #4        |
| i) Key Performance Indicators | ii) Breakthrough Goals        |
+-------------------------------+-------------------------------+
```

**Headings sit on the outer edge of the page**, not at the top of each panel.
The top row is headed at the top, the bottom row at the bottom, with the
numerals pointing inward toward the center cross. The parenthetical descriptor
sits on the outer side of the title.

Quadrant iii order: accomplishments, shortfalls, the process question, then the
numbered strategies in a boxed strip at the foot.

## Label sets

`"labels": "classic"` gives the 2004 wording verbatim. The default is plain
English, which drops the jargon without touching the structure.

| | Classic | Plain |
|---|---|---|
| i | Key Performance Indicators / (Historic Performance Outcomes) | How We Did |
| ii | Breakthrough Goals / (Future Performance Outcomes) | This Year's Goals |
| iii | Core Strategies / (Which Best Drive Traction for Your Multi-year Journey) | How We Get There |
| iv | Other ... / (The Next Most Traction Creating "ions" of Your Journey) | What's On My Mind |

`"label_overrides"` replaces any single label for one report, which is how a
quadrant subtitle carries the basis, for example "September, costed on hours
actually worked".

## Variance colors

Green at or ahead of plan. Amber when the target was missed by 5% of its value
or less. Red when missed by more than 5%. A `stalled` flag on a goal or
strategy prints STUCK, and means no change for two months or more, computed by
diffing against `history/`.

## Content caps

The generator clamps to these. Write short rather than letting it truncate.

| Field | Characters |
|---|---|
| KPI status line | 84 |
| Goal theme | 44 |
| Goal bullet | 88 |
| Strategy | 40 |
| Accomplishment / shortfall | 58 |
| Process line | 86 |
| Quadrant iv item | 84 |
| Group topic | 30 |

Three items maximum for accomplishments and shortfalls, two per quadrant iv
block, six strategies, five KPIs (the original has four), four goals.

## Copyright

Keep the "© Sherpa Alliance, 2004" line in the footer. The format is used with
the author's permission; do not remove the credit.
