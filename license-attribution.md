# Bloques de atribución y licencia — templates dinámicos

Este archivo define los bloques de atribución que se insertan **dinámicamente** en cada artefacto generado por el skill. La licencia se determina por el tipo de archivo:

| Tipo de archivo | Licencia | Razón |
|---|---|---|
| HTML SPA (presentación) | **AGPL-3.0-or-later** | Software ejecutable que se sirve en red (MQTT) |
| Markdown (bosquejo) | **CC BY-SA 4.0** | Documento de contenido, no software |
| Recursos (plantillas, ensayos) | **CC BY-SA 4.0** | Documentos creativos |

## Variables a sustituir

Todas las variables se resuelven en runtime: las referidas al sermón se extraen del bosquejo, y las referidas al usuario/skill se leen de `config-local.md`.

| Variable | Origen | Ejemplo |
|---|---|---|
| `{TITLE}` | Título del bosquejo | `"La gracia que restaura"` |
| `{PREACHER}` | Campo `By:` del bosquejo (el contenido es del predicador) | `"Juan Carlos Pérez"` |
| `{AT}` | Campo `At:` del bosquejo, resuelto contra `entities` del config | `"Mi Iglesia Local"` |
| `{DATE}` | Campo `On:` del bosquejo (formato "DD de mes, YYYY") | `"03 de mayo, 2026"` |
| `{PASSAGE}` | Pasaje bíblico extraído + traducción | `"Marcos 5:21–43 (NTV)"` |
| `{SPA_AUTHOR}` | `user.full_name` del config-local.md (el programa lo creó esa persona) | `"Juan Carlos Pérez Gómez"` |
| `{SPA_AUTHOR_EMAIL}` | `user.email` del config-local.md | `"juan@example.com"` |
| `{SPA_AUTHOR_GITHUB}` | `user.github_handle` del config-local.md | `"juancarlosperez"` |
| `{ORG_GITHUB_URL}` | `entity.github_org_url` (de la entidad donde se aloja **esta copia** del archivo) | `"https://github.com/MiIglesia"` |
| `{REPO_GITHUB_URL}` | URL completa del repo donde vive este archivo (solo bosquejo md) | `"https://github.com/MiIglesia/bosquejos"` |
| `{TOPIC}` | Topic MQTT generado para este sermón (solo SPA) | `"miiglesia/sermon/2026-05-03/x7k3p9m2n1/control"` |

**Importante:** `{PREACHER}` ≠ `{SPA_AUTHOR}`. El predicador (autor del contenido del sermón) puede ser cualquier persona del equipo. El `{SPA_AUTHOR}` es siempre el `user` del config-local.md (autor del programa generador). Esta separación legal es clave para la atribución correcta.

## 1. HTML SPA — Comentario header (AGPL-3.0)

Este bloque va al inicio del archivo HTML, justo después del `<!DOCTYPE html>` y antes del `<html>`:

```html
<!--
  ============================================================================
  {TITLE}
  Presentación de sermón · Single Page Application autocontenida
  ============================================================================

  Predicación
    Pasaje:    {PASSAGE}
    Lugar:     {AT}
    Fecha:     {DATE}
    Predicador: {PREACHER}

  Programa (SPA) creado por
    {SPA_AUTHOR}
    Contacto: {SPA_AUTHOR_EMAIL} · github.com/{SPA_AUTHOR_GITHUB}
    Asistencia: Codificación asistida con IA Claude (Anthropic)
    Disponible en: {ORG_GITHUB_URL}

  Skill generador
    /sermon — generador de presentaciones homiléticas
    Provisto por: Cafecito Teológico (ministerio)
    Repositorio:  https://github.com/CafecitoTeologico/ct-skill-sermon
    Licencia:     AGPL-3.0-or-later

  Licencia del programa
    AGPL-3.0-or-later (GNU Affero General Public License v3.0 o posterior)
    https://www.gnu.org/licenses/agpl-3.0.html
    Software libre. Si lo modificas o lo sirves a través de una red,
    debes liberar el código fuente bajo la misma licencia.

  Tecnología
    HTML5 + CSS (container queries) + JavaScript vanilla
    MQTT 3.1.1 sobre WebSocket Secure (cliente mínimo escrito a mano)
    Broker: HiveMQ público (broker.hivemq.com:8884/mqtt)
    Topic:  {TOPIC}

  Modos (#modo al final de la URL, o ?mode=modo; si hay ambos, gana ?mode=)
    #presentation  → vista personal, sin red (alias: standalone)
    #screen        → cabina: la PC que proyecta, recibe el control
    #control       → controla la presentación y ve notas/cronómetro (PC o móvil)
    #print         → vista print-friendly + bloque info para PDF/papel
    (sin modo)     → menú selector de modo; se vuelve con «‹ Modos» o Atrás
  En Android (archivo abierto desde WhatsApp o Descargas) usar el menú o #modo:
  ?mode= no funciona ahí.
  ============================================================================
-->
```

