# Theme mapping — selección de paleta según el tema del bosquejo

Esta guía define **cómo elegir la paleta visual** de la presentación a partir del análisis temático del bosquejo. La paleta debe adaptarse coherentemente al tema, manteniendo modernidad, legibilidad y reverencia, sin "alocarse" ni desordenarse (regla 13 de doctrina).

## Principio rector

> El tema oscuro nunca debe sentirse "tinieblas". Siempre incluye un acento luminoso que evoque presencia, gracia, o esperanza — incluso en sermones sobre juicio o sufrimiento.

Todas las paletas siguen un esquema **Luminous Dark**: fondo oscuro + texto claro + acento luminoso (oro, ámbar, marfil, perla).

## Paletas predefinidas

### `default` — Sobria reverente
Para sermones sin tema dominante claro o cuando hay duda. Default seguro.

```json
{
  "name": "default",
  "background": "#0F1419",
  "background_subtle": "#1A1F26",
  "text_primary": "#E8E5E0",
  "text_muted": "#8B8680",
  "accent_primary": "#D4A574",
  "accent_secondary": "#E6BC85",
  "accent_emphasis": "#F4D7A8",
  "scripture_serif": "Iowan Old Style, Palatino Linotype, Georgia, serif",
  "ui_sans": "Inter, system-ui, sans-serif"
}
```

### `grace` — Gracia, perdón, restauración
Sermones sobre gracia, perdón, restauración, identidad en Cristo, hijos amados. Tonos cálidos, oro suave.

```json
{
  "name": "grace",
  "background": "#1A0F0A",
  "background_subtle": "#241712",
  "text_primary": "#F5EDE0",
  "text_muted": "#A89478",
  "accent_primary": "#D4A574",
  "accent_secondary": "#E6BC85",
  "accent_emphasis": "#FFE1B0"
}
```

### `hope` — Esperanza, cielo, promesa
Sermones sobre cielo, esperanza, segunda venida, vida eterna, promesa. Tonos azul-índigo con luz dorada.

```json
{
  "name": "hope",
  "background": "#0A1428",
  "background_subtle": "#15203D",
  "text_primary": "#F0F4FA",
  "text_muted": "#94A3B8",
  "accent_primary": "#D4AF37",
  "accent_secondary": "#FFD75A",
  "accent_emphasis": "#FFF2B0"
}
```

### `judgment` — Juicio, santidad, temor reverente
Sermones sobre juicio, santidad, temor de Dios, advertencia. Tonos profundos con acento cálido (rojo borgoña controlado).

```json
{
  "name": "judgment",
  "background": "#100A0A",
  "background_subtle": "#1F1414",
  "text_primary": "#EAE0DC",
  "text_muted": "#8B7E78",
  "accent_primary": "#8B3A3A",
  "accent_secondary": "#B85E5E",
  "accent_emphasis": "#D4A574"
}
```

### `mission` — Misión, llamado, evangelismo
Sermones sobre misión, llamado, evangelismo, el Reino avanzando. Tonos verdes profundos con dorado.

```json
{
  "name": "mission",
  "background": "#0A1F1A",
  "background_subtle": "#142B26",
  "text_primary": "#E8F0EB",
  "text_muted": "#7A9588",
  "accent_primary": "#D4A574",
  "accent_secondary": "#E8C896",
  "accent_emphasis": "#A8D4B5"
}
```

### `passion` — Pasión, sacrificio, semana santa
Sermones sobre la cruz, sacrificio de Cristo, pasión, sangre redentora. Tonos profundos con acento rojo profundo (no chillón).

```json
{
  "name": "passion",
  "background": "#0E0808",
  "background_subtle": "#1C0F0F",
  "text_primary": "#EAE0DC",
  "text_muted": "#8B7E78",
  "accent_primary": "#A04545",
  "accent_secondary": "#C26060",
  "accent_emphasis": "#E8D4A8"
}
```

### `pentecost` — Espíritu Santo, Pentecostés
Sermones sobre el Espíritu, Pentecostés, dones, fuego de Dios. Tonos cálidos rojo-naranja-dorado.

