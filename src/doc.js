function swSet(b, on, note = "") { b.setAttribute("aria-checked", String(!!on)); const n = b.querySelector(".sw-n"); if (n) n.textContent = note; }
function setPlay(b, paused) { b.setAttribute("aria-pressed", String(paused)); const t = paused ? "Seguir" : "Pausa"; b.setAttribute("aria-label", t); b.title = t; }
// ---------------- documentary: prologue, chapter cards, timeline, epilogue ----------------
const CHAPTERS = [
  { t: "Datos", q: "¿De dónde sale todo lo que sabe un modelo?",
    log: "Antes de que exista el modelo hay que reunir su materia prima: texto. Mucho texto, de muchas fuentes, y casi todo hay que limpiarlo antes de usarlo.",
    see: [["#cfe3f2", "Cajas de fuentes", "lanzan fragmentos de texto"], ["#f6e6b0", "Tres cribas", "calidad, duplicados, privacidad"], ["#e8dcc6", "Cubo", "recoge lo descartado"], ["#e8dcc6", "Tolva", "guarda el texto listo, en tokens"]],
    recap: "El texto se reunió, se limpió y se cortó en tokens." },
  { t: "Preentrenar", q: "¿Cómo aprende a escribir una máquina a la que nadie le da reglas?",
    log: "Con un único ejercicio repetido sin descanso: tapar la palabra siguiente, intentar adivinarla y corregir el error. Veremos tres momentos de ese entrenamiento: el principio, la mitad y el final.",
    see: [["#e8dcc6", "Canaleta", "el texto de ejemplo"], ["#dcd6fb", "Torre de 6 capas", "donde se calcula la predicción"], ["#fbd7e5", "Panel y perillas", "la pérdida y los pesos"], ["#ffd6cf", "Cable coral", "el error que viaja hacia atrás"]],
    recap: "Adivinando la palabra siguiente y corrigiendo el error, los pesos se ajustaron cientos de miles de veces." },
  { t: "Ajustar", q: "¿Cómo pasa de completar texto a ser un asistente útil y honesto?",
    log: "Un modelo preentrenado continúa cualquier texto, pero no sabe ayudar. Ahora aprende de ejemplos escritos por personas, de sus votos y de un juez guiado por principios.",
    see: [["#ffd9c4", "Teclado", "las demostraciones humanas"], ["#d5f2e2", "Botones A/B", "los votos de las personas"], ["#ffd6cf", "Libro y balanza", "el juez y sus principios"], ["#fff0c2", "Barras amarillas", "probabilidades antes y después"]],
    recap: "Con demostraciones, votos y un juez con principios, aprendió a preferir buenas respuestas." },
  { t: "Evaluar", q: "¿Cómo se sabe que está listo para salir?",
    log: "Antes de publicarlo se le examina a fondo: pruebas con respuestas conocidas, ataques a propósito y revisión de personas. Lo que falla vuelve al taller.",
    see: [["#d5f2e2", "Banco de pruebas", "tarjetas de examen y luces"], ["#ffd6cf", "Tipos coral", "los ataques del equipo rojo"], ["#d5f2e2", "Consola de votos", "la revisión humana"], ["#d5f2e2", "Luz de publicación", "la decisión final"]],
    recap: "Se examinó, se atacó a propósito y se revisó antes de publicarlo." },
  { t: "Responder", q: "¿Qué ocurre dentro cuando le escribes?",
    log: "Ya publicado, el modelo no aprende nada nuevo: sólo usa sus pesos. Seguiremos tu pregunta desde el teclado hasta la última palabra de la respuesta, token a token.",
    see: [["#ffd9c4", "Teclado y guillotina", "tu texto, cortado en tokens"], ["#ddd3f6", "Tabla de vectores", "cada token, convertido en números"], ["#c9efe9", "Agujas turquesa", "la atención de cada capa"], ["#fff0c2", "Ruleta y fundición", "elegir y escribir el token"]],
    recap: "Tu mensaje se convirtió en tokens, cruzó las capas y la respuesta salió token a token." },
  { t: "Herramientas", q: "¿Cómo actúa más allá de lo que sabe?",
    log: "Hay preguntas que el modelo no puede responder de memoria. Veremos cómo piensa, pide una herramienta, espera el resultado y lo usa, encadenando pasos como un agente.",
    see: [["#eadff3", "Tipos lila", "sus pensamientos"], ["#d6eafb", "Tipos celeste", "llamadas y resultados"], ["#e9e0cf", "Centralita", "el orquestador que conecta"], ["#d9ebfb", "Armario", "las herramientas que trabajan"]],
    recap: "Pensó, usó herramientas reales, leyó sus resultados y respondió con precisión." },
];
const PROLOGUE = {
  k: "Un documental en 6 capítulos",
  h: "Linotipia de tokens",
  q: "¿Cómo funciona por dentro un modelo de lenguaje?",
  narr: "<b>Prólogo.</b> Un modelo de lenguaje no se programa línea a línea: se <b>cultiva</b> a partir de texto. Esta máquina imaginaria se inspira en la <b>linotipia</b>, la que fundía líneas de plomo para imprimir periódicos. Cada pieza es una parte del proceso, y en seis capítulos recorreremos el viaje completo: de los datos en bruto a una respuesta que usa herramientas.",
};
const EPILOGUE_NARR = () => "<b>Epílogo.</b> " + CHAPTERS.map((c, i) => `<b>${i + 1} · ${c.t}:</b> ${c.recap}`).join("<br>") + "<br>Detrás de todo hay un único gesto, repetido sin parar: <b>elegir el siguiente token</b>.";
const docEl = document.querySelector("[data-doc]"), docK = docEl.querySelector("[data-doc-k]"), docH = docEl.querySelector("[data-doc-h]"), docQ = docEl.querySelector("[data-doc-q]"), docSee = docEl.querySelector("[data-doc-see]"), docPrev = docEl.querySelector("[data-doc-prev]"), docBar = docEl.querySelector("[data-doc-bar]"), docSkip = docEl.querySelector("[data-doc-skip]");
const tlEl = document.querySelector("[data-doc-tl]"), clockEl = document.querySelector("[data-doc-clock]"), nowEl = document.querySelector("[data-doc-now]");
const DOC = { covers: new URLSearchParams(location.search).get("portadas") === "1", cardL: [], prologue: false, card: null, cardT: 0, cardDur: 0, chapT: 0, dur: [], base: [], last: -1, epilogue: false };
const mmss = (s) => { s = Math.max(0, Math.round(s)); return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`; };
function cardLen(html, items) { return WAIT_READ ? Math.max(5, readTime(html, 0.8) + items * 0.5) : 4; }
function showCard({ k, hh, q, see = [], prev = "", btn = "Empezar", narrHtml, kind }) {
  if (still.matches || !DOC.covers) return 0;
  docK.textContent = k; docH.textContent = hh; docQ.textContent = q;
  docSee.innerHTML = see.map(([c, n, x]) => `<li style="--c:${c}"><b>${n}</b><span>${x}</span></li>`).join("");
  docPrev.textContent = prev; docPrev.hidden = !prev; docSkip.textContent = btn;
  docEl.dataset.kind = kind; docEl.setAttribute("data-show", "");
  if (narrHtml) { lastNarr = narrHtml; narrEl.innerHTML = narrHtml; }
  DOC.card = kind; DOC.cardT = 0;
  DOC.cardDur = kind === "epilogue" ? (WAIT_READ ? Math.max(12, readTime(narrHtml, 0.7)) : 7) : cardLen((narrHtml || "") + q, see.length);
  return DOC.cardDur;
}
function hideCard() { docEl.removeAttribute("data-show"); DOC.card = null; }
function chapterCard(n) {
  const c = CHAPTERS[n];
  const pro = DOC.prologue; DOC.prologue = false;
  if (pro) {
    return showCard({ k: PROLOGUE.k, hh: PROLOGUE.h, q: PROLOGUE.q, see: CHAPTERS.map((x, i) => [CHIP[i], `${i + 1} · ${x.t}`, x.q]), btn: "Empezar", narrHtml: PROLOGUE.narr, kind: "prologue" })
      + 0.01;
  }
  return showCard({ k: `Capítulo ${n + 1} de 6`, hh: c.t, q: c.q, see: c.see, prev: n > 0 ? `Hasta ahora: ${CHAPTERS[n - 1].recap}` : "", btn: "Empezar", narrHtml: `<b>${c.t}.</b> ${c.log}`, kind: "chapter" });
}
function docStart(n, user) {
  hideCard(); DOC.chapT = 0; DOC.epilogue = false;
  // the card appears at once, while the machine resets behind it; a hold beat keeps the timeline waiting until it has been read
  const pro = DOC.prologue;
  chapterCard(n);
  const hold = { d: 0, talks: false, run: () => { hold.d = DOC.card ? Math.max(0, DOC.cardDur - DOC.cardT) : 0; } };
  const extra = [hold];
  if (pro) {

    extra.push({ d: 0, talks: false, run: function () { this.d = still.matches ? 0 : chapterCard(n); } });
  }
  extra.push({ d: 0.01, talks: false, run: hideCard });
  beats.splice(Math.min(3, beats.length), 0, ...extra);
  tlPaint();
}
function docEnd() {
  if (!touring) return 3.5;
  if (stageNow === 5) { DOC.epilogue = true; return showCard({ k: "Epílogo", hh: "Del texto a la respuesta", q: "Todo lo que hace el modelo, al final, es elegir el siguiente token, una y otra vez.", see: [], btn: "Volver a empezar", narrHtml: EPILOGUE_NARR(), kind: "epilogue" }); }
  return 1.2;
}
// covers off: the film runs straight from one chapter to the next, with no title cards
function setCovers(on) {
  DOC.covers = on;
  const b = document.querySelector("[data-covers]");
  if (b) swSet(b, on);
  if (!on && DOC.card) { const wasEpi = DOC.epilogue; hideCard(); beatLeft = 0; holdLeft = 0; if (wasEpi) paused = 0; }
  DOC.dur = DOC.base.map((d, i) => d + (on ? DOC.cardL[i] : 0));
  [...tlEl.children].forEach((b, i) => (b.style.flex = `${DOC.dur[i].toFixed(1)} 1 0`));
  DOC.last = -1; tlPaint();
}
function docTick(dt) {
  if (DOC.card) {
    DOC.cardT += dt;
    docBar.style.transform = `scaleX(${Math.min(1, DOC.cardT / Math.max(0.1, DOC.cardDur)).toFixed(3)})`;
  }
  if (!finished) DOC.chapT += dt;
  tlPaint();
}
function docInit() {
  // the length of each chapter, read off the beats with every caption's reading time
  for (let n = 0; n < 6; n++) {
    const bs = buildStage(n); let t = 0, holdEnd = 0;
    for (const b of bs) { NARR_LOG = []; b.run(); for (const x of timers) x.fn(); timers = []; const start = b.talks ? Math.max(t, holdEnd) : t; if (NARR_LOG.length) holdEnd = start + readTime(...NARR_LOG[NARR_LOG.length - 1]); t = start + b.d; }
    NARR_LOG = null;
    const c = CHAPTERS[n];
    DOC.base[n] = Math.max(t, holdEnd) + 1.2;
    DOC.cardL[n] = cardLen(`<b>${c.t}.</b> ${c.log}` + c.q, c.see.length);
  }
  DOC.dur = DOC.base.map((d, i) => d + (DOC.covers ? DOC.cardL[i] : 0));
  tlEl.innerHTML = CHAPTERS.map((c, i) => `<button type="button" data-ch="${i}" style="flex:${DOC.dur[i].toFixed(1)} 1 0;--chip:${CHIP[i]}" aria-label="Capítulo ${i + 1}: ${c.t}" title="${i + 1} · ${c.t}"><span class="doc-seg"><i></i></span></button>`).join("");
  tlEl.addEventListener("click", (e) => { const b = e.target.closest("[data-ch]"); if (b) { touring = true; startStage(Number(b.dataset.ch), true); } });
  const skip = (e) => {
    e.stopPropagation();
    if (DOC.epilogue) { DOC.prologue = true; touring = true; startStage(0, true); return; }
    if (!DOC.card) return;
    beatLeft = 0; holdLeft = 0; DOC.cardT = DOC.cardDur;
  };
  docEl.addEventListener("click", skip);
  docEl.addEventListener("dblclick", (e) => e.stopPropagation());
  document.querySelector("[data-doc-back]")?.addEventListener("click", () => { touring = true; startStage(DOC.chapT < 4 && stageNow > 0 ? stageNow - 1 : stageNow, true); });
  document.querySelector("[data-doc-next]")?.addEventListener("click", () => { touring = true; startStage(stageNow + 1, true); });
  document.querySelector("[data-covers]")?.addEventListener("click", () => setCovers(!DOC.covers));
  setCovers(DOC.covers);
  document.querySelector("[data-doc-restart]")?.addEventListener("click", () => { DOC.prologue = true; touring = true; startStage(0, true); });
}
function tlPaint() {
  if (!DOC.dur.length) return;
  const n = stageNow, total = DOC.dur.reduce((a, b) => a + b, 0);
  let u = finished ? 1 : Math.min(0.995, DOC.chapT / DOC.dur[n]);
  // after a jump, the beat counter is a better clock than the time spent here
  if (!finished && beats.length && DOC.chapT < 0.05) u = Math.max(u, beat / beats.length * 0.98);
  const key = n + ":" + u.toFixed(3);
  if (DOC.last === key) return; DOC.last = key;
  [...tlEl.children].forEach((b, i) => {
    const f = i < n ? 1 : i === n ? u : 0;
    b.querySelector("i").style.transform = `scaleX(${f.toFixed(3)})`;
    b.toggleAttribute("data-on", i === n);
  });
  const before = DOC.dur.slice(0, n).reduce((a, b) => a + b, 0);
  clockEl.textContent = `${mmss(before + u * DOC.dur[n])} / ${mmss(total)}`;
  nowEl.textContent = DOC.epilogue ? "Epílogo" : `${n + 1} de 6 · ${CHAPTERS[n].t}`;
}
