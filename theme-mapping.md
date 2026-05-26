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

### `lament` — Lamento, duelo, Salmos imprecatorios
Sermones de lamento, duelo, dolor, "por qué Señor", quebranto. Azul nocturno con marfil cálido — no es juicio, no es default.

```json
{
  "name": "lament",
  "background": "#0B1320",
  "background_subtle": "#15203A",
  "text_primary": "#EDE8DC",
  "text_muted": "#8A95AC",
  "accent_primary": "#B89878",
  "accent_secondary": "#D4B89A",
  "accent_emphasis": "#F0E0BC"
}
```

### `joy` — Gozo, celebración, fiestas, gratitud
Sermones sobre gozo, alegría profunda, fiestas, gratitud, alabanza alegre. Ámbar puro y oro miel (distinto a `pentecost` que tira a rojo).

```json
{
  "name": "joy",
  "background": "#15110A",
  "background_subtle": "#251D10",
  "text_primary": "#F8F0DD",
  "text_muted": "#B89F76",
  "accent_primary": "#E8B842",
  "accent_secondary": "#F5CE6B",
  "accent_emphasis": "#FFE89A"
}
```

### `covenant` — Pacto, fidelidad de Dios, alianza
Sermones sobre el pacto, la fidelidad de Dios, alianza, promesa histórica. Tierra firme: arcilla rojiza y oro profundo.

```json
{
  "name": "covenant",
  "background": "#160E0A",
  "background_subtle": "#261A12",
  "text_primary": "#F0E6D8",
  "text_muted": "#A89078",
  "accent_primary": "#A85838",
  "accent_secondary": "#C47550",
  "accent_emphasis": "#DEA776"
}
```

### `kingdom` — Reino escatológico, realeza de Cristo
Sermones sobre el Reino como realidad escatológica, realeza de Cristo, trono. Púrpura profundo con oro real (distinto a `mission` que es el Reino *activo* en misión).

```json
{
  "name": "kingdom",
  "background": "#150B1F",
  "background_subtle": "#221538",
  "text_primary": "#EFE6F4",
  "text_muted": "#9A8AAB",
  "accent_primary": "#C9A14D",
  "accent_secondary": "#E0BC6F",
  "accent_emphasis": "#F5D898"
}
```

### `prayer` — Intimidad, oración, comunión
Sermones sobre oración, intimidad con Dios, comunión, contemplación, intercesión. Violeta noche con perla — quietud.

```json
{
  "name": "prayer",
  "background": "#0F0D1F",
  "background_subtle": "#1B1832",
  "text_primary": "#EBE8F0",
  "text_muted": "#9590AB",
  "accent_primary": "#B0A4C8",
  "accent_secondary": "#C9BFD9",
  "accent_emphasis": "#E8DFEC"
}
```

### `creation` — Creación, providencia, asombro
Sermones sobre Génesis 1-2, creación, providencia, asombro ante la obra de Dios, criatura. Verde bosque profundo con oro botánico (distinto a `mission` que es verde misión).

```json
{
  "name": "creation",
  "background": "#0A1810",
  "background_subtle": "#142A1F",
  "text_primary": "#E6F0E5",
  "text_muted": "#82A089",
  "accent_primary": "#C8A858",
  "accent_secondary": "#E0C476",
  "accent_emphasis": "#B4D49E"
}
```

### `prophetic` — Voz profética, oráculo, denuncia constructiva
Sermones de tono profético, oráculo, "así dice el Señor", denuncia constructiva (distinto a `judgment` que es juicio escatológico/santidad). Cobre oxidado sobre carbón.

```json
{
  "name": "prophetic",
  "background": "#14100B",
  "background_subtle": "#221B12",
  "text_primary": "#ECE2D2",
  "text_muted": "#9A8870",
  "accent_primary": "#C9743A",
  "accent_secondary": "#DC8E58",
  "accent_emphasis": "#F0B070"
}
```

### `incarnation` — Encarnación, Adviento, Navidad
Sermones sobre la encarnación, Adviento, Navidad, "el Verbo se hizo carne". Vino profundo con verde abeto controlado y oro pálido (sin cliché navideño).

```json
{
  "name": "incarnation",
  "background": "#1A0A10",
  "background_subtle": "#2A1420",
  "text_primary": "#F0E5E8",
  "text_muted": "#A88090",
  "accent_primary": "#6B8E5F",
  "accent_secondary": "#92AD86",
  "accent_emphasis": "#E8D4A0"
}
```

