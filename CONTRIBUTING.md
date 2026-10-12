# Contributing / Contribuir

## English

Thanks for your interest!

1. Edit files in `src/` (or `build.py`), never `index.html` directly. See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).
2. Run `python3 build.py` (Python 3 only, no packages). It must print `ok <length>`; a failed assertion means a `rep(...)` no longer matches exactly once.
3. Open `index.html` in a browser and check the chapters you touched, including with reduced motion.
4. Commit both `src/` changes and the regenerated `index.html`, then open a pull request describing the change.

Keep the page self-contained (no external requests or dependencies). The on-screen text is in Spanish; keep the illustration honest about what it simplifies. Contributions are licensed under MIT (see `LICENSE`).

## Español

¡Gracias por tu interés!

1. Edita los archivos de `src/` (o `build.py`), nunca `index.html` directamente. Consulta [docs/ARQUITECTURA.md](docs/ARQUITECTURA.md).
2. Ejecuta `python3 build.py` (solo Python 3, sin paquetes). Debe imprimir `ok <longitud>`; si falla una aserción, algún `rep(...)` ya no coincide exactamente una vez.
3. Abre `index.html` en un navegador y revisa los capítulos que tocaste, también con movimiento reducido.
4. Incluye en el commit los cambios de `src/` y el `index.html` regenerado, y abre un pull request describiendo el cambio.

Mantén la página autocontenida (sin peticiones ni dependencias externas). El texto en pantalla está en español; la ilustración debe seguir siendo honesta con lo que simplifica. Las contribuciones se publican bajo licencia MIT (ver `LICENSE`).
