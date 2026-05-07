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

Si hay imágenes embebidas en el bosquejo entrante, extraerlas a `<resources_root>/<entity.bosquejos_dir>/assets/{slug}/` (donde `<resources_root>` y `<entity.bosquejos_dir>` vienen del config-local.md) y referenciarlas con paths relativos en el md.

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
- Proponer paleta predefinida (`grace`, `hope`, `judgment`, `mission`, `passion`, `pentecost`, `wisdom`, o `default`).
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
- Si vino con imágenes embebidas, las referencie con paths relativos a `assets/{slug}/`.

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
- 4 modos: presentation (default), screen, control, print.
- Cliente MQTT mínimo escrito a mano para sync screen↔control.
- Mode selector con footer de licencia (`license-attribution.md` § 2).
- Modo print con bloque info al final (`license-attribution.md` § 3).
- **No copiar el bosquejo literalmente** — diseñar como recurso memorístico (regla principal).

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

Vía query param `?mode=`:

| Modo | Comportamiento |
|---|---|
| (sin param) | Menú selector con los 4 modos + footer de licencia |
| `?mode=presentation` | Vista standalone, sin red. Para revisar o compartir |
| `?mode=screen` | Cabina. Recibe comandos de control vía MQTT, pantalla limpia para proyección |
| `?mode=control` | Control. Envía comandos al screen, ve notas/cronómetro/preview de siguiente slide |
| `?mode=print` | Vista print-friendly: todas las slides en flujo + bloque info al final + botón "Imprimir / Guardar PDF" (NO auto-print). El usuario revisa antes de invocar `window.print()` |

## Cronómetro del modo control — política

El cronómetro en `?mode=control` cambia de color según el tiempo transcurrido:

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
5. **NO usar `?mode=print` en auto-print**. El usuario debe poder revisar primero.
6. **NO mezclar identidades**. Cuando un sermón se publica en dos entidades, cada copia tiene SU footer y SU URL — la del repo donde físicamente se aloja.

## Roadmap del skill (mejoras futuras)

Mejoras pendientes, ordenadas por prioridad estimada:

### Compatibilidad móvil para `presentation` y `print`

Actualmente la SPA solo funciona correctamente en PC con orientación landscape. En móvil portrait, los modos `presentation` y `print` fallan por:
- Aspect ratio 16:9 forzado (regla 17 de doctrine.md).
- Container queries con `cqh`/`cqw` que producen escalado roto en portrait.
- Falta de breakpoint para portrait.

**Plan cuando se implemente:**
- Agregar `@media (orientation: portrait)` o `@media (max-width: 768px)` que reescale slides al viewport, no a 16:9.
- Agregar swipe táctil además del click para navegación móvil.
- Deshabilitar modos `screen` y `control` en móvil con tooltip "Solo PC" — su flujo no traduce a celular.
- Actualizar regla 17 de `doctrine.md`: "16:9 lógico canon en PC; móvil-portrait fallback de revisión, NO flujo de presentación."
- Mantener PC-landscape como **flujo principal y prioridad de diseño**.

**Estado:** roadmap. Implementar cuando aparezca un caso de uso real recurrente (alguien queriendo revisar la presentación en móvil).

### Otros pendientes

- **v5 de la plantilla de bosquejo:** consolidar v4 + iteraciones de campo, con la frase clave del sermón obligatoria y la aplicación con eje contextual probadas en sermones reales.
- **Skills hermanos:** `/clase-biblica` y `/reunion-ministerial` (sermones para enseñanza didáctica y reuniones ejecutivas), reutilizando el motor visual + MQTT del `/sermon`.
- **Skill `/bosquejo`:** ayudar a redactar bosquejos siguiendo la plantilla v4/v5. Diferente a `/sermon` que parte de bosquejo terminado.
- **Validación de simetría más rica:** además de contar ideas secundarias, comparar longitud de cada punto en palabras/oraciones para detectar desequilibrio temporal.
- **Detección de pasaje y autoaviso de versión bíblica:** si el bosquejo cita versículos sin traducción explícita, comparar con APIs públicas (RV60, NTV) y sugerir cuál coincide.
- **Cronómetro adaptativo:** umbrales (verde/naranja/rojo) configurables por predicador en el frontmatter del bosquejo (`target_minutes: 35`).

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
**Repo:** [pendiente — aún no publicado]

</small>