## 2. HTML SPA — Footer del menú selector de modo (AGPL-3.0)

Texto pequeño, gris (`#666` sobre fondo oscuro), centrado, al pie del menú:

```html
<div class="mode-selector-footer">
  <p>
    Programa (SPA) creado por {SPA_AUTHOR}
    en base al bosquejo de {PREACHER}.<br>
    Asistido con IA Claude (Anthropic) ·
    <a href="mailto:{SPA_AUTHOR_EMAIL}">{SPA_AUTHOR_EMAIL}</a><br>
    Disponible en <a href="{ORG_GITHUB_URL}">{ORG_GITHUB_URL}</a> ·
    Licenciado bajo
    <a href="https://www.gnu.org/licenses/agpl-3.0.html">AGPL-3.0-or-later</a>
    — software libre con código abierto al servirse en red.
  </p>
  <p class="skill-attribution">
    Generado con el skill
    <a href="https://github.com/CafecitoTeologico/ct-skill-sermon">/sermon</a>
    provisto por Cafecito Teológico.
  </p>
</div>
```

**Estilo del bloque `.skill-attribution`:** una sola línea, tipografía aún más pequeña que el bloque principal (~0.85em del párrafo anterior, o `font-size: 11px`), `opacity: 0.6`, color heredado, margen superior pequeño (~6px). Es colofón discreto del programa, no protagónico — no debe competir visualmente con el bloque del SPA_AUTHOR.

> **Nota:** la formulación "en base al bosquejo de {PREACHER}" se mantiene
> incluso cuando el predicador coincide con el `user` del config (autor del programa).
> Es redundante intencional: separa explícitamente la autoría del programa
> (siempre el `user` del config-local.md) de la autoría del contenido del sermón
> (el predicador real, que puede o no ser el mismo `user`).
>
> Análogamente, la línea `.skill-attribution` separa la autoría del programa
> (siempre el `user` del config-local.md) de la herramienta usada para generarlo
> (el skill `/sermon`, provisto por Cafecito Teológico). El verbo es "generado con",
> no "creado por" — el skill es herramienta, no autor. Mismo patrón que "Asistido
> con IA Claude (Anthropic)" en la línea anterior.

## 3. HTML SPA — Bloque info del modo print (AGPL-3.0)

Al final del flujo print-friendly, antes del cierre, sirve como **colofón discreto** para impresos físicos. Estilo minimalista, no protagónico — fluye al final de la última lámina si hay espacio. NO usar `page-break-before: always`.

```html
<section class="print-license-block">
  <h2>Información de la presentación</h2>
  <table>
    <tbody>
      <tr><th>Sermón</th>     <td>{TITLE}</td></tr>
      <tr><th>Pasaje</th>     <td>{PASSAGE}</td></tr>
      <tr><th>Predicador</th> <td>{PREACHER}</td></tr>
      <tr><th>Lugar</th>      <td>{AT}</td></tr>
      <tr><th>Fecha</th>      <td>{DATE}</td></tr>
    </tbody>
  </table>
  <p class="attribution">
    Programa (SPA) creado por <strong>{SPA_AUTHOR}</strong>
    en base al bosquejo de <strong>{PREACHER}</strong>,
    con asistencia de IA Claude (Anthropic).
    Disponible en <a href="{ORG_GITHUB_URL}">{ORG_GITHUB_URL}</a>.
    Generado con el skill <a href="https://github.com/CafecitoTeologico/ct-skill-sermon">/sermon</a>
    provisto por Cafecito Teológico.
  </p>
  <p class="license">
    <strong>Licencia:</strong> AGPL-3.0-or-later
    (<a href="https://www.gnu.org/licenses/agpl-3.0.html">texto completo</a>).
    Software libre. Se permite su uso, modificación y redistribución bajo los términos
    de la GNU Affero General Public License versión 3 o posterior. Si se sirve a través
    de una red, su código fuente debe estar disponible para los usuarios bajo la misma licencia.
  </p>
</section>
```

> **Estilo del bloque print:** font-size base 9–10pt, h2 a 12pt, paddings 18–22mm, sin
> `page-break-before` (deja que fluya). Es colofón, no sección protagónica.

## 4. Markdown del bosquejo — Frontmatter y bloque (CC BY-SA 4.0)

Frontmatter al inicio del `.md` y bloque al final.

**Frontmatter:**

