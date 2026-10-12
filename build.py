#!/usr/bin/env python3
"""Construye index.html a partir de src/base.html y las capas de src/.
Uso: python3 build.py"""
import re, os
ROOT = os.path.dirname(os.path.abspath(__file__))
S = lambda n: open(os.path.join(ROOT, "src", n), encoding="utf-8").read()
h = S("base.html")
def rep(old,new,count=1):
    global h
    n=h.count(old)
    assert n==count, (n, old[:90])
    h=h.replace(old,new)

# ---------- 1. guion: redundancias y precisión ----------
# compara repetido 3 veces
rep("""showCands(push, b.cands, b.probs, b.truth, false, `<b>Compara.</b> Al entrenar la ruleta no se juega: sólo gira despacio hasta que el puntero señala la palabra real, ${tok(b.cands[b.truth], "y")}. Su porción del círculo es lo que el modelo le daba: ${pct(b.probs[b.truth])}.`, { train: true });""",
"""showCands(push, b.cands, b.probs, b.truth, false, first
        ? `<b>Compara.</b> Al entrenar la ruleta no se juega: sólo gira despacio hasta que el puntero señala la palabra real, ${tok(b.cands[b.truth], "y")}. Su porción del círculo es lo que el modelo le daba: ${pct(b.probs[b.truth])}. Las otras porciones son las palabras en las que se equivocaba.`
        : `<b>Compara.</b> La ruleta va directa a la palabra real, ${tok(b.cands[b.truth], "y")}. Fíjate en su porción: ya ocupa ${pct(b.probs[b.truth])} del círculo.`, { train: true });""")
rep("""aguja del panel y punto coral en la gráfica. Cuanto más baja, mejor.`, first ? 1 : 0.6);""",
"""${first ? "aguja del panel y punto coral en la gráfica. Si hubiera dado 100 %, la pérdida sería 0; cuanto más baja, mejor." : "la aguja marca menos que antes."}`, first ? 1 : 0.6);""")
# tasa de aprendizaje
rep("""Un modelo real tiene miles de millones de perillas y hace este paso con millones de tokens a la vez.`""",
"""Cuánto gira cada una lo decide la <b>tasa de aprendizaje</b>: si fuera grande, borraría lo aprendido; si fuera diminuta, no avanzaría. Un modelo real tiene miles de millones de perillas y hace este paso con millones de tokens a la vez.`""")
# miles de millones -> billones
rep("""`<b>Progreso.</b> ${fmt(Math.round(tokensB))} mil millones de tokens leídos.""",
"""`<b>Progreso.</b> ${tokensB >= 1000 ? dec(tokensB / 1000, 1) + " billones (millones de millones)" : fmt(Math.round(tokensB)) + " mil millones"} de tokens leídos.""")
rep("""narr(`<b>Esto se repite billones de veces</b>, en miles de chips durante meses.""",
"""narr(`<b>Esto se repite cientos de miles de veces</b>, cada paso con millones de tokens a la vez: billones de tokens en total, en miles de chips durante meses.""")
# respuestas A y B idénticas
rep("""narr(`<b>Respuesta ${name}.</b> Ahora es el modelo quien responde, token a token. Se le pide la misma respuesta varias veces y no siempre sale igual.`, ai === 0 ? 1 : 0.6);""",
"""narr(ai === 0
        ? `<b>Respuesta A.</b> Ahora es el modelo quien responde, token a token, en tipos verdes. Se le pide varias veces lo mismo y, como la ruleta sortea, no siempre sale igual.`
        : `<b>Respuesta B.</b> Misma petición, otra tirada de la ruleta: esta vez sale una respuesta distinta. Ya hay dos candidatas para comparar.`, ai === 0 ? 1 : 0.7);""")
