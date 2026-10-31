# Changelog

Todos los cambios notables de este skill se documentan aquí.

El formato sigue [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
El versionado es semántico: `MAJOR.MINOR.PATCH`.

## [1.4.1] — Día del Pastor: último domingo de octubre

### Fixed
- **El Día del Pastor ya tiene fecha:** el último domingo de octubre, que es cuando las iglesias de Ecuador celebran a sus pastores. Antes no tenía fecha por defecto, y su paleta solo salía si se pedía.
- **Si dos conmemoraciones coinciden, gana la del tema principal del sermón.** A fin de octubre el Día del Pastor y el de la Reforma pueden caer en la misma ventana: en 2027, los dos el 31. Antes ganaba la primera de la lista.

### Added
- **Regla `ultimo-domingo:MM`** para las fechas conmemorativas.

## [1.4.0] — 60 paletas que rotan solas, sin café

El skill caía una y otra vez en paletas café: 22 de las 27 paletas originales tenían fondo espresso o acentos tostados (`#D4A574`, `#B89878`), y el modelo, cuando dudaba, iba ahí. Además preguntaba la paleta en cada sermón. Ahora la elige un script: rota entre 60 paletas sin repetir, respeta las fechas conmemorativas y no usa café salvo que se pida.

### Added
- **`palettes/catalog.json`: 94 paletas.**
  - **60 en rotación:**
    - las paletas reales de los sermones de 2026;
    - seis originales sin café;
    - nuevas de fondo «noche» (casi negro con un tinte) y «joya» (profundo y saturado), con acentos vivos.
  - **12 conmemorativas:** Navidad, Fin de año, Ramos, Viernes Santo, Resurrección, Pentecostés, Madre, Padre, Niño, Amor y Amistad, Reforma y Pastor.
  - **22 solo a pedido:** las originales café y una clara.

  Cada paleta trae 16 tokens (fondo, acentos, láminas claras e impresión), temas, ancla bíblica y sus reglas.
- **`scripts/palettes.py`:**
  - **`pick`** elige la paleta de un sermón. Gana la que comparte más temas; no repite una paleta usada en 13 semanas ni la familia del mismo predicador en 26, y separa por matiz las de la misma semana. Nunca falla.
  - **`check`** valida el catálogo: contraste (regla 1), anti-café, que no haya dos casi iguales y el mínimo de 60.
  - **`derivar`** completa una paleta a partir de su fondo y su acento.
  - **`fechas`** lista las conmemoraciones de un año.
  - **`muestrario`** genera un HTML para revisar las paletas a ojo.
- **Módulos de apoyo, sin dependencias:**
  - `scripts/palette_color.py`: OKLab/OKLCH, contraste WCAG y detección de café.
  - `scripts/palette_calendar.py`: Pascua, Adviento, domingos n-ésimos y ventanas.
- **`scripts/test_palettes.py`:** 44 pruebas, incluida la del catálogo real.
- **Conmemoraciones configurables:** usan las reglas de Ecuador, y `config-local.md` puede sobrescribirlas y fijar el Día del Pastor.

### Changed
- **El skill ya no pregunta la paleta:** la usa y la reporta al final con su porqué. Solo pregunta si el usuario quiere elegir.
- **`theme-mapping.md` reescrito:** vocabulario de temas, conmemoraciones, reglas anti-café y uso del script. Sin los bloques de paletas, pesa menos en cada invocación.
- **Las SPA llevan `<meta name="sermon-palette">`** para que la rotación sepa qué paleta se usó.
- **Entidad no reconocida:** va la paleta de `pick`, no `default`, que es café.
- **`doctrine.md`, regla 13:** las excepciones de acento van escritas en las reglas de la paleta.

### Notes
- Las originales café siguen disponibles con `--paleta` (`grace`, `default`, `covenant`…).
- Pentecostés y Pasión (originales) entran a la rotación con el fondo apenas neutralizado, para que no lea café.
- El anti-café está calibrado con paletas reales: marca los tostados, las arenas y las terracotas, y respeta los oros, ámbares y corales vivos.
- Las presentaciones ya generadas no cambian.

## [1.3.0] — el control funciona desde el teléfono

En Android, las SPA no pasaban del selector de modo: al tocar una opción, Chrome mostraba un error. El selector navegaba con `?mode=`, y un HTML abierto desde WhatsApp o Descargas llega como `content://`. Chrome le pasa la URL completa al proveedor de contenido, y el permiso que da la app cubre solo la URI exacta: cualquier carga nueva con algo agregado a la URL falla. En la PC nunca se notó, porque `file://` ignora el query.

La proyección sigue saliendo de una PC en modo Cabina. El Control ahora funciona desde esa PC, desde otra o desde el teléfono.

### Fixed
- **El selector arranca el modo en la misma página**, sin navegar a otra URL.
- **Reloj lógico en `reference-example.html`** (`nextTs()`): un control con el reloj atrasado respecto a la PC de cabina ya no queda ignorado. Las presentaciones recientes ya lo tenían; el reference, no.

### Added
- **Modo por `#modo`** (`sermon.html#control`), además de `?mode=`. Si vienen ambos, gana `?mode=`.
- **La recarga conserva el modo:** por `#modo` en `file://` y `https://`; en `content://`, por `history.state`, sin tocar la URL.
- **Atrás vuelve al selector** y Adelante, al modo, como cuando el selector navegaba: cada modo elegido es una entrada nueva del historial (`history.pushState`).
- **Botón «‹ Modos»** en el encabezado del Control y en la barra de Imprimir, para volver al selector con un clic. No aparece en Cabina ni en Presentación, que se proyectan limpias, ni en el PDF.
- **`SKILL.md` § "Selección de modo"**: las reglas que cumple cualquier SPA, venga su motor del reference o de una presentación anterior, con un grep de verificación.

### Changed
- `standalone` pasa a llamarse `presentation` en `reference-example.html`, como en el resto de los documentos. `standalone` sigue como alias.
- Roles explícitos en `SKILL.md`, README y la cabecera AGPL: la Cabina (`screen`), siempre desde una PC; el Control, desde la misma PC, otra PC o el móvil.
- `ROADMAP.md`: ya no propone deshabilitar `control` en móvil, y el motor canónico parte de las presentaciones recientes, no del reference de mayo.
- `doctrine.md`, regla 23: habla del modo `print`, sin `?mode=`.

### Verified
- **En escritorio**, con Chrome headless y CDP: 40 pruebas sobre `reference-example.html` y 39 sobre una presentación reciente con el mismo cambio, todas en verde. Cubren selección por botón, `#modo` y `?mode=`; recarga; Atrás, Adelante y «‹ Modos»; sincronización por MQTT en los dos sentidos, incluido un control con el reloj 60 s atrasado; PDF de impresión con contenido y sin el botón; y el Control en pantallas de teléfono y tablet.
- **En un teléfono Android con Chrome**, con la Cabina en la PC: abierto desde Descargas (`content://media/...`) y desde WhatsApp, el Control entra, pasa láminas, vuelve al selector con Atrás y con «‹ Modos», y al recargar sigue en Control y recupera la lámina desde la Cabina.

### Notes
Las presentaciones ya generadas no cambian. En la PC siguen funcionando con `?mode=`; en Android necesitan el mismo cambio, aplicado aparte. Tras una recarga, el cronómetro del Control vuelve a cero (pendiente en el ROADMAP).

## [1.2.0] — pipeline de imágenes: persistir, optimizar, atribuir

El skill no especificaba cómo manejar imágenes: ni dónde guardarlas, ni con qué compresión, ni cómo acreditarlas. Esta versión define el pipeline completo.

### Added
- **`image-pipeline.md`** (documento de referencia, **lectura condicional**: solo si el sermón usa imágenes): sourcing, persistencia, perfiles de optimización, inyección y atribución.
- **`scripts/optimize-image.py`**: conversión a WebP con tres perfiles (`bg`, `fg-half`, `fg-third`), recorte tipo `cover` con `--focus`, y registro de procedencia con `--credit` en `credits.json`. Incluye `--inject` (reemplaza un placeholder `{{IMG:clave}}` por el data URI, in place) y `--check` (falla si queda algún placeholder sin inyectar).
- **`scripts/recover-embedded-images.py`**: extrae a disco las imágenes de presentaciones generadas con versiones anteriores, que solo existen como base64 dentro del HTML. Sin recomprimir, idempotente, no modifica el HTML.
- **Nombres planos con fecha y slug**: `{YYYYMMDD}-{slug-corto}-{clave}.webp`. Sin subcarpeta por sermón, y sin colisiones entre claves repetidas (`portada`, `amanecer`) de sermones distintos.
- **`license-attribution.md` § 6**: procedencia de las imágenes. Las generadas con IA se **declaran**, no se acreditan — no hay autor, pero en material de enseñanza una imagen sintética no puede pasar por documental, y nunca debe ilustrar un hecho, lugar o persona reales. Las de banco llevan autor y URL. Las aportadas por el predicador exigen preguntar el origen antes de usarlas: que alguien las entregue no significa que tenga los derechos.
- **Tres escenarios de imágenes en la SPA**, cada uno con su línea de créditos: solo generadas con IA, mixtas (IA + del predicador), o solo del predicador. En el caso mixto la línea no puede decir solo "generadas con IA", sería falso sobre las del predicador. Campo `image_credits` en el frontmatter del bosquejo.
- **Bootstrap de directorios**: si `resources_root` o los directorios de la entidad no existen, el skill reporta qué falta y ofrece crear el esqueleto. No inventa rutas alternativas ni escribe en el directorio actual.
- **`CHANGELOG.md` y `ROADMAP.md`.** El roadmap sale de `SKILL.md` a su propio archivo: deja de cargarse en cada invocación (~550 tokens menos).

### Fixed
- **El base64 nunca debe pasar por la salida del modelo.** No estaba dicho en ninguna parte. El modo de fallo malo — intentar transcribir el string — corrompe la imagen en silencio. Ahora la inyección la hace el script sobre un placeholder, y `SKILL.md` § 8 lo declara explícitamente.
- **Toda imagen que llegue a la SPA debe existir antes como archivo** bajo `<resources_root>/assets/imagenes-sermones/`, un directorio local fuera de todo repo. La regla existía en `SKILL.md` § 1 pero solo cubría imágenes que venían *dentro* del bosquejo; las obtenidas durante la generación no tenían regla, y podían terminar sin copia recuperable.
- **Las fotos de banco necesitan crédito.** Los bloques de licencia cubren el programa (AGPL-3.0), no las imágenes. `license-attribution.md` no las mencionaba.
- **Los repos ya no reciben imágenes.** Los repos de bosquejos y presentaciones contienen solo el entregable (`.md` / `.html`); las imágenes viven en `<resources_root>/assets/imagenes-sermones/`, un directorio plano y local fuera de todo control de versiones. La SPA es autocontenida, así que no las necesita en runtime, y el respaldo de ese directorio corre por cuenta del usuario.
- **El `.md` generado ya no lleva imágenes.** Si el bosquejo entrante trae una, se extrae para usarla en la SPA pero el markdown queda como texto; si tenía pie o texto alternativo, se conserva como nota sin enlace. Antes se referenciaban con paths relativos dentro del repo.
- **Contradicción de licencia en `license-attribution.md` § 6** (antes § 5). La prosa decía que los documentos del skill son CC BY-SA 4.0, pero el pie que ese mismo apartado manda poner declara AGPL-3.0-or-later, igual que el `LICENSE` de la raíz. El error venía de confundir los *documentos del skill* (la herramienta → AGPL) con el *`.md` que el skill genera* (obra del predicador → CC BY-SA). Ahora hay una tabla explícita con las tres licencias en juego.
- **Cabecera de licencia en los scripts.** No la tenían: al copiarlos fuera del repo viajaban sin indicación, aunque el `LICENSE` de la raíz ya los cubriera. Añadida nota AGPL + `SPDX-License-Identifier`.
- **Referencia al repo desactualizada** en seis documentos, que aún decían "pendiente — aún no publicado".

### Measured
Sobre imágenes de banco típicas (1600×900 JPEG):

- **`bg`** (1280×720 q65): 94 KB → 32 KB, **34% del original**. SSIM contra el original *ya compuesto bajo el scrim* = **0.979**, imperceptible en proyección — el velo cubre del 12% al 80% de opacidad, así que el fondo tolera compresión agresiva.
- **`fg-half`** (960×1080 q80): ~55 KB, SSIM 0.988. Al frente no hay velo que disimule artefactos; por debajo de q80 se nota.
- Una presentación con cinco fondos baja alrededor de **60%** de peso total.
- Subir la calidad "por si acaso" no ayuda: un fondo a q90 pesa 3× y se ve igual bajo el velo.

### Notes
Aditivo. Las presentaciones ya generadas siguen funcionando sin cambios — son archivos autónomos. `recover-embedded-images.py` no las modifica.

Los perfiles `fg-*` piden orientación portrait: media lámina de 16:9 es ~8:9. Una fuente landscape no la llena sin agrandar; el script nunca agranda y lo reporta.

## [1.1.0] — catálogo de paletas y atribución del skill

### Added
- Catálogo de paletas expandido de 8 a 19, con variantes intra-paleta (`grace-jewel`, `hope-twilight`, `default-ember`, etc.) para distinguir dos cultos del mismo domingo con temas cercanos.
- Atribución discreta del skill en la SPA generada (clase `.skill-attribution` en el footer, frase añadida en modo print), como exige la AGPL-3.0.

### Changed
- Introducción del README reescrita para lectores pastorales no técnicos.

## [1.0.0] — primer release estable

### Added
- Flujo completo bosquejo → SPA + bosquejo limpio en markdown.
- SPA autocontenida con 4 modos (presentation, screen, control, print) y sincronización MQTT entre cabina y púlpito.
- Configuración por `config-local.md`: `resources_root`, `user`, `entities` con roles y destinos de publicación.
- Documentos de referencia: `doctrine.md` (24 reglas de diseño), `parser-guidelines.md`, `theme-mapping.md`, `identity-discovery.md`, `license-attribution.md`.

## [0.1.0] — release inicial

Primera versión publicable del skill `/sermon`.

---

<small>

**Skill:** /sermon — generador de presentaciones homiléticas
**Licencia del skill:** AGPL-3.0-or-later
**Repo:** https://github.com/CafecitoTeologico/ct-skill-sermon

</small>