```yaml
---
title: "{TITLE}"
preacher: "{PREACHER}"
at: "{AT}"
date: "{DATE}"
passage: "{PASSAGE}"
language: es
license: CC-BY-SA-4.0
license_url: https://creativecommons.org/licenses/by-sa/4.0/
license_short: Uso libre con atribución y bajo la misma licencia.
attribution: "Bosquejo de {PREACHER}"
repo: {REPO_GITHUB_URL}
---
```

**Bloque al final:**

```markdown
---

<small>

**Licencia:** Creative Commons Attribution-ShareAlike 4.0 International ([CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))
Uso libre con atribución y bajo la misma licencia.

**Bosquejo de** {PREACHER}.
**Disponible en** {REPO_GITHUB_URL}.

</small>
```

## 5. Documentos del skill (este archivo y los demás)

Los documentos de este skill (`SKILL.md`, `doctrine.md`, `parser-guidelines.md`, etc.) son **parte del skill** y se publican bajo **AGPL-3.0-or-later**, igual que su código.

No confundir con el `.md` que el skill **genera**: ese es el bosquejo del predicador y va bajo **CC BY-SA 4.0** (§ 4). La distinción es entre *documentos del skill* (AGPL, son la herramienta) y *documento generado por el skill* (CC BY-SA, es obra del predicador).

Resumen de las tres licencias en juego:

| Qué | Licencia | Por qué |
|---|---|---|
| El skill: documentos y scripts | AGPL-3.0-or-later | Es la herramienta |
| La SPA HTML generada | AGPL-3.0-or-later | Es un programa ejecutable derivado del skill |
| El bosquejo `.md` generado | CC BY-SA 4.0 | El contenido es obra del predicador, no del skill |

Cada documento del skill debe terminar con:

```markdown
---

<small>

**Skill:** /sermon — generador de presentaciones homiléticas
**Autor del skill:** Jonathan Ricardo Proaño Alcívar (Parlox), con asistencia de IA Claude (Anthropic).
**Licencia del skill:** AGPL-3.0-or-later (todo el skill — documentos y código que genera).
**Licencia del bosquejo .md generado:** CC BY-SA 4.0 (contenido es obra del predicador, no del skill).
**Licencia de la SPA HTML generada:** AGPL-3.0-or-later (programa ejecutable).
**Repo:** https://github.com/CafecitoTeologico/ct-skill-sermon

</small>
```

## 6. Imágenes de terceros (bancos de imágenes, material ajeno)

Los bloques 1-3 cubren la autoría del **programa** y la licencia AGPL. **No cubren las imágenes.** Cada imagen de la SPA cae en uno de tres casos, y cada uno pide algo distinto:

| Origen | Qué hace falta | Por qué |
|---|---|---|
| **Generada con IA** | **Declararlo.** No hay autor que acreditar. | Es divulgación, no atribución: en un contexto de enseñanza, nadie debe confundir una imagen sintética con evidencia documental. |
| **Banco de imágenes** | Autor + URL | Atribución al autor real, y camino de vuelta al master. |
| **Propia o aportada en el bosquejo** | Autor conocido, o verificar con quien la aportó | No asumir que quien la entregó tiene los derechos. |

La procedencia se registra al optimizar (`optimize-image.py --credit`) y queda en `<resources_root>/assets/imagenes-sermones/credits.json`. De ahí se lleva a dos lugares:

**a) Frontmatter del bosquejo `.md`** — campo adicional a los de § 4, solo si hay imágenes:

```yaml
image_credits:
  - file: 20260601-gracia-restaura-portada.webp
    origen: generada con IA
  - file: 20260601-gracia-restaura-manos.webp
    origen: banco de imágenes
    autor: "Unsplash · Jane Doe"
    url: https://unsplash.com/photos/xyz
```

**b) Bloque de créditos de la SPA** — línea adicional dentro de `.selector-credits`, después de la licencia:

```html
<span class="sep">·</span>
Imágenes generadas con IA.
```

La línea depende de **quién puso las imágenes**. Son tres escenarios, y el skill debe detectar cuál aplica:

| Escenario | Línea en la SPA |
|---|---|
| **1. Solo generadas con IA** (el skill las produjo) | `Imágenes generadas con IA.` |
| **2. Mixtas** (IA + provistas por el predicador) | `Imágenes provistas por {PREACHER}, salvo las generadas con IA.` |
| **3. Solo provistas por el predicador** | `Imágenes provistas por {PREACHER}.` |

Si además hay imágenes de banco, agregar los autores: `Imágenes: {AUTOR_1}, {AUTOR_2}.` Con más de tres, resumir por fuente (`Imágenes: Unsplash y Pexels`) y dejar el listado completo en el frontmatter del `.md`.