rep("""Con ese libro, otro modelo critica y corrige respuestas (la <b>IA constitucional</b> de Anthropic).""",
"""Guiado por ese libro, otro modelo también critica, corrige y compara respuestas (la <b>IA constitucional</b> de Anthropic).""")
# atención: menos repetición, con datos
rep("""const top = tok(topOf(qPos, w), slots[w.indexOf(Math.max(...w))]?.kind === "gen" ? "m" : slots[w.indexOf(Math.max(...w))]?.kind === "tool" ? "s" : "");""",
"""const top = tok(topOf(qPos, w), slots[w.indexOf(Math.max(...w))]?.kind === "gen" ? "m" : slots[w.indexOf(Math.max(...w))]?.kind === "tool" ? "s" : "") + ` (${pct(Math.max(...w))})`;""")
rep("""Las agujas turquesa son la respuesta: aquí mira sobre todo a ${top}.`);""",
"""Las <b>agujas turquesa</b> de la canaleta son la respuesta: cuanto más alta, más atención. Aquí la más alta está sobre ${top}.`);""")
rep("""Las primeras capas suelen fijarse en lo cercano: la gramática y el orden de las palabras. Mira sobre todo a ${top}.`);""",
"""Las primeras capas suelen fijarse en lo cercano: la gramática y el orden de las palabras. Las agujas cambian de altura: ahora gana ${top}.`);""")
rep("""narr(`<b>Capas ${L + 1} y ${L + 2}.</b> ${talk[L - 2]} ${talk[L - 1]} Mira sobre todo a ${top}.`, 0.9);""",
"""narr(`<b>Capas ${L + 1} y ${L + 2}.</b> ${talk[L - 2]} ${talk[L - 1]} Aguja más alta: ${top}.`, 0.9);""")
rep("""narr(`<b>Capa 2 · Red neuronal.</b> En cada capa el vector se enriquece un poco más. Un modelo real tiene decenas de capas; aquí hay 6.`);""",
"""narr(`<b>Capa 2 · Red neuronal.</b> Lo que calcula cada capa se <b>suma</b> al vector que ya traía (la conexión residual): se enriquece sin perder lo anterior. Un modelo real tiene decenas de capas, y en cada una muchas «cabezas» de atención miran a la vez; aquí hay 6 capas y una sola aguja por token.`);""")
rep("""cada token tiene su varilla de números: se saca la del token actual y sus cuentas de colores pasan al elevador. Ese <b>vector</b> sube ahora capa por capa.`""",
"""cada token tiene su varilla de números: se saca la del token actual y sus cuentas de colores pasan al elevador. A ese <b>vector</b> se le añade también su <b>posición</b> en la frase, porque el orden importa. Ahora sube capa por capa.`""")
# probabilidades + temperatura
rep("""del vocabulario (decenas de miles).""","""del vocabulario (entre decenas y cientos de miles).""")
rep("""casi siempre cae en las más probables, pero no siempre. Eso es el <b>muestreo</b>.`""",
"""casi siempre cae en las más probables, pero no siempre. Eso es el <b>muestreo</b>. La <b>temperatura</b> regula el riesgo: baja, gana casi siempre la porción mayor; alta, sale más variedad.`""")
# caché KV
rep("""Lo verás más rápido: en un modelo real cada viaje dura una fracción de segundo.`""",
"""Lo verás más rápido, y no es sólo por abreviar: los cálculos de los tokens anteriores quedan guardados (la <b>caché KV</b>), así que sólo el token nuevo hace el viaje entero. En un modelo real cada viaje dura milisegundos.`""")
# fin de turno
rep("""Un viaje completo por todas las capas por cada token. Los pesos no cambiaron: el modelo no aprende de tu conversación.`);""",
"""Un viaje completo por todas las capas por cada token. Termina cuando la ruleta saca un token especial de <b>fin de turno</b>. Los pesos no cambiaron: el modelo no aprende de tu conversación, sólo la lee.`);""")
# herramientas: segunda vuelta más breve
rep("""showCands(push, g.cands, probs, 0, false, `<b>Elige herramienta.</b> Ahora el token más probable no es una palabra, sino una llamada: ${g.cands.slice(0, 4).map((c, i) => `${tok(c, "s")} ${pct(probs[i])}`).join(" · ")}.`);""",
"""showCands(push, g.cands, probs, 0, false, ranTools === 0
          ? `<b>Elige herramienta.</b> Ahora el token más probable no es una palabra, sino una llamada: ${g.cands.slice(0, 4).map((c, i) => `${tok(c, "s")} ${pct(probs[i])}`).join(" · ")}.`
          : `<b>Elige herramienta.</b> Con el pensamiento delante, cambia la ganadora: ${g.cands.slice(0, 3).map((c, i) => `${tok(c, "s")} ${pct(probs[i])}`).join(" · ")}.`);""")
rep("""narr(`<b>Ejecuta.</b> No lo hace el modelo: el <b>orquestador</b>, el programa que lo rodea, lee la llamada y comprueba que sea válida. En la <b>centralita</b> de delante, la clavija viaja hasta la toma de esa herramienta y se enchufa.`);""",
"""narr(firstCall
            ? `<b>Ejecuta.</b> No lo hace el modelo: el <b>orquestador</b>, el programa que lo rodea, lee la llamada y comprueba que sea válida. En la <b>centralita</b> de delante, la clavija viaja hasta la toma de esa herramienta y se enchufa.`
            : `<b>Ejecuta.</b> La clavija salta a otra toma: la de ejecutar código. El orquestador vuelve a validar la llamada antes de lanzarla.`);""")

rep('''        forward(push, here, g.focus, false, ranTools === 0 ? `<b>Elige herramienta.</b>''','''        const firstCall = ranTools === 0;
        forward(push, here, g.focus, false, ranTools === 0 ? `<b>Elige herramienta.</b>''')
