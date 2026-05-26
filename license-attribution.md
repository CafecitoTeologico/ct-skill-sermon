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

  Modos (vía query param)
    ?mode=presentation  → vista personal, sin red (default)
    ?mode=screen        → cabina, recibe el control
    ?mode=control       → controla la presentación, ve notas/cronómetro
    ?mode=print         → vista print-friendly + bloque info para PDF/papel
    (sin parámetro)     → menú selector de modo
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

Los documentos de este skill son texto creativo que se publica bajo **CC BY-SA 4.0** cuando el skill se publique como repo independiente. Cada documento debe terminar con:

```markdown
---

<small>

**Skill:** /sermon — generador de presentaciones homiléticas
**Autor del skill:** Jonathan Ricardo Proaño Alcívar (Parlox), con asistencia de IA Claude (Anthropic).
**Licencia del skill:** AGPL-3.0-or-later (todo el skill — documentos y código que genera).
**Licencia del bosquejo .md generado:** CC BY-SA 4.0 (contenido es obra del predicador, no del skill).
**Licencia de la SPA HTML generada:** AGPL-3.0-or-later (programa ejecutable).
**Repo:** [pendiente — aún no publicado]

</small>
```

## Notas importantes para mí (Claude) al aplicar el skill

1. **El bloque del SPA siempre dice "Programa creado por `{SPA_AUTHOR}`"** aunque el predicador sea otra persona. La autoría del programa ≠ autoría del sermón. `{SPA_AUTHOR}` viene de `user.full_name` en `config-local.md`.
2. **El bloque del bosquejo md dice el predicador real** ("Bosquejo de `{PREACHER}`"). Si el predicador coincide con el `user` del config, va su nombre igual — no decimos "Bosquejo de mí".
3. **`{ORG_GITHUB_URL}`** se determina según la entidad de la copia que se está generando:
   - Tomar `entity.github_org_url` de la entidad correspondiente al repo destino.
4. **Cuando un sermón va a 2 repos (caso `user_also_publishes_to_primary: true`)**, cada copia tiene el `{ORG_GITHUB_URL}` correspondiente a su repo. Las copias NO son idénticas — el bloque de atribución y el topic MQTT cambian.
5. **NUNCA inventes handles ni URLs**. Si un campo no está poblado en el config, detener y preguntar al usuario.
6. **La atribución del skill `/sermon` es obligatoria** en los 3 bloques (HTML header comment, footer del menú selector, print license block). El URL del repo (`https://github.com/CafecitoTeologico/ct-skill-sermon`) es constante del skill — no es variable de runtime. NUNCA omitirla. La AGPL-3.0 lo exige legalmente, y el estilo está diseñado para ser discreto (clase `.skill-attribution` en footer, frase añadida al párrafo en print) — no es opcional ni "estorba", coexiste con el crédito del `{SPA_AUTHOR}` como herramienta complementaria, no como autoría compartida.

---

<small>

**Skill:** /sermon — generador de presentaciones homiléticas
**Autor del skill:** Jonathan Ricardo Proaño Alcívar (Parlox), con asistencia de IA Claude (Anthropic).
**Licencia del skill:** AGPL-3.0-or-later (todo el skill — documentos y código que genera).
**Licencia del bosquejo .md generado:** CC BY-SA 4.0 (contenido es obra del predicador, no del skill).
**Licencia de la SPA HTML generada:** AGPL-3.0-or-later (programa ejecutable).
**Repo:** [pendiente — aún no publicado]

</small>
