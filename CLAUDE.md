# Lemon-Checklists: working rules and house style

Source: https://github.com/Hellreaver/Lemon-Checklists (its `CLAUDE.md` and `style-guide.json`).
Site: https://hellreaver.github.io/Lemon-Checklists/
Apply these rules whenever building or editing a Lemon procedure guide.

## Functional rules (workflow)

- Guides are procedure checklists built from the **Lemon manuals MCP server** (`mcp__Lemon_Manuals__*`: browse, find, read_page, get_image). One self-contained HTML file per job under `guides/`, named `<make>-<model>-<engine>-<job>.html` (e.g. `volvo-940-b230fd-head-gasket.html`).
- Follow `style-guide.json` for colors, type and components. `guides/volvo-940-b230fd-head-gasket.html` is the reference page; copy its structure, CSS and script.
- **Confirm the exact year, model and engine code before writing.** Pull every spec from that vehicle's book, never from memory or a similar vehicle.
- **Figures:** put the manual's own figures in wherever a step, sequence or spec table has one (bolt orders, timing marks, exploded views, scanned torque tables).
  - Fetch with MCP `get_image`. It shows the image to Claude but writes no file.
  - Save with `python3 tools/save-figures.py <guide-name> ID=name ...` (ID is the last segment of the image path, e.g. `364989686` from `/images/IMP68Q313/euro650/364989686/`; name has no extension). It pulls the image out of this session's transcript into `guides/img/<guide-name>/`.
  - Never download figures from the public LEMON site or any mirror; the container blocks it, and the connector is the source.
  - Link figures with relative paths.
- List every new guide in `index.html` and `README.md` (README format: `- [<year> <make> <model> <engine> <job>](https://hellreaver.github.io/Lemon-Checklists/guides/<file>.html) (\`guides/<file>.html\`)`).
- The first link in every guide's jump nav is the `&larr; All guides` chip (`<a href="../index.html">&larr; All guides</a>`).
- Push straight to `main` (GitHub Pages serves from it). **No attribution lines in commits** for that repo.
- The repo is public: keep local paths, host names, ports and personal details out of committed files.

## Style guide ("Lemon house style")

Always dark; no light theme. Mobile first, 720px max content width, safe-area insets. Warm near-black background, muted teal accent, amber and brick-red for status. **Use only these tokens; no new colors.**

```css
:root{
  --bg:#1B1917; --card:#232019; --text:#ECE8E0; --muted:#B6AFA0;
  --line:#3A362F; --field:#1B1917;
  --accent:#7BAFA9; --accent-soft:#243B37; --accent-ink:#BFE0DA; --on-accent:#13201E;
  --good:#7BAFA9; --good-bg:#243B37;
  --warn:#D9A95B; --warn-bg:#3A2F1C;
  --bad:#D97A7A; --bad-bg:#3B2323;
  --idle-bg:#2C2923; --track:#3A362F; --plate:#FFFFFF;
  color-scheme: dark;
}
html, body { margin:0; background:var(--bg); color:var(--text); font:16px/1.4 "Barlow", system-ui, Arial, sans-serif; }
h1, h2, h3, .eyebrow { font-family:"Barlow Condensed","Arial Narrow",sans-serif; }
.mono, .num { font-family:"IBM Plex Mono", ui-monospace, monospace; font-variant-numeric:tabular-nums; }
```

Token uses: `bg` page/topbar/theme-color; `card` cards, tab bar, default button; `text` primary; `muted` labels, secondary, table heads; `line` borders/dividers; `accent` primary buttons, active tab, focus ring, links, eyebrow, progress fill; `accent-soft` note callouts, torque chips, selected row; `accent-ink` headings, big numbers, title, text on accent-soft; `on-accent` text on accent buttons; `warn`/`warn-bg` cautions; `bad`/`bad-bg` warnings, hard limits, danger; `idle-bg` neutral chips, inline code, unhighlighted sequence cells; `track` progress track.

Status chips: thrive = good/good-bg, survive = warn/warn-bg, behind = bad/bad-bg, idle = muted/idle-bg.

**Fonts** (Google Fonts): `https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700&family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap`
- Body: Barlow 16px / 1.4.
- Display (h1–h3, eyebrow, tabs, jump nav): Barlow Condensed 600/700.
- Mono (**every number**: specs, chips, counts, number inputs): IBM Plex Mono, tabular-nums.
- Inputs are 16px so iOS Safari doesn't zoom.

**Type scale:** hint 11px muted · table head 11px uppercase .05em muted · small 12px · eyebrow 12px uppercase .1em 700 accent · chip 12px 600 mono · label 13px muted · row 14px · tab 15px uppercase .06em · input 16px · h3 17px accent-ink · h2 20px accent-ink (guide section h2 is 26px) · stat value 22px 600 mono · h1 24px accent-ink .01em · big number 34px 600 mono lh 1.1 accent-ink.

