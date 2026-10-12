[English](ARCHITECTURE.md) | [Español](ARQUITECTURA.md)

# Arquitectura

Linotipia de tokens es un único `index.html` estático y autocontenido (sin dependencias ni red). Lo **genera** `build.py` a partir de las fuentes de `src/`. No edites `index.html` a mano: se sobrescribe en cada construcción.

## Capas de las fuentes

| Archivo | Función |
|---------|---------|
| `src/base.html` | Figura base (~670 KB): cámara y sólidos isométricos, renderizado SVG, modelo de la máquina, pasos de los seis capítulos, narración, bucle de animación, teclado y toques, sonido, parámetros `stage` y `cam`. Incluye el kit anatomy con licencia MIT (ver `THIRD_PARTY_NOTICES.md`). |
| `src/doc.js` | Capa documental: datos de `CHAPTERS` (título, pregunta, introducción, «qué mirar», resumen), prólogo, portadas y epílogo, línea de tiempo y reloj, ayudantes de interruptores (`swSet`, `setPlay`) y los ganchos `docInit`, `docStart`, `docTick`, `docEnd`. Lee el parámetro `portadas`. |
| `src/doc.css` | Estilos que se añaden al final del `<style>` base: diseño en pantallas grandes, controles, portadas, leyenda. |
| `src/controls.html` | Marcado de la barra de controles (transporte, velocidad, interruptores, línea de tiempo). Sustituye el bloque `.lino-ctl` de la base. |
| `src/legend.html` | Código de color y reparto de piezas. Sustituye el `<figcaption class="iso-legend">` de la base. |

## Cómo funciona `build.py`

1. Lee `src/base.html` en memoria.
2. Aplica una serie de sustituciones `rep(viejo, nuevo)`. Cada una **comprueba que el texto original aparece exactamente una vez** (o `count` veces); si no, falla con `AssertionError: (n, <primeros 90 caracteres>)`.
3. Grupos de sustituciones:
   - **Guion**: redacción y precisión de la narración (tasa de aprendizaje, temperatura, caché KV, token de fin de turno, conexión residual…).
   - **Ganchos del bucle**: llama a `docTick(dt)` en cada fotograma, `docStart(...)` al empezar un capítulo, `docEnd()` al terminar y `docInit()` al arrancar; sin `?stage`, empieza en el capítulo 1 con el prólogo marcado.
   - **Inyección de JS**: inserta `src/doc.js` antes de `window.__linoDurations` y adapta los botones originales a los nuevos interruptores.
   - **HTML**: añade la tarjeta de portada, sustituye los controles por `src/controls.html`, oculta la antigua navegación y el resumen, y sustituye la leyenda por `src/legend.html`.
   - **CSS**: añade `src/doc.css` antes del primer `</style>`.
4. Escribe `index.html` e imprime `ok <longitud>`.

## Editar y ampliar

- Estilos, controles, leyenda o textos documentales: edita el archivo de `src/` correspondiente y ejecuta `python3 build.py`.
- Si editas en `src/base.html` un texto al que apunta un `rep(...)`, actualiza también esa llamada; la aserción te dirá cuál.
- Nueva corrección: añade `rep("original exacto", "sustituto")` en `build.py`, con un original único.
- Los elementos se enlazan por atributos `data-*` (`data-doc-next`, `data-pause`, `data-speed`, `data-cam`, `data-pace`, `data-sound`, `data-covers`, `data-doc-tl`…); consérvalos al editar el marcado.

## Controles

- Toque o clic en la máquina: siguiente paso; doble toque: siguiente capítulo.
- Teclas: `1`–`6` capítulo; `→` / `Enter` / `Espacio` siguiente paso; `↓` / `Av Pág` siguiente capítulo; `←` capítulo anterior.
- Barra: capítulo anterior, reproducir/pausa, capítulo siguiente, ver desde el inicio, velocidad 0,5× / 1× / 2×, interruptores (cámara que sigue, esperar a la lectura, sonido, portadas) y línea de tiempo con los capítulos.

## Parámetros de URL

| Parámetro | Origen | Efecto |
|-----------|--------|--------|
| `stage=1..6` | `base.html` | Empieza en ese capítulo |
| `cam=0` | `base.html` | Cámara fija |
| `portadas=1` | `doc.js` | Prólogo, portadas y epílogo |

## Accesibilidad

- `prefers-reduced-motion: reduce` (`matchMedia` en `base.html`): los pasos se adelantan y se muestran como imagen fija, no corre el bucle de animación y se desactivan las animaciones CSS de flujo y pulso.
- Los interruptores usan `role="switch"` + `aria-checked`; reproducir/pausa usa `aria-pressed` y actualiza su `aria-label`; los botones de icono tienen `aria-label`/`title`; la portada es una región `aria-live="polite"`; los grupos llevan `aria-label`.
- El sonido está desactivado por defecto.

## Publicación

`.github/workflows/pages.yml` se ejecuta con cada envío a `main` o a mano: prepara Python 3.12, ejecuta `python3 build.py`, copia `index.html` a `_site/` con `.nojekyll` y publica con `actions/deploy-pages`. Activa **Settings → Pages → Source: GitHub Actions**. En línea: https://alenj0x1.github.io/linotipia-de-tokens/

Sirve cualquier alojamiento estático: basta con servir `index.html`.
