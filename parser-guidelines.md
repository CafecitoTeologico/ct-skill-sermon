# Parser guidelines — extracción de datos del bosquejo

Guía de cómo extraer información estructurada de un bosquejo entrante, con heurísticas adaptativas para bosquejos no estandarizados.

## Estrategia general

1. Intentar primero el **parsing estructurado** (estructura canónica recomendada — ver "Plantilla canónica" abajo).
2. Si la estructura no coincide, aplicar **parsing heurístico** (patrones genéricos de bosquejo homilético).
3. Si datos críticos faltan, **preguntar al usuario** antes de seguir.

## Plantilla canónica

La estructura recomendada del skill (versión v4) está documentada en una plantilla que el usuario puede mantener en su `<resources_root>` (típicamente bajo `<resources_root>/recursos/` o equivalente). Si el usuario quiere una copia base, el skill puede ofrecerle generarla siguiendo este resumen:

```markdown
# "Título del sermón"

By: Nombre Completo del Predicador
At: Lugar de predicación
On: DD de mes, YYYY

## (Opcional) Enfoque homilético
[Acentos doctrinales seleccionados]

## Pasaje bíblico: **Libro Capítulo:Versículos**

Pasajes paralelos: ...
Textos para referencias: ...

## Tema
[3-4 líneas que condensan el mensaje]

## Propósito
[Una frase: verbo de cambio + área + para + resultado pastoral]

## Introducción
[Texto memorizable, 1-3 min]

## Cuerpo del mensaje

### I. [Idea principal 1] (vv. ...)

1. **[Idea secundaria 1.1]**
   a) [Subordinada]
   b) [Subordinada]
   c) [Subordinada]
2. **[Idea secundaria 1.2]**
   a) [...]
   b) [...]
   c) [...]
3. **[Idea secundaria 1.3]**
   ...

### II. [Idea principal 2] (vv. ...)
   [Misma estructura, simétrica con I]

### III. [Idea principal 3] (vv. ...)
   [Misma estructura, simétrica con I y II]

## Transición a la conclusión
[Puente breve]

## Conclusión
[Síntesis memorable, 10-15% del sermón]

## Aplicación / Call to Action

[Frase guía única que captura "la una aplicación"]

**Pasos / Expresiones (eje: [temporal | relacional | vertical | antropológico | vocacional | otro]):**

1. **[Etiqueta 1]:** [acción concreta]
2. **[Etiqueta 2]:** [acción concreta]
3. **[Etiqueta 3]:** [acción concreta]

## Frase clave del sermón

[Frase lapidaria, memorable, anchor único]
```

## Reglas de extracción — emoji-agnóstico

**Los emojis en headings son decorativos.** El parser los ignora y matchea por el **texto del heading** (case-insensitive, tolerante a espacios). Esto permite que el predicador cambie emojis sin romper el parser.

### Datos de cabecera

| Campo | Selector | Valor a extraer |
|---|---|---|
| `title` | `# "..."` (primer h1) | Texto entre comillas |
| `preacher` | Línea `By:` | Todo después del `:` |
| `at` | Línea `At:` | Todo después del `:` |
| `date` | Línea `On:` | Texto en formato "DD de mes, YYYY" → convertir a ISO `YYYY-MM-DD` |
| `enfoque` | h2 que contenga `Enfoque homilético` (con o sin emoji, opcional) | Texto del bloque |
| `passage` | h2 que contenga `Pasaje bíblico` | Texto entre `**...**` o tras `:` |
| `passage_parallel` | Línea `Pasajes paralelos:` | Resto de la línea |
| `passage_references` | Línea `Textos para referencias:` o `Textos de referencia:` | Resto de la línea |

### Datos de cuerpo (matching por texto, ignorar emojis)