```json
{
  "name": "pentecost",
  "background": "#1A0F08",
  "background_subtle": "#28180D",
  "text_primary": "#F5EAE0",
  "text_muted": "#B89878",
  "accent_primary": "#E08B3D",
  "accent_secondary": "#F0A858",
  "accent_emphasis": "#FFD08A"
}
```

### `wisdom` — Sabiduría, proverbios, sermón temático didáctico
Para enseñanza didáctica, exposición temática, libros sapienciales. Tonos azul-verdes serenos con dorado.

```json
{
  "name": "wisdom",
  "background": "#0A1A1F",
  "background_subtle": "#152A30",
  "text_primary": "#E8EFF2",
  "text_muted": "#8AA3AB",
  "accent_primary": "#D4A574",
  "accent_secondary": "#E6BC85",
  "accent_emphasis": "#A8D4D0"
}
```

## Algoritmo de selección

1. **Leer el tema y propósito del bosquejo** (campos `theme` y `purpose`).
2. **Identificar palabras clave** que matcheen con paletas:

| Palabra clave | Paleta sugerida |
|---|---|
| gracia, perdón, restaura, identidad, hijo/hija, etiqueta | `grace` |
| esperanza, cielo, eterno, promesa, futuro, segunda venida | `hope` |
| juicio, santidad, temor, advertencia, ira, pecado | `judgment` |
| misión, llamado, evangelio, Reino, ir, hacer discípulos | `mission` |
| cruz, sacrificio, pasión, sangre, sufrimiento, Calvario | `passion` |
| Espíritu, Pentecostés, fuego, dones, llenura | `pentecost` |
| sabiduría, proverbios, prudencia, consejo, enseñanza | `wisdom` |
| (ningún match claro) | `default` |

3. **Si hay múltiples matches**, priorizar el que dominen palabras del **propósito** sobre el tema. El propósito refleja el destino emocional del sermón.

4. **Reportar la decisión al usuario** antes de generar la SPA: "Detecté tema sobre `restauración e identidad`, propongo paleta `grace`. ¿Confirmas o cambias?"

5. **Si el lugar tiene paleta institucional registrada** en `assets/paleta-{org}.json`, fusionarla con la paleta temática (ver "Override institucional" abajo).

## Override institucional

Si la entidad tiene una paleta registrada en `<resources_root>/assets/paleta-{entity.slug}.json`, aplicar esta lógica:

- **Mantener:** `background`, `background_subtle`, `text_primary`, `text_muted` de la paleta temática.
- **Reemplazar (si la institución lo tiene):** `accent_primary`, `accent_secondary` con los colores institucionales.
- **Mantener:** `accent_emphasis` de la temática (preserva la "identidad emocional" del sermón).

Esto permite que la presentación se vea "de la iglesia" pero adaptada al sermón.

## Para el caso fallback (entidad no reconocida)

Usar `default` puro, sin override. Mostrar mensaje al usuario:

> "No reconocí la entidad `'X'` en assets/. Genero con paleta neutra. ¿Quieres registrar esta entidad para futuros sermones? Si sí, ¿dónde guardo su logo y cuál es su paleta?"

## Notas de uso

- Las paletas son **valores hex puros**. Cualquier transparencia o variante se computa con `color-mix()` o `rgba()` en CSS.
- Cada paleta está afinada para cumplir **regla 1** (contraste 7:1 entre `text_primary` y `background`).
- Validar siempre el contraste con [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) antes de finalizar la SPA.

---

<small>

**Skill:** /sermon — generador de presentaciones homiléticas
**Autor del skill:** Jonathan Ricardo Proaño Alcívar (Parlox), con asistencia de IA Claude (Anthropic).
**Licencia del skill:** AGPL-3.0-or-later (todo el skill — documentos y código que genera).
**Licencia del bosquejo .md generado:** CC BY-SA 4.0 (contenido es obra del predicador, no del skill).
**Licencia de la SPA HTML generada:** AGPL-3.0-or-later (programa ejecutable).
**Repo:** [pendiente — aún no publicado]

</small>
