# Identity discovery — descubrimiento de identidad visual institucional

Esta guía define **dónde busco logos y paletas institucionales** para aplicar identidad visual a la presentación generada.

## Ubicación canónica

Todos los assets de identidad visual viven en:

```
<resources_root>/assets/
```

Donde `<resources_root>` se define en `config-local.md` (ver `SKILL.md` § Pre-flight).

Estructura plana — **sin subcarpetas por entidad**. Los archivos se distinguen por nombres explícitos basados en el `slug` de cada entidad.

## Convención de nombres

### Logos

```
logo-{entidad-slug}.{ext}
```

- `{entidad-slug}` en kebab-case minúsculas, sin tildes ni ñ. Coincide con el campo `slug` de la entidad en `config-local.md`.
- `{ext}` preferentemente `svg` (vectorial, escala perfecto). Aceptable `png` con transparencia. Evitar `jpg`.

Ejemplos genéricos:
```
logo-mi-iglesia.svg
logo-mi-marca-personal.svg
logo-ministerio-juvenil.svg
logo-mi-iglesia-monocromo.svg     ← versión variante para fondos claros
logo-mi-iglesia-blanco.png        ← versión blanca para fondos oscuros
```

### Paletas

```
paleta-{entidad-slug}.json
```

Cuando existe, override sobre la paleta temática (ver `theme-mapping.md` § "Override institucional").

Schema esperado del JSON:

```json
{
  "name": "Mi Iglesia",
  "slug": "mi-iglesia",
  "primary": "#XXXXXX",
  "secondary": "#XXXXXX",
  "accent": "#XXXXXX",
  "logo_default": "logo-mi-iglesia.svg",
  "logo_dark_bg": "logo-mi-iglesia-blanco.png",
  "logo_light_bg": "logo-mi-iglesia-monocromo.svg"
}
```

### Tipografías custom (opcional)

Si la entidad tiene una tipografía custom embebida, va en `assets/fonts/{entidad-slug}/`:

```
assets/fonts/mi-marca/MiMarcaSerif-Regular.woff2
assets/fonts/mi-marca/MiMarcaSerif-Bold.woff2
```

Y se referencia desde el `paleta-*.json`:

```json
{
  "fonts": {
    "serif": "CafecitoSerif, Iowan Old Style, Georgia, serif",
    "sans": "Inter, system-ui, sans-serif"
  }
}
```

## Algoritmo de búsqueda

Cuando el skill identifica una entidad (regla de `parser-guidelines.md`), buscar en este orden:

### Paso 1: Resolver el slug de la entidad

Iterar sobre `entities` del `config-local.md`. Para cada entidad, comparar el campo `At:` del bosquejo (case-insensitive, normalizando tildes) contra:

- `entity.name` (nombre completo)
- `entity.aliases` (lista de variantes)

Primer match gana. El `slug` resultante es `entity.slug`.

| Caso | Acción |
|---|---|
| Match contra una entidad | Usar `entity.slug` para buscar assets |
| Sin match | Modo fallback neutro + ofrecer al usuario registrar la entidad nueva |

### Paso 2: Buscar archivos coincidentes

Probar la existencia de archivos en este orden:

1. `assets/paleta-{slug}.json` (si existe, leer y usar para colores).
2. `assets/logo-{slug}.svg` (preferido).
3. `assets/logo-{slug}.png` (fallback).
4. Variantes específicas si el contexto lo demanda:
   - `assets/logo-{slug}-blanco.{ext}` cuando el fondo es muy oscuro.
   - `assets/logo-{slug}-monocromo.{ext}` cuando se quiere efecto sobrio.

### Paso 3: Si no hay paleta JSON

Aplicar la paleta temática elegida en `theme-mapping.md` sin override.

### Paso 4: Si tampoco hay logo

Usar tipografía como identidad: el nombre de la entidad escrito en la portada con la tipografía sans del tema, sin imagen de logo.

## Subgrupos y herencia

Si una entidad tiene `parent: <slug-de-otra-entidad>` en su definición de `config-local.md` (ej. un ministerio dentro de una iglesia), aplicar herencia visual:

1. Buscar primero el slug específico de la entidad subgrupo.
2. Si no existe el asset, **fallback al slug del `parent`**.
3. Si tampoco existe del padre, modo neutro.

Esto permite que un grupo nuevo herede temporalmente la identidad de su iglesia/marca padre hasta que tenga la suya propia.

## Reportar decisiones al usuario

Antes de generar la SPA, mostrar resumen al usuario (sustituyendo placeholders por valores reales del config y de los archivos encontrados):

```
Identidad visual aplicada:
- Entidad detectada: <entity.name>
- Logo: logo-<entity.slug>.svg (encontrado / no encontrado)
- Paleta institucional: paleta-<entity.slug>.json (encontrada / usando paleta temática)
  → override de accent_primary y accent_secondary aplicado sobre paleta '<theme>'
- Logo variant para fondo oscuro: logo-<entity.slug>-blanco.png (si existe)
```

Si algo falló o usó fallback:

```
⚠ Logo de <entity.name> no encontrado en assets/.
  Solo paleta temática '<theme>' aplicada, sin logo institucional.
  Para futuras presentaciones, sube el logo a:
  <resources_root>/assets/logo-<entity.slug>.svg
```

## Casos especiales

### Sermón co-predicado o invitado

Si el sermón se predica en un contexto distinto al de la entidad principal del usuario (ej. el `user` invitado a otra iglesia o ministerio), aplicar identidad **del lugar de predicación**, no de la entidad principal del usuario. La paleta refleja el contexto de la audiencia, no la identidad personal del predicador.

### Sermón con dos identidades válidas

Cuando un sermón se publica en dos repos (entidad `primary` + entidad `secondary` con `user_also_publishes_to_primary: true`), generar **dos versiones del HTML**:

- Versión para repos de la entidad `primary`: identidad de la primary en footer + `ORG_GITHUB_URL` = `primary.github_org_url`
- Versión para repos de la entidad `secondary`: identidad de la secondary + `ORG_GITHUB_URL` = `secondary.github_org_url`

La identidad visual del cuerpo (paleta + logo grande en cover) es la del **lugar de predicación**. Solo el footer y los metadatos de licencia/atribución cambian entre versiones.

---

<small>

**Skill:** /sermon — generador de presentaciones homiléticas
**Autor del skill:** Jonathan Ricardo Proaño Alcívar (Parlox), con asistencia de IA Claude (Anthropic).
**Licencia del skill:** AGPL-3.0-or-later (todo el skill — documentos y código que genera).
**Licencia del bosquejo .md generado:** CC BY-SA 4.0 (contenido es obra del predicador, no del skill).
**Licencia de la SPA HTML generada:** AGPL-3.0-or-later (programa ejecutable).
**Repo:** [pendiente — aún no publicado]

</small>