| Campo | Heading match (case-insensitive, sin emojis) |
|---|---|
| `theme` | `Tema` |
| `purpose` | `Propósito` o `Proposito` |
| `introduction` | `Introducción` o `Introduccion` |
| `body_points` | `Cuerpo del mensaje` o `Cuerpo` |
| `transition` | `Transición a la conclusión` o `Transición` |
| `conclusion` | `Conclusión` o `Conclusion` |
| `application` | `Aplicación` o `Aplicación / Call to Action` o `Call to Action` |
| `key_phrase` | `Frase clave` o `Frase clave del sermón` |

### Estructura del cuerpo (`body_points`)

Aceptar dos formatos para el body:

**Formato v4 canónico (preferido):**

```markdown
### I. Título idea principal
1. **Idea secundaria 1.1**
   a) Subordinada
   b) Subordinada
2. **Idea secundaria 1.2**
   ...
```

**Formato legacy (Jesús sana 2026-05-03, también válido):**

```markdown
### I. Título idea principal
#### 1. Idea secundaria 1.1
a) Subordinada
b) Subordinada
#### 2. Idea secundaria 1.2
...
```

El parser detecta cualquiera de los dos. Idea principal = h3 con romano (I., II., III.). Idea secundaria = lista numerada o h4. Subordinadas = items con `a)`, `b)`, `c)`.

### Validación de simetría

Después de parsear el cuerpo, **validar simetría**:

- Contar ideas secundarias en cada I/II/III. Si los conteos difieren, reportar al usuario.
- Contar subordinadas en cada idea secundaria. Si difieren dentro de una principal, reportar.

Mensaje al usuario si hay asimetría:

```
⚠ Asimetría detectada en el cuerpo del bosquejo:
  - I tiene 3 ideas secundarias.
  - II tiene 2 ideas secundarias.
  - III tiene 3 ideas secundarias.

Tu plantilla canónica pide simetría (mismo número de ideas en cada principal).
¿Quieres revisarlo antes de generar la presentación, o procedemos con la asimetría tal cual?
```

No bloquea — solo reporta. El predicador puede tener razón para una asimetría intencional.

### Aplicación — extracción

La aplicación tiene dos componentes:

1. **Frase guía:** primer párrafo después del heading `Aplicación`. Es la "una aplicación" memorable.
2. **Pasos / Expresiones:** lista numerada de 3 ítems, cada uno con etiqueta + acción.

**Detección del eje:**

Buscar en la línea introductoria de los pasos un patrón como `(eje: temporal)` o `(eje: relacional)`. Si no aparece, **inferir el eje** del contenido de las etiquetas:

| Etiquetas detectadas | Eje inferido |
|---|---|
| "Hoy", "Esta semana", "En X días", fechas o plazos | `temporal` |
| "Hacia ti", "Hacia X", "Yo / cercano / mundo" | `relacional` |
| "Con Dios", "Con otros", "Vertical / horizontal" | `vertical` |
| "Mente", "Corazón", "Voluntad", "Pensar / sentir / hacer" | `antropológico` |
| "Personal", "Familiar", "Comunitario", "Casa / trabajo / iglesia" | `vocacional` |
| (no encaja claro) | `otro` (contextual al sermón) |

El eje se almacena en frontmatter del bosquejo como `application_axis: <eje>` y se usa en la SPA para renderizar las 3 expresiones con consistencia visual.

### Compatibilidad con bosquejos legacy (3 aplicaciones independientes)

Algunos bosquejos previos a la plantilla v4 usan **3 aplicaciones independientes** en lugar de la estructura "1 frase guía + 3 expresiones". El parser debe:

- Si detecta el patrón legacy (3 aplicaciones independientes con sus propios títulos como `**1. Acción A...**`, `**2. Acción B...**`, etc.), tratarlas como 3 expresiones bajo un eje inferido del contenido (típicamente `relacional` cuando son acciones hacia distintos sujetos, o `temporal` cuando hay plazos en cada acción).
- Inferir una frase guía a partir del párrafo introductorio del bloque "Aplicación".
- Reportar al usuario el remap: "Convertí 3 aplicaciones independientes a la estructura v4 (1 frase + 3 expresiones, eje X). ¿Confirmas o ajustas?"

