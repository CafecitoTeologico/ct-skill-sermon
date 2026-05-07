# Doctrina visual — 24 reglas no negociables

Estas reglas definen los constraints que debe cumplir cualquier presentación generada por el skill `/sermon`. Construidas sobre el research compilado por Gemini Pro (Mayo 2026) más ajustes y adiciones específicas para el contexto evangélico ecuatoriano y la tecnología SPA.

> **Aplicación**: las reglas son *no negociables* en tanto el output debe cumplirlas todas. Si el bosquejo o el contexto exigen una excepción, debo flagearla al usuario antes de proceder.

## Las 24 reglas

| # | Regla | Especificación técnica |
|---|---|---|
| 1 | **Contraste** | Objetivo 7:1 (WCAG AAA); mínimo aceptable 4.5:1 (WCAG AA). Nunca por debajo. |
| 2 | **Tamaño de cuerpo** | 32–40pt según tamaño de sala; default **36pt**. Títulos +50% mínimo. |
| 3 | **Palabras por slide** | Máximo 20 palabras; ideal <10. Excepción: cita bíblica clave (ver regla 24). |
| 4 | **Tipografía de citas** | Serif para texto bíblico (Libre Baskerville, Iowan Old Style, Palatino). Sans para resto (Inter, Montserrat, Source Sans). |
| 5 | **Interlineado** | Mínimo 1.4em, ideal 1.5–1.6em. Evita colapso visual a distancia. |
| 6 | **Sin blanco puro** | Prohibido `#FFFFFF` como fondo. Usar grises tibios (`#F4F1ED`) o azules profundos (`#0A192F`) según paleta. |
| 7 | **Progresión de puntos** | Revelar puntos de bosquejo uno por uno (Progressive Disclosure). El control lo dispara desde modo control. |
| 8 | **Imágenes de fondo** | Opacidad ≤ 20% si hay texto encima. Preferir overlays sólidos sobre imágenes texturadas. |
| 9 | **Jerarquía del versículo** | La referencia (ej. "Marcos 5:34") debe ser ≥30% más pequeña que el cuerpo del versículo. Indicación de traducción (NTV, RV60) más pequeña aún, en color tenue. |
| 10 | **Margen de seguridad** | Reservar 8–10% exterior libre de contenido. Algunos proyectores cortan los bordes. |
| 11 | **Sin subrayados** | Usar negrita o color de acento para énfasis. El subrayado corta los descendentes (g, j, p, q, y) y reduce legibilidad. |
| 12 | **Iconografía simple** | Iconos line-art con `stroke-width` consistente. Nada de clipart, gradientes complejos o emojis decorativos en exceso. |
| 13 | **Paleta limitada** | Máximo 3 colores funcionales por presentación (fondo, texto principal, acento). Variantes tonales OK. |
| 14 | **Pantalla de cierre** | Terminar con frase clave del sermón o pantalla neutra/negra. **No** terminar con "Gracias" o emoticones. |
| 15 | **Comillas tipográficas** | Usar comillas curvas `"texto"` (Unicode `“”`) por defecto (estándar latinoamericano). `«texto»` solo si el bosquejo o el usuario lo solicitan explícitamente. |
| 16 | **Sin itálicas extensas** | Más de 3 líneas en cursiva = ilegible a distancia. Para énfasis largo usar negrita o cambio de peso. |
| 17 | **Aspect ratio** | 16:9 forzado (1920×1080 lógico). Container queries para escalar al viewport real. |
| 18 | **Alineación** | Texto bibliográfico/párrafos: alineado a la izquierda. Títulos cortos y frases icónicas: centrado OK. Bloques largos centrados son anti-patrón. |
| 19 | **Sombras de texto** | Si hay imagen de fondo, aplicar `text-shadow` sutil (`0 2px 4px rgba(0,0,0,0.6)`) — nunca como adorno gratuito. |
| 20 | **One Focus Rule** | Cada slide tiene **un solo foco visual**. Si hay 2 cosas importantes, son 2 slides. |
| **21** | **Glifos del español** | Toda fuente seleccionada debe incluir glifos completos: ñ, á, é, í, ó, ú, ü, ¿, ¡. Verificar en `display=swap` que la fuente cargue Latin Extended. |
| **22** | **Indicación de traducción** | Cada cita bíblica indica discretamente la traducción (NTV, RV60, LBLA, etc.) en línea de pie 50% más pequeña, en `text-muted`. Nunca embebido en el cuerpo del texto. |
| **23** | **Print-safe colors** | El stylesheet `?mode=print` mapea colores oscuros a impresión amigable. Sin gradientes pesados, sin imágenes de fondo a sangre, sin texto blanco sobre negro pleno (consume tinta). |
| **24** | **Versículos largos en disclosure progresivo** | Pasajes de >3 líneas se fragmentan en porciones, controladas por modo control vía MQTT. Permite leer junto con la audiencia, no leer en voz lo que ya está completo en pantalla. |