rep('say(`${emitted} fragmentos · ${dropped} descartados`);', 'say(emitted ? `${emitted} fragmentos · ${dropped} descartados` : "datos listos");')
# ---------- 2. bucle: el documental ----------
rep("""    drawSpinners(dt);\n""","""    drawSpinners(dt);\n    docTick(dt);\n""")
rep("""if (beat >= beats.length && beatLeft <= 0 && (holdLeft <= 0 || !WAIT_READ) && !finished) { finished = true; paused = 3.5; }""",
"""if (beat >= beats.length && beatLeft <= 0 && (holdLeft <= 0 || !WAIT_READ) && !finished) { finished = true; paused = docEnd(); }""")
rep("""  sayEl.innerHTML = SAY[stageNow];\n""","""  sayEl.innerHTML = SAY[stageNow];\n  docStart(stageNow, user);\n""")
rep("""startStage(fromUrl >= 1 && fromUrl <= 6 ? fromUrl - 1 : 4);""",
"""docInit();\nif (fromUrl >= 1 && fromUrl <= 6) startStage(fromUrl - 1); else { DOC.prologue = true; startStage(0); }""")
rep("""<span class="iso-plate-corner" data-corner="hint">Toque: paso · doble: etapa</span>""",
"""<span class="iso-plate-corner" data-corner="hint">Toque: avanzar · doble: capítulo</span>""")

DOC_JS = S('doc.js')
rep("""window.__linoDurations = (auto) =>""", DOC_JS + """\nwindow.__linoDurations = (auto) =>""")

rep('camBtn.textContent = CAM_ON ? "🔍 Cámara: sigue" : "🔍 Cámara: fija"; camBtn.setAttribute("aria-pressed", String(CAM_ON));','swSet(camBtn, CAM_ON);')
rep('''paceBtn.textContent = WAIT_READ ? "⏱ Ritmo: lectura" : "⏱ Ritmo: automático";
    paceBtn.setAttribute("aria-pressed", String(!WAIT_READ));''','swSet(paceBtn, WAIT_READ);')
rep('''    paceBtn.title = WAIT_READ ? "Cada frase espera a que termines de leerla" : "La animación sigue su propio ritmo sin esperar al texto";\n''','')
rep('pauseBtn.textContent = pausedUser ? "▶ Seguir" : "❚❚ Pausa"; pauseBtn.setAttribute("aria-pressed", String(pausedUser));','setPlay(pauseBtn, pausedUser);')
rep('const label = (t) => { soundBtn.textContent = t; };','const label = (t) => swSet(soundBtn, /sí|otra vez/.test(t), /Sin audio/.test(t) ? "no disponible aquí" : /otra vez/.test(t) ? "toca otra vez" : "");')
rep('    soundBtn.setAttribute("aria-pressed", String(SND.on));\n','')
rep('soundBtn.textContent = "♪ Sonido: sí";','swSet(soundBtn, true);')
# ---------- 3. HTML ----------
rep("""<p class="lino-lede" data-lede aria-hidden="true"></p>""",
"""<p class="lino-lede" data-lede aria-hidden="true"></p><div class="doc-card" data-doc aria-live="polite"><div class="doc-in"><p class="doc-kicker" data-doc-k></p><h2 class="doc-h" data-doc-h></h2><p class="doc-q" data-doc-q></p><ul class="doc-see" data-doc-see></ul><p class="doc-prev" data-doc-prev></p><div class="doc-foot"><span class="doc-bar"><i data-doc-bar></i></span><button type="button" data-doc-skip>Empezar ▸</button></div></div></div>""")
rep("""<button type="button" data-pause aria-pressed="false">❚❚ Pausa</button>""",
"""<button type="button" data-doc-back title="Capítulo anterior" aria-label="Capítulo anterior">‹ Cap.</button><button type="button" data-pause aria-pressed="false">❚❚ Pausa</button><button type="button" data-doc-next title="Capítulo siguiente" aria-label="Capítulo siguiente">Cap. ›</button><button type="button" data-doc-restart title="Ver desde el prólogo">↺ Desde el inicio</button>""")
rep("""<button type="button" data-sound aria-pressed="false">♪ Sonido: no</button></div></div>""",
"""<button type="button" data-sound aria-pressed="false">♪ Sonido: no</button><button type="button" data-covers aria-pressed="false" title="Muestra u oculta las portadas de prólogo, capítulos y epílogo">🎞 Portadas: no</button></div><div class="doc-time"><div class="doc-tl" data-doc-tl role="group" aria-label="Capítulos"></div><p class="doc-clock"><span data-doc-now></span><span data-doc-clock></span></p></div></div>""")
rep("""<nav class="lino-stages" aria-label="Etapas">""","""<nav class="lino-stages" aria-label="Etapas" hidden>""")
rep("""<p class="lino-say" data-say aria-live="polite"></p>""",
"""<details class="lino-sum"><summary>Resumen del capítulo</summary><p class="lino-say" data-say></p></details>""")
a=h.index('<div class="lino-ctl" data-controls>'); b=h.index('</p></div>', h.index('<div class="doc-time">',a))+len('</p></div>')
h=h[:a]+S('controls.html').strip()+h[b:]
rep('<details class="lino-sum"><summary>Resumen del capítulo</summary><p class="lino-say" data-say></p></details>','<p class="lino-say" data-say hidden></p>')
# legend
a=h.index('<figcaption class="iso-legend">'); b=h.index('</figcaption>',a)+len('</figcaption>')
h=h[:a]+S('legend.html')+h[b:]
# css
h=h.replace('</style>', S('doc.css')+'</style>',1)
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(h)
print("ok", len(h))