**Qué hacer cuando el predicador aporta imágenes:**

1. **Preguntar el origen antes de usarlas.** "¿Es tuya, o la sacaste de algún lado?" No es burocracia: si viene de internet, el crédito y la licencia son de otro, y el repo de presentaciones es público.
2. Si es **propia del predicador** → `origen: propia`, y se acredita a su nombre solo si él lo pide.
3. Si el predicador **no sabe de dónde salió** → `origen: por verificar`. Se puede usar en la presentación del culto, pero **avisar al usuario** antes de publicarla en el repo.
4. **No mezclar sin distinguir.** En el escenario 2, el `credits.json` debe dejar claro cuál es cuál — si mañana hay que quitar una imagen por licencia, tiene que saberse cuál.

En los escenarios 2 y 3 la línea **no puede decir solo "generadas con IA"**: sería falso sobre las imágenes del predicador.

**Reglas:**

1. **Las imágenes generadas con IA se declaran, no se acreditan.** No hay autor. La línea de la SPA debe decirlo con claridad: en material de enseñanza, una imagen sintética no puede pasar por documental. Si se conoce el modelo usado, registrarlo en `credits.json`; en la SPA basta "generadas con IA".
2. **Nunca presentar una imagen de IA como registro de un hecho real.** Si el sermón ilustra un evento histórico, un lugar concreto o una persona real, usar fotografía real o no usar imagen. Este es un criterio de honestidad, no de licencia.
3. **Para banco de imágenes**, preferir licencia permisiva (Unsplash, Pexels, Pixabay) y registrar autor y URL siempre, aunque la licencia no lo exija: es lo que permite verificar o reemplazar la imagen después.
4. **Si una imagen no tiene procedencia conocida, preguntar al usuario antes de usarla.** No embeber material de origen incierto en un repo público. Que alguien la haya aportado en el bosquejo no significa que tenga los derechos.
5. Las imágenes propias del usuario o del predicador no necesitan crédito público, pero sí quedan registradas en `credits.json` con `origen: propia`.

## Notas importantes para mí (Claude) al aplicar el skill

1. **El bloque del SPA siempre dice "Programa creado por `{SPA_AUTHOR}`"** aunque el predicador sea otra persona. La autoría del programa ≠ autoría del sermón. `{SPA_AUTHOR}` viene de `user.full_name` en `config-local.md`.
2. **El bloque del bosquejo md dice el predicador real** ("Bosquejo de `{PREACHER}`"). Si el predicador coincide con el `user` del config, va su nombre igual — no decimos "Bosquejo de mí".
3. **`{ORG_GITHUB_URL}`** se determina según la entidad de la copia que se está generando:
   - Tomar `entity.github_org_url` de la entidad correspondiente al repo destino.
4. **Cuando un sermón va a 2 repos (caso `user_also_publishes_to_primary: true`)**, cada copia tiene el `{ORG_GITHUB_URL}` correspondiente a su repo. Las copias NO son idénticas — el bloque de atribución y el topic MQTT cambian.
5. **NUNCA inventes handles ni URLs**. Si un campo no está poblado en el config, detener y preguntar al usuario.
6. **La atribución del skill `/sermon` es obligatoria** en los 3 bloques (HTML header comment, footer del menú selector, print license block). El URL del repo (`https://github.com/CafecitoTeologico/ct-skill-sermon`) es constante del skill — no es variable de runtime. NUNCA omitirla. La AGPL-3.0 lo exige legalmente, y el estilo está diseñado para ser discreto (clase `.skill-attribution` en footer, frase añadida al párrafo en print) — no es opcional ni "estorba", coexiste con el crédito del `{SPA_AUTHOR}` como herramienta complementaria, no como autoría compartida.
7. **Las imágenes de banco se acreditan** (§ 6). El bloque de licencia AGPL cubre el programa, no las fotos. Si el sermón usa imágenes de terceros y no hay procedencia registrada, detener y preguntar antes de embeberlas.

---

<small>

**Skill:** /sermon — generador de presentaciones homiléticas
**Autor del skill:** Jonathan Ricardo Proaño Alcívar (Parlox), con asistencia de IA Claude (Anthropic).
**Licencia del skill:** AGPL-3.0-or-later (todo el skill — documentos y código que genera).
**Licencia del bosquejo .md generado:** CC BY-SA 4.0 (contenido es obra del predicador, no del skill).
**Licencia de la SPA HTML generada:** AGPL-3.0-or-later (programa ejecutable).
**Repo:** https://github.com/CafecitoTeologico/ct-skill-sermon

</small>
