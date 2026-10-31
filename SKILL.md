---
name: sermon
description: Generador de presentaciones homiléticas. Cuando el usuario invoca /sermon adjuntando un bosquejo (en cualquier formato: md, docx, pdf, txt, etc.), procesar el bosquejo, identificar contexto (predicador, lugar, tema), generar la presentación SPA autocontenida con sincronización MQTT, y la copia limpia del bosquejo en markdown. Ubicar los archivos en los repos correspondientes según las entidades del usuario (config-local.md). NO commitear ni pushear sin confirmación explícita del usuario.
---

# Skill: /sermon

Generador automatizado de presentaciones de sermones a partir de un bosquejo entrante. Pensado para predicadores que quieren un flujo "bosquejo → SPA + bosquejo limpio en markdown" con sincronización MQTT entre cabina y control, sin frameworks ni dependencias pesadas.

## Pre-flight: configuración del usuario

**Antes de procesar cualquier bosquejo, leer `config-local.md` en la raíz del skill.**

- ✅ **Si existe:** parsear `resources_root`, `user`, `entities` y otras preferencias. Usar esos valores en todo el flujo.
- ❌ **Si NO existe:** detener flujo y mostrar al usuario:

  > "No encontré tu `config-local.md`. Tienes 2 opciones:
  >
  > **a) Yo lo creo.** Cuéntame:
  >   - Tu nombre completo
  >   - Ruta donde guardas tus recursos teológicos (ej. `~/sermon-resources/`)
  >   - Entidades donde predicas (iglesia, ministerio, conferencia)
  >   - Tu org de GitHub (si planeas publicar bosquejos/presentaciones)
  >
  > **b) Lo haces tú:** copia `config-local-example.md` → `config-local.md` y llena los campos. Después me avisas.
  >
  > ¿Qué prefieres?"

No procesar ningún bosquejo sin config válido. Toda referencia a rutas, entidades, paths, github orgs, y al "autor del programa" viene del config — nunca hardcodear.

## Documentos de referencia (leer antes de actuar)

| Documento | Propósito |
|---|---|
| `doctrine.md` | Las 24 reglas no negociables del diseño visual |
| `parser-guidelines.md` | Cómo extraer datos del bosquejo (estructurado o no) |
| `theme-mapping.md` | Cómo elegir la paleta de colores según el tema del bosquejo |
| `identity-discovery.md` | Cómo encontrar logos y paletas institucionales en assets/ |
| `license-attribution.md` | Templates de los bloques de atribución y licencia |
| `image-pipeline.md` | Imágenes: dónde guardarlas, cómo optimizarlas e inyectarlas. **Leer solo si el sermón usa imágenes.** |
| `reference-example.html` | Ejemplo de output validado (sermón "Jesús sana", 2026-05-03) |
| `licenses/CC-BY-SA-4.0.txt` | Texto canónico de CC BY-SA 4.0 para repos de bosquejos y recursos (contenido textual) |
| `licenses/AGPL-3.0.txt` | Texto canónico de AGPL-3.0 para repos de presentaciones (programas SPA) y este skill |

### Cómo usar `reference-example.html`

**Es referencia ESTRUCTURAL, no plantilla de estilo.**