### `resurrection` — Pascua, vida nueva, victoria
Sermones sobre la resurrección, Pascua, vida nueva, victoria sobre la muerte, primicias. Violeta noche transitando a oro amanecer.

```json
{
  "name": "resurrection",
  "background": "#160E14",
  "background_subtle": "#281C28",
  "text_primary": "#F5EDE0",
  "text_muted": "#B8A5A0",
  "accent_primary": "#E8A050",
  "accent_secondary": "#F5C078",
  "accent_emphasis": "#FFE0A0"
}
```

### `discipleship` — Vida cristiana práctica, formación
Sermones sobre discipulado, formación, vida cristiana cotidiana, seguir a Cristo en lo ordinario. Bronce arcilla — cotidiano, no épico.

```json
{
  "name": "discipleship",
  "background": "#14110A",
  "background_subtle": "#251F12",
  "text_primary": "#E8E0CC",
  "text_muted": "#9A8868",
  "accent_primary": "#9A6D3D",
  "accent_secondary": "#BC8B52",
  "accent_emphasis": "#D4A574"
}
```

### `suffering` — Sufrimiento del creyente, Job, perseverancia
Sermones sobre el sufrimiento del creyente, Job, prueba, aflicción, perseverancia (distinto a `passion` que es el sufrimiento de Cristo). Pizarra con cobre suave y marfil — esperanza que persiste.

```json
{
  "name": "suffering",
  "background": "#0E1418",
  "background_subtle": "#1A2228",
  "text_primary": "#E5E8EA",
  "text_muted": "#7A8A92",
  "accent_primary": "#A87858",
  "accent_secondary": "#C49678",
  "accent_emphasis": "#E8D8C0"
}
```

## Variantes intra-paleta

Algunas paletas de alto tráfico tienen **variantes tonales** dentro de la misma familia temática. Cuando el bosquejo cae en una de estas familias, el predicador o el operador del skill puede elegir manualmente la variante para diferenciar dos sermones de tema cercano (p. ej. dos cultos del mismo domingo). Las variantes preservan la coherencia teológica de la familia — cambian el matiz visual, no el mensaje.

**Cómo invocarlas:** el usuario indica explícitamente la variante (`grace-jewel`, `hope-twilight`, etc.) en lugar del slug base. Si no se indica, se usa la paleta base de la familia (`grace`, `hope`, `default`, `mission`, `wisdom`).

### `grace-jewel` — variante joya de `grace`
Más profunda y rica que `grace`. Oro joya en lugar de oro suave.

```json
{
  "name": "grace-jewel",
  "background": "#1A0F0A",
  "background_subtle": "#241712",
  "text_primary": "#F5EDE0",
  "text_muted": "#A89478",
  "accent_primary": "#B8763D",
  "accent_secondary": "#D4925A",
  "accent_emphasis": "#F5C788"
}
```

### `grace-dawn` — variante alba de `grace`
Más fresca, melocotón cálido en lugar de oro miel.

```json
{
  "name": "grace-dawn",
  "background": "#1A100E",
  "background_subtle": "#251812",
  "text_primary": "#F8EDE5",
  "text_muted": "#B89A85",
  "accent_primary": "#E8A878",
  "accent_secondary": "#F5C49A",
  "accent_emphasis": "#FFDDB5"
}
```

### `hope-twilight` — variante crepúsculo de `hope`
Más violeta que el `hope` base. Azul-violeta nocturno con oro.

```json
{
  "name": "hope-twilight",
  "background": "#14102A",
  "background_subtle": "#1F1A40",
  "text_primary": "#EFEAF5",
  "text_muted": "#998AAB",
  "accent_primary": "#D4AF37",
  "accent_secondary": "#E8C766",
  "accent_emphasis": "#F8E0A8"
}
```

### `hope-ocean` — variante océano de `hope`
Más profundo, azul oceánico en lugar de azul-índigo.

```json
{
  "name": "hope-ocean",
  "background": "#08182A",
  "background_subtle": "#122638",
  "text_primary": "#EAF2F8",
  "text_muted": "#8FA8B8",
  "accent_primary": "#D4AF37",
  "accent_secondary": "#F0C95E",
  "accent_emphasis": "#FFE9A8"
}
```

### `default-stone` — variante piedra de `default`
Gris piedra cálido en lugar de carbón azulado. Mantiene la neutralidad reverente.