**Radius:** bar 5 · row 6 · control 8 · card 10 · pill 999. **Spacing:** page 12px, card padding 14px, card gap 12px, inputs 10px, buttons 12px 14px, rows 9px 0. Breakpoint: ≤340px collapses 3-col grids to 2.

**Components:** card (card bg, 1px line, r10, p14, mb12); live card adds 5px accent left border; button (r8, 1px line, card bg), primary (accent bg/border, on-accent text, 700), ghost (transparent), danger (bad text, bad-bg border), disabled opacity .6; input (field bg, 1px line, r8, p10, focus 2px accent outline offset -1px); chip (pill, 3px 9px, 12px 600 mono); progress bar (10px, r5, track, accent fill); info panel (13px, 8px 10px, r8, accent-soft/accent-ink; warn variant warn-bg/warn); toast (bottom-center, accent-ink bg, bg text, 14px 600, r8, opacity .2s fade).

**Color rules:**
- Notes use accent-soft/accent, cautions warn, hard limits bad. No separate blue note color or olive accent.
- Body text on any tint stays `text`; tags on accent-soft use accent-ink, not accent.
- Checked contrast pairs all pass AA (text/warn-bg 10.7, accent-ink/accent-soft 8.5, accent/bg 7.1, muted/card 7.5, bad/bad-bg 4.8).
- A done step keeps its colors and drops to opacity .62. Never grey it to muted, or the torque chips lose contrast.

## Guide page anatomy (match the reference page)

- `<head>`: viewport with `viewport-fit=cover`, `theme-color #1B1917`, a short `<title>` (e.g. "940 Head Gasket"), font preconnects + stylesheet, inline `<style>` starting with the token block.
- **Topbar** (`header.topbar > .topbar-inner`): sticky, bg, 3px accent bottom border. `p.eyebrow` (year, model, body · engine code/displacement · "from the shop manual"), `h1`, then `.progress` (`.bar > i#fill` + mono `span.count#count` "n / total").
- **Jump nav** (`nav.jump`): horizontal-scroll row of chips (card fill, 1px line, r8, 15px Barlow Condensed uppercase, muted; hover/focus accent). First chip is `← All guides` → `../index.html`, then `#section` anchors.
- **Sections** (`section#id`): `h2` 26px accent-ink, `div.rule` (40×3px accent), `p.sub` (muted 15px one-liner).
- **Steps**: `ol.steps > li.step`. Card fill, 1px line, 5px line-coloured left border, r10, padding 12px 14px. The script injects a mono numbered pill (`span.n`), restarting per list. Tapping or Space/Enter toggles `.done` (good left border, good-bg pill, opacity .62), with `role=checkbox` and `aria-checked`. State lives in localStorage only, under a KEY equal to the guide filename. A reset button clears it. Clicks inside `.fig` don't toggle.
- **Torque chip** (`span.torq`): inline mono 600, accent-ink on accent-soft, r6, `white-space:nowrap`. Use it for every number the reader sets a tool to.
- **Callouts** (`div.callout.c-warn|c-note|c-bad` with a `span.tag`), each with a 4px left border:
  - warn: warn-bg fill, warn tag. For manual cautions and "check your engine" notices.
  - note: accent-soft fill, accent-ink tag. For context and side notes.
  - bad: bad-bg fill, bad tag. For manual warnings and scrap/replace limits.
- **Spec table** (`div.tablewrap > table`): card fill in a 1px line, r10. Head is Barlow Condensed uppercase muted. First column Barlow, spec column mono tabular. Qualifiers go in `<em>` as 12px muted on their own line.
- **Figure** (`figure.fig > a.plate[href=img] > img` + `figcaption`): manual scan on a white `--plate` block, r8, padding 8px. The img has max-width 100%, explicit width/height, `loading="lazy"` and descriptive alt text, and links to the full-size file. The 12px muted caption names the manual figure ("Manual figure: …"). The figure sits inside the step it illustrates.
- **Sequence diagram** (`div.seq > figure > figcaption + div.grid5 > span…`): 5-column grid of mono pills on idle-bg, first bolt `span.first` on accent-soft/accent-ink, dashed outline. Orientation matches the manual figure; add a hint "Laid out as drawn in the manual figure." plus the manual scan beneath.
- **Footer** (`p.foot`): 13px muted, 1px line top border. Names the LEMON manual year, model, engine (full engine designation) and every manual section used, and notes that figures are the manual's own scans.
- Usual section flow for a repair: scope → confirm/diagnose → removal → clean & inspect → install → finish → torque/spec summary table.