## Tres ajustes a la versión Gemini original

Gemini propuso reglas más estrictas en estos 3 puntos. Las flexibilizamos así:

- **Regla 1** (contraste): Gemini decía "7:1 mínimo". Ajustado a "objetivo 7:1, mínimo 4.5:1".
  *Razón*: el 4.5:1 es estándar legal (WCAG AA) y permite paletas más sutiles cuando la sala lo permite.

- **Regla 2** (cuerpo): Gemini decía "40pt mínimo". Ajustado a "32–40pt según sala, default 36pt".
  *Razón*: la literatura técnica permite 28–32pt en salas medianas y 32–36pt funciona en auditorios típicos.

- **Regla 15** (comillas): Gemini decía "comillas latinas « » obligatorias". Ajustado a "curvas `"X"` por defecto, `«X»` opcional".
  *Razón*: en Latinoamérica las comillas curvas inglesas predominan en publicaciones cotidianas. Forzar `« »` puede sentirse afectado.

## Cuatro reglas adicionales (no estaban en Gemini)

- **Regla 21** (glifos): el español tiene caracteres que muchas fuentes "minimalistas" recortan. Validación obligatoria.
- **Regla 22** (traducción): respeto al lector y a la diversidad de versiones. Discreta pero presente.
- **Regla 23** (print-safe): el modo `?mode=print` debe ser usable e imprimible sin consumir cartuchos.
- **Regla 24** (disclosure de versículos): controla el ritmo de lectura conjunta predicador-audiencia.

## Anti-patterns explícitamente prohibidos

1. **Bullet point hell** — más de 3 viñetas por slide.
2. **Cita enorme completa** — versículo entero >3 líneas mostrado de golpe.
3. **Comillas rectas** `"texto"` — usar siempre tipográficas curvas.
4. **Animaciones de entrada decorativas** — texto rebotando, volando, parpadeando. Romp en con la reverencia.
5. **Stock religioso kitsch** — manos orando con brillos, cruces con destellos Photoshop, fondos celestiales saturados.
6. **Pantalla "Gracias"** al cierre — desperdicia el último foco visual.
7. **Logos en cada slide** — saturan; logo solo en cover y/o cierre.
8. **Múltiples fuentes** — máximo 2 (una serif para citas + una sans para todo lo demás).

## Principios homiléticos visuales

Apoyados en la doctrina de los autores citados:

- **Reynolds (Presentation Zen)**: la *restricción* es el principio. Espacio negativo permite respirar.
- **Duarte (Resonate)**: el sermón es un arco "lo que es / lo que podría ser" (sparkline). La presentación visualiza esa tensión.
- **Tufte**: si el dato es tenue, aburre. Si es denso, confunde. Para proyección, mover lo denso a folletos.
- **Mayer (Multimedia Learning)**: principio de redundancia — no leer en voz alta lo que el público ya está leyendo. La presentación apoya, no duplica.
- **Maeda (Simplicity)**: encoger, ocultar, encarnar. Mostrar la idea encarnada en imagen poderosa.

## Referentes contemporáneos

- **Andy Stanley**: "One Point Preaching" — una frase corta + una imagen impactante por sermón.
- **Tim Keller**: bosquejo lógico revelado paso a paso; el oyente sabe siempre dónde está.
- **Miguel Núñez, Sugel Michelén** (LatAm): exposición textual sobria; visual al servicio del texto bíblico, sin compita.

---

<small>

**Skill:** /sermon — generador de presentaciones homiléticas
**Autor del skill:** Jonathan Ricardo Proaño Alcívar (Parlox), con asistencia de IA Claude (Anthropic).
**Licencia del skill:** AGPL-3.0-or-later (todo el skill — documentos y código que genera).
**Licencia del bosquejo .md generado:** CC BY-SA 4.0 (contenido es obra del predicador, no del skill).
**Licencia de la SPA HTML generada:** AGPL-3.0-or-later (programa ejecutable).
**Repo:** [pendiente — aún no publicado]

</small>