```json
{
  "name": "default-stone",
  "background": "#15171A",
  "background_subtle": "#21242A",
  "text_primary": "#E5E5E2",
  "text_muted": "#8A8A86",
  "accent_primary": "#B89878",
  "accent_secondary": "#CFB298",
  "accent_emphasis": "#E8D6B8"
}
```

### `default-ember` — variante brasa de `default`
Carbón con acento brasa. Para mensajes neutros que necesitan un poco más de calor.

```json
{
  "name": "default-ember",
  "background": "#120F0E",
  "background_subtle": "#1F1A18",
  "text_primary": "#E8E2DC",
  "text_muted": "#8A8278",
  "accent_primary": "#B86838",
  "accent_secondary": "#D08658",
  "accent_emphasis": "#E8B080"
}
```

### `mission-sage` — variante salvia de `mission`
Verde salvia más quieto y reflexivo (para sermones de misión contemplativos, no exhortativos).

```json
{
  "name": "mission-sage",
  "background": "#101A14",
  "background_subtle": "#1C281F",
  "text_primary": "#E5ECE5",
  "text_muted": "#8A9A88",
  "accent_primary": "#B89878",
  "accent_secondary": "#D0B898",
  "accent_emphasis": "#B8C8A8"
}
```

### `wisdom-slate` — variante pizarra de `wisdom`
Azul pizarra más sobrio que el azul-verde de `wisdom`. Para enseñanza más austera.

```json
{
  "name": "wisdom-slate",
  "background": "#0E1418",
  "background_subtle": "#1A2128",
  "text_primary": "#E5EAEF",
  "text_muted": "#889098",
  "accent_primary": "#B89878",
  "accent_secondary": "#D0B898",
  "accent_emphasis": "#A8B8C8"
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
| misión activa, llamado, evangelio, ir, hacer discípulos | `mission` |
| cruz, sacrificio, pasión de Cristo, sangre, Calvario | `passion` |
| Espíritu, Pentecostés, fuego, dones, llenura | `pentecost` |
| sabiduría, proverbios, prudencia, consejo, enseñanza didáctica | `wisdom` |
| lamento, duelo, llanto, quebranto, "por qué Señor", Salmos imprecatorios | `lament` |
| gozo, alegría, celebración, fiesta, gratitud, alabanza | `joy` |
| pacto, alianza, fidelidad de Dios, juramento, promesa histórica | `covenant` |
| Reino escatológico, realeza de Cristo, trono, Cristo Rey | `kingdom` |
| oración, intimidad, comunión, súplica, intercesión, contemplación | `prayer` |
| creación, providencia, asombro, naturaleza, Génesis 1-2, criatura | `creation` |
| profecía, oráculo, denuncia, "así dice el Señor", voz profética | `prophetic` |
| encarnación, Adviento, Navidad, Verbo, "se hizo carne" | `incarnation` |
| resurrección, Pascua, vida nueva, victoria sobre la muerte, primicias | `resurrection` |
| discipulado, formación, vida cristiana cotidiana, seguir a Cristo | `discipleship` |
| sufrimiento del creyente, Job, prueba, aflicción, perseverancia | `suffering` |
| (ningún match claro) | `default` |

3. **Si hay múltiples matches**, priorizar el que dominen palabras del **propósito** sobre el tema. El propósito refleja el destino emocional del sermón. En particular, distinguir:
   - `passion` (sufrimiento *de Cristo* en la cruz) vs. `suffering` (sufrimiento *del creyente*).
   - `judgment` (juicio escatológico/santidad de Dios) vs. `prophetic` (voz profética denunciante).
   - `mission` (Reino *avanzando* / acción evangelizadora) vs. `kingdom` (Reino como *realidad escatológica* / realeza).
   - `mission` (verde misión activa) vs. `creation` (verde creación contemplativa).
   - `pentecost` (fuego/rojo-naranja, Espíritu activo) vs. `joy` (ámbar/oro miel, gozo celebrativo).

4. **Reportar la decisión al usuario** antes de generar la SPA: "Detecté tema sobre `restauración e identidad`, propongo paleta `grace`. ¿Confirmas o cambias?"

5. **Si el usuario quiere una variante intra-paleta** (p. ej. dos cultos del mismo domingo con tema cercano), puede indicarlo explícitamente: `grace-jewel`, `hope-twilight`, `default-stone`, etc. Ver sección "Variantes intra-paleta" arriba. Si no se indica variante, usar la paleta base de la familia.

6. **Si el lugar tiene paleta institucional registrada** en `assets/paleta-{org}.json`, fusionarla con la paleta temática (ver "Override institucional" abajo).

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