### Frase clave del sermón

**Sección obligatoria** en v4. El parser:

- Busca `# Frase clave del sermón` (h1) o `## Frase clave del sermón` (h2). Acepta ambos.
- Si la sección está, extrae la primera línea no vacía como `key_phrase`.
- Si la línea empieza con `- [*]` (formato Obsidian de "tarea destacada"), extraer todo lo que sigue.
- Si la sección NO existe, **preguntar al usuario** antes de generar la SPA: "No encontré frase clave del sermón. Es la frase única, lapidaria y memorable del sermón. ¿Cuál es?"

### Heurística de detección de versión bíblica

Buscar en `passage` o en citas dentro del bosquejo el sufijo de traducción:

- `(NTV)` → Nueva Traducción Viviente
- `(RV60)` o `(RVR1960)` → Reina-Valera 1960
- `(LBLA)` → La Biblia de las Américas
- `(NVI)` → Nueva Versión Internacional
- `(DHH)` → Dios Habla Hoy
- `(BLPH)` o `(BLP)` → La Palabra (Hispanoamérica)

Si no hay marcador explícito en el bosquejo:

- **Si predicador = `user.full_name` del config-local.md** → asumir `user.preferred_bible_version`.
- **Si predicador = otro** → asumir `user.default_others_bible_version` del config-local.md.
- **En cualquier caso, confirmar con el usuario antes de generar la SPA.**

## Estructuras alternativas (heurística adaptativa)

Si el bosquejo no sigue la plantilla canónica, aplicar estas heurísticas:

### A) Bosquejo en Word/PDF convertido

- Si entra como `.docx`, `.pdf`, `.odt`: convertir a markdown primero (usar `pandoc` vía Bash si está disponible, o conversión manual asistida).
- Una vez en markdown, aplicar las reglas estructuradas o heurísticas.

### B) Bosquejo en texto plano

- Buscar líneas que parezcan títulos (cortas, sin punto final, en mayúsculas o capitalizadas).
- Buscar referencias bíblicas con regex: `\b(?:[1-3]\s?)?(?:[A-Záéíóúñ]+)\s\d+:\d+(?:[–\-]\d+)?(?:\s*\([A-Z]+\))?\b`
- Identificar listas numeradas o con bullets como puntos del cuerpo o aplicaciones.

### C) Bosquejo "estilo libre"

- Si el predicador escribe párrafos sin estructura clara, intentar identificar:
  - **Tema** (primer párrafo o párrafo más declarativo).
  - **Pasaje principal** (primera referencia bíblica).
  - **Aplicaciones** (frases en imperativo o verbos en 2da persona).
- Si la confianza es baja, mostrar al usuario lo extraído y pedir validación.

### D) Datos ausentes

Si después del parsing falta alguno de estos campos críticos, **preguntar al usuario antes de generar**:

- Predicador (si no está en By:)
- Fecha (si no está en On:)
- Lugar (si no está en At:) — necesario para identidad visual
- Pasaje bíblico (si no se identifica ninguna referencia)
- Versión bíblica (si las citas no llevan abreviatura y el predicador no coincide con `user.full_name` del config)
- **Frase clave del sermón** (sección obligatoria en v4 — preguntar si no está)

Datos no críticos (tema, propósito, etc.) pueden inferirse del cuerpo del bosquejo sin preguntar, anotando los valores asumidos en el reporte de generación.

## Tabla de transliteración para slugs

Para generar el filename, transliterar el título así:

| Carácter | Reemplazo |
|---|---|
| á, à, ä, â | a |
| é, è, ë, ê | e |
| í, ì, ï, î | i |
| ó, ò, ö, ô | o |
| ú, ù, ü, û | u |
| ñ | n |
| ¿, ?, ¡, ! | (eliminar) |
| , : ; . | (eliminar) |
| `"`, `'`, `"`, `"`, `'`, `'`, `«`, `»` | (eliminar) |
| espacio | guion `-` |
| Otros símbolos | (eliminar) |

