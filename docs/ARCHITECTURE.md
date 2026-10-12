[English](ARCHITECTURE.md) | [Español](ARQUITECTURA.md)

# Architecture

Linotipia de tokens is one static, self-contained `index.html` (no dependencies, no network). It is **generated** by `build.py` from the sources in `src/`. Never edit `index.html` by hand: it is overwritten on every build.

## Source layers

| File | Role |
|------|------|
| `src/base.html` | Base figure (~670 KB): isometric camera and solids, SVG rendering, the machine model, the six chapters' beats, narration, animation loop, keyboard/tap handling, sound, URL params `stage` and `cam`. Includes the MIT-licensed anatomy kit (see `THIRD_PARTY_NOTICES.md`). |
| `src/doc.js` | Documentary layer: `CHAPTERS` data (title, question, intro, "what to look at", recap), prologue/chapter covers/epilogue, timeline and clock, switch helpers (`swSet`, `setPlay`), and hooks `docInit`, `docStart`, `docTick`, `docEnd`. Reads the `portadas` URL param. |
| `src/doc.css` | Styles appended at the end of the base `<style>`: large-screen layout, controls, cover cards, legend. |
| `src/controls.html` | Markup of the control bar (transport, speed, switches, timeline). Replaces the base `.lino-ctl` block. |
| `src/legend.html` | Color code and cast of parts. Replaces the base `<figcaption class="iso-legend">`. |

## How `build.py` works

1. Reads `src/base.html` into memory.
2. Applies a sequence of `rep(old, new)` substitutions. Each one **asserts the old text appears exactly once** (or `count` times); otherwise the build fails with `AssertionError: (n, <first 90 chars>)`.
3. Substitutions are grouped as:
   - **Script fixes**: narration wording and precision (e.g. learning rate, temperature, KV cache, end-of-turn token, residual connection).
   - **Loop hooks**: calls `docTick(dt)` each frame, `docStart(...)` when a stage starts, `docEnd()` when it ends, `docInit()` at startup; with no `?stage`, starts at chapter 1 with the prologue flag set.
   - **JS injection**: inserts the contents of `src/doc.js` before `window.__linoDurations`, and rewires the original button labels to the new switch helpers.
   - **HTML**: adds the cover card, replaces the controls with `src/controls.html`, hides the old stage nav and summary, replaces the legend with `src/legend.html`.
   - **CSS**: appends `src/doc.css` before the first `</style>`.
4. Writes `index.html` and prints `ok <length>`.

## Editing and extending

- Change styles, controls markup, legend or documentary text: edit the matching `src/` file and run `python3 build.py`.
- Editing `src/base.html`: if you change text targeted by a `rep(...)` in `build.py`, update that call too; the assertion will point to it.
- Add a fix: append a `rep("exact original", "replacement")` in `build.py`. Keep `old` unique in the file.
- Element hooks use `data-*` attributes (e.g. `data-doc-next`, `data-pause`, `data-speed`, `data-cam`, `data-pace`, `data-sound`, `data-covers`, `data-doc-tl`); keep them when editing markup.

## Controls

- Tap/click on the machine: next step; double tap: next chapter.
- Keys: `1`–`6` chapter; `→` / `Enter` / `Space` next step; `↓` / `Page Down` next chapter; `←` previous chapter.
- Bar: previous chapter, play/pause, next chapter, restart from the beginning, speed 0.5× / 1× / 2×, switches (follow camera, wait for reading, sound, covers), clickable chapter timeline.

## URL parameters

| Parameter | Source | Effect |
|-----------|--------|--------|
| `stage=1..6` | `base.html` | Start at that chapter |
| `cam=0` | `base.html` | Fixed camera |
| `portadas=1` | `doc.js` | Prologue, chapter covers and epilogue |

## Accessibility

- `prefers-reduced-motion: reduce` (`matchMedia` in `base.html`): steps are fast-forwarded and shown as still images, the animation frame loop doesn't run, and CSS flow/pulse animations are disabled.
- Switches use `role="switch"` + `aria-checked`; play/pause uses `aria-pressed` and an updated `aria-label`; icon buttons have `aria-label`/`title`; the cover card is an `aria-live="polite"` region; groups carry `aria-label`.
- Sound is off by default.

## Deploy

`.github/workflows/pages.yml` runs on push to `main` or manually: sets up Python 3.12, runs `python3 build.py`, copies `index.html` into `_site/` with `.nojekyll`, and deploys with `actions/deploy-pages`. Enable **Settings → Pages → Source: GitHub Actions**. Live: https://alenj0x1.github.io/linotipia-de-tokens/

Any static host works: serve `index.html`.