- ✅ **Sí inspirar de él:** patrones de slide types (cover/hook/verse/section/etc.), arquitectura del cliente MQTT mínimo escrito a mano, manejo de los 4 modos (presentation/screen/control/print), container queries, manejo de blackout, sincronización de estado.
- ❌ **No copiar de él:** la paleta exacta (oro #D4A574, borgoña #8B3A3A), tipografía específica (Iowan Old Style), o decisiones visuales puntuales. Esos vienen de `theme-mapping.md` aplicado al sermón actual.

Cada nuevo sermón debe tener su propia paleta según el tema (ver `theme-mapping.md`). El `reference-example` solo demuestra **cómo** se construye un output válido, no **qué** colores usar.

### Cómo usar `licenses/`

Cuando vinculemos un repo nuevo a GitHub, copiar el archivo de licencia correspondiente como `LICENSE` (sin extensión) a la raíz del repo, antes del primer commit. GitHub usa `licensee` para detectar la licencia y mostrar el badge correspondiente automáticamente.

| Tipo de repo | Licencia a copiar |
|---|---|
| Repos de **bosquejos** y **recursos** (contenido textual, .md) | `licenses/CC-BY-SA-4.0.txt` → `LICENSE` |
| Repos de **presentaciones** (SPA HTML, programa ejecutable) y este skill | `licenses/AGPL-3.0.txt` → `LICENSE` |

Razón: el selector de licencias de GitHub al crear un repo no incluye CC BY-SA 4.0 (solo licencias de software). Pero GitHub la detecta correctamente si el archivo `LICENSE` contiene el texto canónico completo.

## Flujo de procesamiento

### 1. Recepción del bosquejo

El usuario invoca `/sermon` adjuntando:
- Un archivo `.md`, `.docx`, `.pdf`, `.odt`, `.txt`, o
- Texto pegado directamente en el mensaje.

**Regla de manejo según formato de entrada:**

| Formato entrante | Acción del skill |
|---|---|
| `.md` (markdown) | **Copiar verbatim**. Solo agregar frontmatter + bloque CC BY-SA al final. NO reformatear contenido. |
| `.docx` / `.odt` | **Convertir a markdown** vía `pandoc` (preferido) o extracción heurística. Agregar frontmatter + footer. |
| `.pdf` | **Convertir a markdown** vía `pdftotext` + heurística estructural. Agregar frontmatter + footer. |
| `.txt` / texto pegado | **Estructurar en markdown** detectando títulos, listas, refs bíblicas. Agregar frontmatter + footer. |
| Imagen / escaneo | **Pedir al usuario** versión textual. No procesar OCR sin autorización. |

**El archivo `.md` resultante en el repo de bosquejos siempre se licencia bajo CC BY-SA 4.0**, sin importar el formato de entrada. La licencia AGPL-3.0 aplica solo al programa SPA generado, no al bosquejo.

Si hay imágenes embebidas en el bosquejo entrante, extraerlas a `<resources_root>/assets/imagenes-sermones/` (donde `<resources_root>` viene del config-local.md) para poder usarlas en la SPA. **El `.md` generado no las referencia**: el bosquejo queda como texto. Si la imagen traía pie o texto alternativo, conservarlo como nota en el cuerpo, sin el enlace.

**Las imágenes NO van a los repos.** Los repos de bosquejos y presentaciones contienen solo el entregable (`.md` / `.html`). Toda imagen que termine en la SPA debe existir primero como archivo bajo `<resources_root>/assets/imagenes-sermones/`, un directorio **local** fuera de todo repo, con nombre `{YYYYMMDD}-{slug-corto}-{clave}.webp`. **Nunca dejar el original solo en `/tmp`**: es efímero, y si la única copia queda como base64 dentro del HTML, la imagen se vuelve irrecuperable. El respaldo de ese directorio corre por cuenta del usuario. Ver `image-pipeline.md`.

### 2. Parsing y extracción de datos

Aplicar `parser-guidelines.md`:

- Extraer cabecera: título, predicador, lugar, fecha, pasaje bíblico.
- Extraer cuerpo: tema, propósito, introducción, puntos del cuerpo, transición, conclusión, aplicaciones, frase clave.
- Inferir versión bíblica (NTV/RV60/etc.) o preguntar.
- Si faltan datos críticos (predicador, fecha, lugar, pasaje), **detener y preguntar al usuario**.

### 3. Determinación de destino

Aplicar la tabla de "Decisión de destino" en `parser-guidelines.md`. La lógica usa los `entities` definidos en `config-local.md`:

| Predicador | Lugar de predicación | Repos destino |
|---|---|---|
| `user.full_name` (autor del config) | Entidad con `role: secondary` y `user_also_publishes_to_primary: true` | Repos de la `primary` + repos de la `secondary` (bosquejos + presentaciones de cada) → 4 archivos |
| `user.full_name` | Entidad con `role: primary` o lugar no registrado | Solo repos de la `primary` → 2 archivos |
| Otro predicador | Entidad reconocida (`role: secondary` o subgrupo) | Solo repos de esa entidad → 2 archivos |
| Otro predicador | Lugar no reconocido | Preguntar al usuario |

El skill detecta el lugar matcheando el campo `At:` del bosquejo contra los `aliases` de cada entidad. La detección es case-insensitive y tolerante a variantes de tildes/sin tildes.

### 4. Identificación visual

Aplicar `identity-discovery.md`:
- Resolver slug de entidad.
- Buscar `assets/logo-{slug}.svg|png` y `assets/paleta-{slug}.json`.
- Si encontrado, aplicar override; si no, modo neutro.
- Reportar al usuario qué assets se encontraron.

### 5. Selección de paleta temática

Aplicar `theme-mapping.md`:
- Analizar `theme` y `purpose` del bosquejo.
- Identificar palabras clave.
- Proponer paleta predefinida entre las 19 base: `grace`, `hope`, `judgment`, `mission`, `passion`, `pentecost`, `wisdom`, `lament`, `joy`, `covenant`, `kingdom`, `prayer`, `creation`, `prophetic`, `incarnation`, `resurrection`, `discipleship`, `suffering`, o `default`.
- Si el usuario quiere una variante intra-paleta (p. ej. dos cultos del mismo domingo con tema cercano), permitir `grace-jewel`, `grace-dawn`, `hope-twilight`, `hope-ocean`, `default-stone`, `default-ember`, `mission-sage`, `wisdom-slate`.
- Reportar la elección al usuario antes de generar.

### 6. Generación de filename

Convención (ver `parser-guidelines.md` § "Convención de filename completa"):

```
{YYYYMMDD}-{Slug-Capitalizado}-{Nombre}-{Apellido}.{ext}
```

Aplicar transliteración (ñ→n, tildes→ASCII) y kebab-case con capitalización por palabra.

### 7. Generación del bosquejo limpio (markdown)

Producir un `.md` que:
- Tenga **frontmatter YAML** al inicio (entre `---`) con campos de licencia + metadata canónica del sermón. Ver `license-attribution.md` § 4 para los campos.
- Mantenga el **contenido original del bosquejo** sin cambios de fondo, solo limpieza estructural mínima.
- Termine con el **bloque CC BY-SA 4.0** (ver `license-attribution.md` § 4).
- **No contenga imágenes ni referencias a imágenes.** El repo de bosquejos guarda solo texto; las imágenes viven en `<resources_root>/assets/imagenes-sermones/` y van embebidas en la SPA.

#### Manejo del frontmatter — regla de merge

**Siempre se agrega/mantiene frontmatter al inicio**, incluso cuando el input es un `.md` que se copia verbatim. La lógica es:

| Caso del input | Acción sobre frontmatter |
|---|---|
| `.md` sin frontmatter | **Agregar nuevo** con todos los campos del skill |
| `.md` con frontmatter existente (típico de Obsidian) | **Merge:** preservar campos del usuario + agregar/sobrescribir solo los campos canónicos del skill |
| `.docx`, `.pdf`, etc. (convertidos) | **Generar nuevo** con campos del skill |

**Campos canónicos que el skill SIEMPRE define o sobrescribe** (sus valores son la fuente de verdad para identificación y licencia):

```yaml
title: ...           # del título del bosquejo
preacher: ...        # del campo "By:" o equivalente
at: ...              # del campo "At:" o equivalente
date: ...            # del campo "On:" o equivalente, formato ISO YYYY-MM-DD
date_human: ...      # formato "DD de mes, YYYY"
passage: ...         # del pasaje bíblico principal
language: es         # default
license: CC-BY-SA-4.0
license_url: https://creativecommons.org/licenses/by-sa/4.0/
license_short: "Uso libre con atribución y bajo la misma licencia."
attribution: "Bosquejo de {PREACHER}"
repo: {REPO_GITHUB_URL}
```

**Campos del usuario que se PRESERVAN sin tocar** (típicos de Obsidian u otros editores):

- `tags`
- `aliases`
- `cssclass`, `cssclasses`
- `date created`, `date modified`
- `cover`, `banner`
- Cualquier campo custom del usuario que no esté en la lista canónica del skill.

**Resultado:** un usuario de Obsidian que escribe su bosquejo con tags y demás puede pasarlo al skill, y la versión que va al repo conserva sus tags **y además** lleva los metadatos canónicos del skill. Su workflow Obsidian no se rompe.

**Excepción:** si el frontmatter del usuario tiene un campo con el mismo nombre que uno canónico del skill pero con valor distinto, **gana el del skill** (pero registrar en el reporte la sobrescritura para transparencia).

### 8. Generación de la SPA HTML

Producir el `.html` siguiendo:
- Header con comentario AGPL-3.0 (`license-attribution.md` § 1).
- Las 24 reglas de doctrine.md.
- Paleta del paso 5.
- Identidad visual del paso 4.
- 4 modos: presentation, screen, control, print, con la selección de modo de § "Modos de la SPA generada": el selector arranca el modo sin navegar ni recargar.
- Cliente MQTT mínimo escrito a mano para sync screen↔control, con reloj lógico (mismo §).
- Mode selector con footer de licencia (`license-attribution.md` § 2).
- Modo print con bloque info al final (`license-attribution.md` § 3).
- **No copiar el bosquejo literalmente** — diseñar como recurso memorístico (regla principal).

#### Imágenes (si el sermón las usa)

**Nunca escribir un string base64 como parte de mi salida.** Una imagen de 90 KB son ~123.000 caracteres: es desperdicio y es imposible transcribirlo sin corromper el archivo.

En el HTML escribo un placeholder, y un script hace la inyección vía Bash:

```js
const IMAGES = {
  portada: '{{IMG:portada}}',
};
```

```bash
python3 scripts/optimize-image.py FUENTE.jpg --mode bg \
  --out $IMGS/$N-portada.webp --credit "generada con IA"
python3 scripts/optimize-image.py --inject SALIDA.html --key portada \
  --image $IMGS/$N-portada.webp
python3 scripts/optimize-image.py --check SALIDA.html
```

Perfiles: `bg` (fondo bajo scrim, ~32 KB), `fg-half` y `fg-third` (imagen al frente, ~55/30 KB). **Correr siempre `--check` antes de reportar al usuario**: un placeholder sin inyectar deja la lámina sin imagen.

Registrar la procedencia de cada imagen con `--credit` y llevarla al bloque de atribución (`license-attribution.md` § 6). Detalle completo en `image-pipeline.md`.

#### Rendering de la aplicación (estructura v4: 1 frase guía + 3 expresiones)

Cuando la aplicación sigue la estructura canónica v4 (frase guía + 3 expresiones bajo un eje), generar **5 slides** en este orden:

| # | Tipo | Contenido |
|---|---|---|
| 1 | `application-anchor` | Frase guía centrada, gran impacto, único foco. La "una aplicación" memorable. |
| 2 | `application-step` | Expresión 1: etiqueta del eje como label pequeño arriba + acción como titular. |
| 3 | `application-step` | Expresión 2: misma estructura visual. |
| 4 | `application-step` | Expresión 3: misma estructura visual. |
| 5 | `application-recap` (opcional) | Las 3 etiquetas en compacto + la frase clave del sermón al pie. |

**Diseño de cada `application-step`:**
- Label del eje (ej. "Hacia ti", "Hoy mismo", "Mente") en sans-serif tenue, arriba.
- Acción como titular grande, serif para evocar contemplación, centrada.
- Sin números de paso visibles — la progresión la lleva el predicador, no la lámina.

**Compatibilidad con bosquejos legacy** (3 aplicaciones independientes, ej. "Jesús sana"):
- El parser detecta y remapea a la estructura v4 (ver `parser-guidelines.md` § "Compatibilidad con bosquejos legacy").
- El render visual es el mismo: 5 slides como tabla anterior.
- La frase guía se infiere del párrafo introductorio del bloque "Aplicación".
- Las 3 aplicaciones legacy se tratan como expresiones del eje `relacional`.

### 9. Topic MQTT

Generar topic único:

```
{org-handle}/sermon/{YYYY-MM-DD}/{random10}/{tipo}
```

Donde:
- `{org-handle}` es el `github_org` (en lowercase) de la entidad **donde se aloja el archivo** que se está generando. Tomado del config-local.md.
- `{random10}` es 10 caracteres aleatorios alfanuméricos (a-z, 0-9).
- `{tipo}` es `control`, `state`, `heartbeat`.

Si el sermón se duplica entre dos entidades (caso `user_also_publishes_to_primary: true`), **cada copia tiene su propio topic** (porque cada copia se sirve desde una org diferente).

### 10. Reporte y confirmación

Antes de **cualquier** acción de git:
- Mostrar al usuario un resumen completo:
  - Datos extraídos del bosquejo.
  - Decisiones tomadas (paleta, identidad, topic, filename).
  - Rutas donde se generaron los archivos.
- Pedir confirmación explícita: "¿Procedemos a commit y push, o quieres revisar/ajustar?"

### 11. Commit y push (solo tras confirmación)

Aplicar la memoria global de versionado y workflow:
- Sugerir bump SemVer (probable PATCH para nueva presentación).
- Crear commit en cada repo afectado con mensaje descriptivo.
- Tag anotado si el usuario lo pide.
- Push tras nueva confirmación.

## Estructura de archivos generados

Para un sermón cuyo predicador es el `user` del config y el lugar es una entidad `secondary` con `user_also_publishes_to_primary: true` (caso de duplicación), se generan 4 archivos:

```
<resources_root>/
├── <primary.bosquejos_dir>/
│   └── {YYYYMMDD}-{Slug}-{Nombre}-{Apellido}.md
├── <primary.presentaciones_dir>/
│   └── {YYYYMMDD}-{Slug}-{Nombre}-{Apellido}.html
├── <secondary.bosquejos_dir>/
│   └── {YYYYMMDD}-{Slug}-{Nombre}-{Apellido}.md
└── <secondary.presentaciones_dir>/
    └── {YYYYMMDD}-{Slug}-{Nombre}-{Apellido}.html
```

Las copias del bosquejo entre las dos entidades son **idénticas en contenido**, solo difieren en el campo `repo` del frontmatter. Las SPAs difieren en topic MQTT, footer de atribución, y `ORG_GITHUB_URL` — cada una refleja la entidad donde se aloja.

## Modos de la SPA generada

La proyección siempre sale de una PC en modo `screen` (cabina). El `control` tiene que funcionar desde esa misma PC, desde otra PC o desde un teléfono o tablet. En Android, el HTML abierto desde WhatsApp o Descargas llega como `content://`.

El modo se indica con `#modo` al final de la URL (`sermon.html#control`) o con `?mode=modo`. Si vienen ambos, gana `?mode=`.

| Modo | Comportamiento |
|---|---|
| (sin modo) | Menú selector + footer de licencia |
| `presentation` | Vista standalone, sin red. Para revisar o compartir. Alias: `standalone` |
| `screen` | Cabina. Recibe comandos de control vía MQTT, pantalla limpia para proyección. Solo PC |
| `control` | Control. Envía comandos al screen, ve notas/cronómetro/preview de siguiente slide. PC o móvil |
| `print` | Vista print-friendly: todas las slides en flujo + bloque info al final + botón "Imprimir / Guardar PDF" (NO auto-print). El usuario revisa antes de invocar `window.print()` |

### Selección de modo

Toda SPA cumple estas reglas, venga su motor de `reference-example.html` o de una presentación anterior:

1. **Al cargar**, el modo sale de `?mode=` si es válido; si no, de `#modo`; si no, de `history.state.sermonMode`. Sin ninguno, se muestra el selector.
2. **El selector arranca el modo en la misma página.** Nunca `location.search = …`, `location.href = …` ni `location.hash = …`. En Android, Chrome le pasa al proveedor de contenido la URL completa, con `?` y `#`, y el permiso que dan WhatsApp o el gestor de archivos cubre solo la URI exacta: cualquier carga nueva con algo agregado termina en «archivo no encontrado».
3. **Al elegir, el modo se anota como entrada nueva del historial** (`history.pushState`): en `file:` y `http(s):`, con `#modo` en la URL; en `content:`, sin tocar la URL, solo en el estado. Así la recarga conserva el modo y Atrás vuelve al selector.
4. **Volver al selector:** botón sobrio «‹ Modos» en `control` y en la barra de `print` (no en `screen` ni en `presentation`, que se proyectan limpios), además de Atrás. Los dos cargan la URL original, sin nada agregado: si el modo vino del selector, `history.back()`; si no, se quita `#modo` (o `?mode=`, que solo se usa en PC) y se recarga. Es la única recarga permitida: en `content://` es la misma URI que abrió el usuario.
5. **Sincronización con reloj lógico:** cada cambio local usa `ts = Math.max(Date.now(), ts + 1)`, y un estado entrante se aplica solo si su `ts` es mayor. Así un teléfono con el reloj atrasado respecto a la PC no queda ignorado.
6. **`localStorage` y `sessionStorage`**, si se usan, siempre dentro de `try/catch`: en `content://` pueden no estar disponibles.
7. **Los atajos de depuración** (`?mode=preview&slide=N&step=M`) quedan solo por query: son para herramientas de escritorio.

Antes de reportar, este grep sobre la SPA generada debe salir vacío:

```bash
grep -nE "location\.(search|href|hash)\s*=[^=]|searchParams\.set\(\s*['\"]mode" SALIDA.html
```

## Cronómetro del modo control — política

El cronómetro del modo `control` cambia de color según el tiempo transcurrido:

| Tramo | Color | CSS class |
|---|---|---|
| 0:00 → 30:00 | **Verde** (`#4ADE80`) | `.good` |
| 30:01 → 35:00 | **Anaranjado** (`#FB923C`) | `.warn` |
| 35:01 → ∞ | **Rojo** (`#EF4444`) | `.danger` |

Razón de los umbrales: el `user` del config típicamente apunta a 30 min; predicadores invitados o de equipo extendido pueden llegar a 35-45 min. Verde es zona segura, naranja es alerta amable, rojo es señal de cierre urgente. Constantes en JS: `TIMER_GREEN_UNTIL_SECS = 30 * 60`, `TIMER_ORANGE_UNTIL_SECS = 35 * 60`. Estos defaults pueden ser override-eados desde `config-local.md` en versiones futuras del skill (ver Roadmap).

## Lo que NO debo hacer

1. **NO commitear ni pushear** sin confirmación explícita del usuario en el turno actual.
2. **NO modificar el contenido del bosquejo** más allá de:
   - Convertir formato a markdown.
   - Limpiar caracteres mal codificados (mojibake).
   - Agregar frontmatter y bloque de licencia.
3. **NO inventar datos faltantes**. Si el predicador, fecha, lugar o pasaje no están claros, preguntar.
4. **NO copiar el bosquejo en la SPA literalmente**. La SPA es recurso memorístico, no documento.
5. **NO hacer auto-print en el modo `print`**. El usuario debe poder revisar primero.
6. **NO mezclar identidades**. Cuando un sermón se publica en dos entidades, cada copia tiene SU footer y SU URL — la del repo donde físicamente se aloja.
7. **NO cambiar de modo navegando a una URL con algo agregado** (`?mode=`, `#modo`). El selector arranca el modo en la misma página (§ "Selección de modo"); si navega, en Android la SPA no pasa del selector.

## Roadmap del skill

Las mejoras pendientes viven en [`ROADMAP.md`](./ROADMAP.md); lo ya entregado, en [`CHANGELOG.md`](./CHANGELOG.md). No hace falta leerlos para generar un sermón.

## Lo que SÍ debo hacer

1. Aplicar las 24 reglas de doctrine.md sin excepciones (salvo flag al usuario).
2. Verificar contraste real de la paleta resultante.
3. Validar que las fuentes seleccionadas tengan glifos completos del español.
4. Reportar todas las decisiones al usuario con transparencia.
5. Estar dispuesto a iterar — el usuario puede pedir cambios visuales o estructurales antes del commit.
6. Sugerir el bump SemVer adecuado al final (PATCH/MINOR/MAJOR según el cambio).

## Si la entidad no se reconoce

Modo fallback adaptativo:
- Generar con `default` (paleta neutra, sin logo).
- En el reporte: ofrecer registrar la entidad para futuros sermones.
- No detener el flujo.

---

<small>

**Skill:** /sermon — generador de presentaciones homiléticas
**Autor del skill:** Jonathan Ricardo Proaño Alcívar (Parlox), con asistencia de IA Claude (Anthropic).
**Licencia del skill:** AGPL-3.0-or-later (todo el skill — documentos y código que genera).
**Licencia del bosquejo .md generado:** CC BY-SA 4.0 (contenido es obra del predicador, no del skill).
**Licencia de la SPA HTML generada:** AGPL-3.0-or-later (programa ejecutable).
**Repo:** https://github.com/CafecitoTeologico/ct-skill-sermon

</small>