Capitalización: cada palabra empieza en mayúscula. Conectores cortos (`de`, `la`, `el`, `los`, `las`, `un`, `una`, `y`, `o`, `con`, `sin`, `por`, `para`, `en`, `a`) **se mantienen en minúscula** salvo si son la primera palabra.

Ejemplo:
- Título: `"Jesús sana, sin importar las etiquetas"`
- Slug: `Jesus-Sana-Sin-Importar-Las-Etiquetas`

(Nota: en este caso "Sin", "Las" inician con mayúscula por convención visual, no por ser inicial de oración. Cuando hay duda, **preferir capitalizar palabras cortas dentro del slug** porque mejora la legibilidad del filename.)

## Convención de filename completa

```
{YYYYMMDD}-{Slug}-{Nombre}-{Apellido}.{ext}
```

- `{YYYYMMDD}`: fecha sin guiones (ej. `20260503`).
- `{Slug}`: título transliterado en kebab-case capitalizado (ej. `Jesus-Sana-Sin-Importar-Las-Etiquetas`).
- `{Nombre}`: primer nombre transliterado (ej. `Juan` — un solo nombre, no `Juan-Carlos`).
- `{Apellido}`: primer apellido transliterado (ej. `Perez` — un solo apellido, sin tildes ni ñ).
- `{ext}`: `html` para SPA, `md` para bosquejo.

Ejemplo de filename: `20260601-La-Gracia-Que-Restaura-Juan-Perez.html`

## Decisión de destino (a qué repos va el output)

La lógica usa los `entities` definidos en `config-local.md` y los matches del campo `At:` del bosquejo:

| Predicador detectado | Lugar detectado (matchea `aliases` de) | Repos destino (bosquejos + presentaciones de cada) |
|---|---|---|
| `user.full_name` del config | Entidad con `role: secondary` y `user_also_publishes_to_primary: true` | Repos de la entidad `primary` + repos de la `secondary` → 4 archivos |
| `user.full_name` | Entidad con `role: primary` | Solo repos de la `primary` → 2 archivos |
| `user.full_name` | Entidad `guest` o lugar no registrado | Solo repos de la `primary` → 2 archivos (a menos que el usuario indique lo contrario) |
| Otro predicador | Entidad reconocida (cualquier role) | Solo repos de esa entidad → 2 archivos |
| Otro predicador | Lugar no reconocido | Preguntar al usuario |

## Detección de "lugar"

Heurísticas para identificar el lugar a partir del campo `At:`:

1. Iterar sobre `entities` del config-local.md.
2. Para cada entidad, comparar `At:` (case-insensitive, normalizando tildes) contra:
   - `entity.name` (nombre completo)
   - `entity.aliases` (lista de variantes)
3. Primer match gana. Reportar al usuario qué entidad fue detectada antes de generar.
4. Si una entidad tiene `parent` (subgrupo), heredar identidad visual del padre si la propia no existe.
5. Si ningún match → modo fallback neutro + preguntar al usuario si quiere registrar la entidad para futuras presentaciones (ver `identity-discovery.md` § "Reportar decisiones al usuario").

---

<small>

**Skill:** /sermon — generador de presentaciones homiléticas
**Autor del skill:** Jonathan Ricardo Proaño Alcívar (Parlox), con asistencia de IA Claude (Anthropic).
**Licencia del skill:** AGPL-3.0-or-later (todo el skill — documentos y código que genera).
**Licencia del bosquejo .md generado:** CC BY-SA 4.0 (contenido es obra del predicador, no del skill).
**Licencia de la SPA HTML generada:** AGPL-3.0-or-later (programa ejecutable).
**Repo:** [pendiente — aún no publicado]

</small>
