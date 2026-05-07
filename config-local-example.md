# config-local-example.md

> **Este archivo es un template público.** Cópialo a `config-local.md` (que está
> gitignored) y rellena los valores con tus datos reales. El skill `/sermon`
> leerá ese archivo en runtime para saber tus rutas, entidades y preferencias.
>
> Si invocas `/sermon` y no existe `config-local.md`, Claude te ofrecerá crearlo
> conversacionalmente o copiarlo manualmente.

---

## resources_root

Ruta absoluta al directorio raíz donde guardas tus recursos teológicos
(bosquejos, presentaciones, plantillas, assets institucionales).

```yaml
resources_root: ~/sermon-resources/
```

Ejemplo de estructura esperada bajo `resources_root`:

```
~/sermon-resources/
├── assets/                    ← logos y paletas institucionales
├── bosquejos/                 ← outputs .md (puede tener subdirs por entidad)
├── presentaciones/            ← outputs .html (puede tener subdirs por entidad)
└── recursos/                  ← plantillas, ensayos, materiales
```

---

## user

Datos del usuario del skill. Aplican a la atribución del **programa SPA** (no al
contenido del sermón — ese va con el predicador real, que se extrae del bosquejo).

```yaml
user:
  full_name: "[Tu nombre completo, ej. Juan Carlos Pérez Gómez]"
  short_name: "[Nombre-Apellido para filenames, transliterado y sin acentos]"
  email: "[tu@email.com]"
  github_handle: "[tu-handle-en-github]"
  preferred_bible_version: "[NTV | RV60 | LBLA | NVI | DHH | otra]"
  default_others_bible_version: "[default cuando otros predican, ej. RV60]"
```

---

## entities

Lista de entidades (iglesia, ministerio, conferencia, contexto) donde predicas
o para las cuales generas material. Cada entidad tiene su propio destino de
publicación, identidad visual y org de GitHub.

```yaml
entities:
  - slug: "[slug-en-kebab-case-sin-acentos]"
    name: "[Nombre completo de la entidad]"
    aliases:
      - "[variante 1]"
      - "[variante 2]"
    bosquejos_dir: "[subdir relativo a resources_root, ej. bosquejos/mi-iglesia/ o mi-iglesia-bosquejos/]"
    presentaciones_dir: "[subdir relativo a resources_root]"
    recursos_dir: "[opcional, si tienes plantillas/recursos por entidad]"
    github_org: "[handle de GitHub de la entidad, ej. MiIglesia]"
    github_org_url: "[URL completa, ej. https://github.com/MiIglesia]"
    role: "primary | secondary | guest"
    user_also_publishes_to_primary: false
```

### Campos explicados

- **slug**: identificador en kebab-case, sin tildes ni ñ. Se usa internamente y
  potencialmente como prefijo/sufijo de filenames.
- **name**: nombre completo y legible para mostrar en SPAs y bosquejos.
- **aliases**: variantes que el parser puede detectar en el campo `At:` del
  bosquejo. Útil cuando los predicadores escriben con o sin acentos, abreviado, etc.
- **bosquejos_dir / presentaciones_dir**: rutas relativas a `resources_root`.
  Pueden ser:
  - **planos** (`bosquejos/`, `presentaciones/`) si solo manejas una entidad
  - **subdirs por entidad** (`bosquejos/mi-iglesia/`, `presentaciones/mi-iglesia/`)
  - **prefijo o sufijo** (`mi-iglesia-bosquejos/`, `bosquejos-mi-iglesia/`)
  El skill respeta lo que pongas aquí.
- **github_org**: handle de la organización en GitHub (case-sensitive como
  aparece en URLs). Se usa para el footer de atribución de la SPA.
- **role**:
  - `primary` → entidad principal del usuario; siempre se publica aquí cuando el
    usuario es el predicador, sin importar dónde se predica.
  - `secondary` → entidad donde se predica también; recibe copia cuando el
    predicador está en su contexto.
  - `guest` → contexto invitado; el skill pregunta antes de publicar aquí.
- **user_also_publishes_to_primary**: cuando el usuario predica en esta entidad
  secondary, ¿también sube copia a su primary? `true` para iglesia local del
  usuario; `false` para conferencias o invitaciones puntuales.

### Ejemplo: usuario con una sola entidad

```yaml
entities:
  - slug: mi-iglesia
    name: Mi Iglesia Local
    aliases: ["mi iglesia"]
    bosquejos_dir: bosquejos/
    presentaciones_dir: presentaciones/
    github_org: MiIglesia
    github_org_url: https://github.com/MiIglesia
    role: primary
```

### Ejemplo: usuario con dos entidades (personal + iglesia local)

```yaml
entities:
  - slug: mi-marca
    name: Mi Marca Personal o Ministerio
    aliases: ["marca personal"]
    bosquejos_dir: marca-bosquejos/
    presentaciones_dir: marca-presentaciones/
    recursos_dir: marca-recursos/
    github_org: MiMarca
    github_org_url: https://github.com/MiMarca
    role: primary

  - slug: iglesia-local
    name: Mi Iglesia Local
    aliases: ["iglesia local", "il"]
    bosquejos_dir: iglesia-bosquejos/
    presentaciones_dir: iglesia-presentaciones/
    github_org: MiIglesiaLocal
    github_org_url: https://github.com/MiIglesiaLocal
    role: secondary
    user_also_publishes_to_primary: true
```

---

## Subgrupos / herencia visual (opcional)

Si una entidad es subgrupo de otra y comparte parte de su identidad visual
(ej. ministerio de jóvenes dentro de una iglesia), declárala con `parent`:

```yaml
entities:
  # ... otras entidades ...
  - slug: jovenes-mi-iglesia
    name: Ministerio de Jóvenes - Mi Iglesia
    aliases: ["jóvenes", "ministerio juvenil"]
    bosquejos_dir: jovenes-bosquejos/
    presentaciones_dir: jovenes-presentaciones/
    parent: mi-iglesia      # hereda assets/identidad si los suyos no existen
    role: secondary
```

---

## Sobre la privacidad

`config-local.md` está en `.gitignore` y nunca debe subirse al repo público del
skill. Si en algún momento te das cuenta que se commiteo por error:

1. Removerlo del repo: `git rm --cached config-local.md && git commit -m "Remove leaked config-local.md"`
2. Considera regenerar tokens/handles si crees que se filtró algo sensible.
3. Reescribe el historial si el commit ya está en GitHub: `git filter-repo` (más radical, hablar con el equipo del repo si aplica).

---

<small>

**Skill:** /sermon — generador de presentaciones homiléticas
**Licencia del skill:** AGPL-3.0-or-later
**Repo:** https://github.com/CafecitoTeologico/ct-skill-sermon

</small>
