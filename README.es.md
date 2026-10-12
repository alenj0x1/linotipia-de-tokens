[English](README.md) | **Español**

# Linotipia de tokens

**Cómo funciona un modelo de lenguaje, contado como un documental animado.**

▶ **Verlo en línea:** https://alenj0x1.github.io/linotipia-de-tokens/

Una máquina imaginaria, inspirada en la linotipia que fundía líneas de plomo para imprimir periódicos, recorre en seis capítulos el viaje completo de un gran modelo de lenguaje: de los datos en bruto a una respuesta que usa herramientas. Cada pieza de la máquina representa una parte real del proceso, y cada número que aparece en pantalla (probabilidades, pérdidas, recompensas, atención) se calcula en la propia página.

![Vista en escritorio](docs/preview-escritorio.png)

## Capítulos

| # | Capítulo | Pregunta |
|---|----------|----------|
| 1 | Datos | ¿De dónde sale todo lo que sabe un modelo? |
| 2 | Preentrenar | ¿Cómo aprende a escribir una máquina a la que nadie le da reglas? |
| 3 | Ajustar | ¿Cómo pasa de completar texto a ser un asistente útil y honesto? |
| 4 | Evaluar | ¿Cómo se sabe que está listo para salir? |
| 5 | Responder | ¿Qué ocurre dentro cuando le escribes? |
| 6 | Herramientas | ¿Cómo actúa más allá de lo que sabe? |

La reproducción completa dura unos 13 minutos y medio (unos 14 y medio con las portadas activadas).

## Uso

Es una sola página HTML autocontenida, sin dependencias ni red. Basta con abrir `index.html` en un navegador.

- **Toque o clic** sobre la máquina: avanza al siguiente paso. **Doble toque:** siguiente capítulo.
- **Teclado:** `1`–`6` saltan a un capítulo; `→`, `Enter` o `Espacio` avanzan un paso; `↓` o `Av Pág` pasan al capítulo siguiente y `←` vuelve al anterior.
- **Controles:** reproducción, velocidad (0,5×, 1×, 2×) e interruptores para la cámara que sigue a la pieza activa, la espera a la lectura, el sonido sintetizado y las portadas.
- **La línea de tiempo** muestra el avance y permite saltar a cualquier capítulo.

### Parámetros de URL

| Parámetro | Efecto |
|-----------|--------|
| `?stage=1` … `?stage=6` | Empieza directamente en ese capítulo |
| `?portadas=1` | Muestra el prólogo, las portadas de capítulo y el epílogo |
| `?cam=0` | Cámara fija, sin acercamientos |

Respeta `prefers-reduced-motion`: con movimiento reducido muestra cada paso como imagen fija.

Para más detalle técnico, consulta [docs/ARQUITECTURA.md](docs/ARQUITECTURA.md). Para colaborar, [CONTRIBUTING.md](CONTRIBUTING.md).

## Estructura del repositorio

```
index.html          Página final, lista para publicar (generada)
build.py            Genera index.html a partir de src/
src/base.html       Figura base: geometría isométrica, modelo y animación
src/doc.js          Capa documental: portadas, línea de tiempo, interruptores
src/doc.css         Estilos: diseño en pantallas grandes, controles, leyenda
src/controls.html   Marcado de los controles
src/legend.html     Código de color y reparto de piezas
docs/               Capturas y documentación técnica
```

`build.py` aplica sobre `src/base.html` las correcciones de guion y las capas de `src/`, y escribe `index.html`. Para regenerar la página tras editar algo en `src/`:

```bash
python3 build.py
```

Solo necesita Python 3, sin paquetes adicionales. Cada sustitución comprueba que el texto original aparece exactamente una vez, así que si se edita `src/base.html` y una sustitución deja de coincidir, el script se detiene y dice cuál.

## Publicar en GitHub Pages

El repositorio incluye un flujo de trabajo en `.github/workflows/pages.yml` que publica la página en cada envío a `main`.

1. Crea el repositorio en GitHub y sube el contenido:
   ```bash
   git init
   git add .
   git commit -m "Linotipia de tokens"
   git branch -M main
   git remote add origin https://github.com/alenj0x1/linotipia-de-tokens.git
   git push -u origin main
   ```
2. En el repositorio, ve a **Settings → Pages** y en **Source** elige **GitHub Actions**.
3. Tras el primer envío, la página queda en `https://alenj0x1.github.io/linotipia-de-tokens/`.

Al ser un único archivo estático, también funciona en Netlify, Vercel, Cloudflare Pages o cualquier servidor web: solo hay que servir `index.html`.

## Honestidad de la ilustración

Es una simplificación deliberada. Seis bandejas representan las decenas de capas de un transformer, y una sola aguja por token resume las muchas cabezas de atención que trabajan en paralelo. Doce casillas representan una ventana de contexto que en un modelo real tiene cientos de miles de tokens. Las probabilidades, pérdidas y recompensas son ejemplos calculados en la página con softmax. La figura muestra cómo funcionan en general los grandes modelos de lenguaje, no la arquitectura interna de ningún modelo concreto.

## Créditos y licencia

Construido con la skill **anatomy** para figuras isométricas, cuyo kit de dibujo va incluido dentro de `index.html` y `src/base.html` bajo licencia MIT (ver `THIRD_PARTY_NOTICES.md`).

El resto del proyecto se distribuye bajo licencia MIT (ver `LICENSE`).
