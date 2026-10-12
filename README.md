**English** | [Español](README.es.md)

# Linotipia de tokens

**How a language model works, told as an animated documentary.**

▶ **Watch it live:** https://alenj0x1.github.io/linotipia-de-tokens/

An imaginary machine, inspired by the Linotype that cast lines of hot lead to print newspapers, walks through the full journey of a large language model in six chapters: from raw data to an answer that uses tools. Every part of the machine stands for a real part of the process, and every number shown on screen (probabilities, losses, rewards, attention) is computed by the page itself.

> The on-screen narration and interface are in **Spanish**.

![Desktop view](docs/preview-escritorio.png)

## Chapters

| # | Chapter (Spanish title) | Question |
|---|-------------------------|----------|
| 1 | Data (*Datos*) | Where does everything a model knows come from? |
| 2 | Pretraining (*Preentrenar*) | How does a machine nobody gives rules to learn to write? |
| 3 | Fine-tuning (*Ajustar*) | How does it go from completing text to being a helpful, honest assistant? |
| 4 | Evaluation (*Evaluar*) | How do we know it is ready to ship? |
| 5 | Answering (*Responder*) | What happens inside when you write to it? |
| 6 | Tools (*Herramientas*) | How does it act beyond what it knows? |

A full playthrough lasts about 13½ minutes (about 14½ with the cover cards enabled).

## Usage

It is a single self-contained HTML page with no dependencies and no network access. Just open `index.html` in a browser.

- **Tap or click** on the machine: advance to the next step. **Double tap:** next chapter.
- **Keyboard:** `1`–`6` jump to a chapter; `→`, `Enter` or `Space` advance one step; `↓` or `Page Down` go to the next chapter and `←` to the previous one.
- **Controls:** previous/next chapter, play/pause, restart from the beginning, speed (0.5×, 1×, 2×) and switches for the camera that follows the active part, waiting for you to finish reading, synthesized sound, and cover cards.
- **The timeline** shows progress and lets you jump to any chapter.

### URL parameters

| Parameter | Effect |
|-----------|--------|
| `?stage=1` … `?stage=6` | Start directly at that chapter |
| `?portadas=1` | Show the prologue, chapter covers and epilogue |
| `?cam=0` | Fixed camera, no zooming in |

It honors `prefers-reduced-motion`: with reduced motion, each step is shown as a still image.

For technical details see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md). To contribute, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Repository layout

```
index.html          Final page, ready to publish (generated)
build.py            Builds index.html from src/
src/base.html       Base figure: isometric geometry, model and animation
src/doc.js          Documentary layer: covers, timeline, switches
src/doc.css         Styles: large-screen layout, controls, legend
src/controls.html   Controls markup
src/legend.html     Color code and cast of parts
docs/               Screenshots and technical documentation
```

`build.py` applies script corrections and the `src/` layers on top of `src/base.html`, and writes `index.html`. To regenerate the page after editing anything in `src/`:

```bash
python3 build.py
```

It only needs Python 3, no extra packages. Every substitution checks that the original text appears exactly once, so if you edit `src/base.html` and a substitution stops matching, the script stops and tells you which one.

## Publishing on GitHub Pages

The repository includes a workflow at `.github/workflows/pages.yml` that rebuilds and publishes the page on every push to `main` (it can also be run manually).

1. Create the repository on GitHub and push the content:
   ```bash
   git init
   git add .
   git commit -m "Linotipia de tokens"
   git branch -M main
   git remote add origin https://github.com/alenj0x1/linotipia-de-tokens.git
   git push -u origin main
   ```
2. In the repository, go to **Settings → Pages** and under **Source** choose **GitHub Actions**.
3. After the first push, the page is live at `https://alenj0x1.github.io/linotipia-de-tokens/`.

Since it is a single static file, it also works on Netlify, Vercel, Cloudflare Pages or any web server: just serve `index.html`.

## Honesty of the illustration

This is a deliberate simplification. Six trays stand for the dozens of layers of a transformer, and a single needle per token sums up the many attention heads working in parallel. Twelve slots stand for a context window that in a real model holds hundreds of thousands of tokens. Probabilities, losses and rewards are examples computed on the page with softmax. The figure shows how large language models work in general, not the internal architecture of any specific model.

## Credits and license

Built with the **anatomy** skill for isometric figures, whose drawing kit is bundled inside `index.html` and `src/base.html` under the MIT license (see `THIRD_PARTY_NOTICES.md`).

The rest of the project is distributed under the MIT license (see `LICENSE`).
