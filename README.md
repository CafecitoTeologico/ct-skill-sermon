# 📖 /sermon — Skill de Claude Code para presentaciones homiléticas

[![License: AGPL-3.0-or-later](https://img.shields.io/badge/license-AGPL--3.0--or--later-blue.svg)](https://www.gnu.org/licenses/agpl-3.0.html)
[![Version](https://img.shields.io/github/v/tag/CafecitoTeologico/ct-skill-sermon?label=version)](https://github.com/CafecitoTeologico/ct-skill-sermon/tags)
[![Claude Code skill](https://img.shields.io/badge/Claude%20Code-skill-7857FF.svg)](https://claude.com/claude-code)
[![Idioma](https://img.shields.io/badge/idioma-espa%C3%B1ol-yellow.svg)](#)

> Convierte un bosquejo de sermón en una presentación SPA autocontenida con sincronización MQTT (cabina ↔ predicador), un bosquejo limpio en markdown y vista print-friendly para PDF — en un solo comando: **`/sermon`**.

---

## ✨ Qué hace

- 📝 **Recibe un bosquejo** en cualquier formato: `.md`, `.docx`, `.pdf`, `.odt`, `.txt` o texto pegado.
- 🧠 **Extrae datos** automáticamente: título, predicador, lugar, fecha, pasaje, tema, propósito, cuerpo, aplicación, frase clave.
- 🎨 **Aplica una paleta visual** según el tema del sermón — 8 paletas predefinidas (gracia, esperanza, juicio, misión, pasión, pentecostés, sabiduría, default).
- 🖼 **Detecta identidad institucional** (logos, colores) desde una carpeta de assets local.
- 📤 **Genera 2 archivos por entidad destino:**
  - `bosquejo.md` limpio con frontmatter + licencia **CC BY-SA 4.0**.
  - `presentacion.html` SPA autocontenida con licencia **AGPL-3.0**.
- 🔄 **Si el sermón aplica a más de una entidad** (p. ej. tu marca personal + tu iglesia local), genera copias diferenciadas para cada repo, con su propia atribución y topic MQTT.

## 🖥 Modos de la presentación SPA

| Modo | Para qué sirve |
|---|---|
| 📺 `?mode=presentation` | Vista standalone, sin red. Para revisar o compartir. |
| 🎬 `?mode=screen` | Pantalla de cabina. Recibe comandos vía MQTT, proyecta. |
| 🎛 `?mode=control` | Control del predicador. Notas, cronómetro, próxima slide. |
| 🖨 `?mode=print` | Vista lineal para imprimir o exportar PDF nativo. |

Sin frameworks, sin librerías. Cliente MQTT 3.1.1 escrito a mano sobre WebSocket Secure (broker público HiveMQ por defecto).

## 🚀 Instalación

```bash
# 1. Clona el repo donde gustes (carpeta de proyectos, workspace, etc.)
git clone https://github.com/CafecitoTeologico/ct-skill-sermon.git

# 2. Symlink al directorio de skills de Claude Code
ln -s "$(pwd)/ct-skill-sermon" ~/.claude/skills/sermon

# 3. Copia el template de configuración
cd ct-skill-sermon
cp config-local-example.md config-local.md

# 4. Edita config-local.md con tus datos
$EDITOR config-local.md
```

## ⚙ Configuración

`config-local.md` (gitignored, vive solo en tu máquina) define:

- 📂 **`resources_root`** — directorio donde guardas tus bosquejos, presentaciones y assets.
- 👤 **`user`** — datos del autor de la SPA: nombre, email, GitHub handle, versión bíblica preferida.
- ⛪ **`entities`** — iglesias, ministerios o contextos donde predicas, con sus directorios de output, GitHub org, y reglas de duplicación entre entidades.

Ver [`config-local-example.md`](./config-local-example.md) para schema completo + ejemplos de uso single-entity y multi-entity.

> 💡 Si invocas `/sermon` sin haber creado tu `config-local.md`, Claude te ofrece dos opciones: (a) crearlo conversando contigo, o (b) que lo copies y edites tú.

## 🪄 Uso

Una vez instalado y configurado, en Claude Code:

```
/sermon
```

Adjuntas o pegas tu bosquejo. El skill:

1. 📋 Lee tu `config-local.md`.
2. 🔍 Parsea el bosquejo (estructura canónica + heurística adaptativa).
3. 🎯 Detecta entidad destino por el campo `At:` del bosquejo.
4. 🎨 Propone paleta temática según el contenido del sermón.
5. 📝 Genera los archivos en sus directorios destino.
6. ✅ Te muestra resumen y **pide confirmación**.
7. 📤 Solo tras tu OK explícito, hace commit/push.

## 📚 Estructura del repo

| Archivo | Rol |
|---|---|
| [`SKILL.md`](./SKILL.md) | Punto de entrada del skill — instrucciones para Claude. |
| [`doctrine.md`](./doctrine.md) | Las 24 reglas no negociables de diseño visual homilético. |
| [`parser-guidelines.md`](./parser-guidelines.md) | Cómo extraer estructura del bosquejo (canónica + heurística). |
| [`theme-mapping.md`](./theme-mapping.md) | Las 8 paletas temáticas + lógica de selección. |
| [`identity-discovery.md`](./identity-discovery.md) | Cómo encontrar logos/paletas institucionales en assets. |
| [`license-attribution.md`](./license-attribution.md) | Templates de bloques de atribución (placeholders dinámicos). |
| [`reference-example.html`](./reference-example.html) | Output validado real (sermón "Jesús sana, sin importar las etiquetas"). |
| [`config-local-example.md`](./config-local-example.md) | Template público de configuración. |
| `config-local.md` | Tu configuración local (gitignored, no en este repo). |
| [`licenses/`](./licenses) | Textos canónicos AGPL-3.0 y CC BY-SA 4.0 listos para vincular en repos hijos. |

## 🎓 Doctrina visual

24 reglas no negociables, basadas en research de Reynolds, Duarte, Mayer y Tufte, contextualizadas al uso pastoral evangélico hispanoamericano. Algunas:

- 👁 Contraste objetivo 7:1 (mínimo aceptable 4.5:1).
- 🔠 Tipografía 32-40pt cuerpo, default 36pt.
- ✂ Máximo 20 palabras por slide (ideal < 10).
- 📜 Serif para citas bíblicas, sans para resto.
- 🚫 Sin blanco puro como fondo, sin animaciones decorativas.
- ✅ Glifos completos del español obligatorios (ñ, tildes, ¿, ¡).
- 🌒 Paleta luminous-dark — oscuro elegante, nunca opresivo.

Las 24 completas en [`doctrine.md`](./doctrine.md).

## 📜 Licencia

| Componente | Licencia |
|---|---|
| **Skill (este repo)** | [AGPL-3.0-or-later](https://www.gnu.org/licenses/agpl-3.0.html) |
| **Presentaciones SPA HTML generadas** | AGPL-3.0-or-later (programa derivado) |
| **Bosquejos `.md` generados** | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) (contenido del predicador) |

Software libre. Si modificas el skill o lo sirves a través de una red, debes liberar el código fuente bajo la misma licencia.

## 🛣 Roadmap

- 📱 Compatibilidad móvil para los modos `presentation` y `print`.
- 📋 Plantilla v5 de bosquejo (refinada tras uso real en sermones).
- 🎓 Skill hermano `/clase-biblica` (presentaciones para enseñanza didáctica).
- 👥 Skill hermano `/reunion-ministerial` (presentaciones de decisiones para liderazgo pastoral).
- ✍️ Skill hermano `/bosquejo` (asistente para redactar bosquejos siguiendo la plantilla v4/v5).
- ⏱ Cronómetro adaptativo con umbrales configurables por predicador.

## 🙏 Créditos

Skill creado por **Jonathan Ricardo Proaño Alcívar** ([@parlox](https://github.com/parlox)) con asistencia de IA **Claude** (Anthropic).

Inspirado por la necesidad pastoral del equipo de predicación de [Iglesia Alianza República](https://github.com/AlianzaRepublica) y la marca teológica de [Cafecito Teológico](https://github.com/CafecitoTeologico).

> *"Cristo no te llama por la etiqueta que otros te pusieron; te llama por la identidad que Él vino a restaurar."*
> — Frase clave de [`reference-example.html`](./reference-example.html)

---

<sub>📍 Compatible con [Claude Code](https://claude.com/claude-code) · Bajo licencia AGPL-3.0-or-later</sub>
