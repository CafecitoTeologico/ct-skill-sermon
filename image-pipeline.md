# image-pipeline.md — manejo de imágenes en las SPA

> **Leer solo cuando el sermón involucre imágenes** (el bosquejo trae imágenes
> embebidas, o se van a usar fondos atmosféricos / imágenes al frente). Si el
> sermón es solo texto, saltar este documento.

Este documento cubre de dónde salen las imágenes, dónde se guardan, cómo se
optimizan, cómo se inyectan en el HTML y cómo se atribuyen.

---

## 1. Regla fundamental: el base64 nunca pasa por mi salida

Una imagen de 90 KB son ~123.000 caracteres en base64. **Nunca debo escribir ese
string como parte de mi respuesta.** No solo es desperdicio: es imposible
transcribirlo sin corromper el archivo.

El flujo correcto es siempre:

```
fuente → optimizar a WebP en imagenes-sermones/ → inyectar por placeholder
```

Los últimos dos pasos los hace `scripts/optimize-image.py` vía Bash. Yo escribo
en el HTML un placeholder `{{IMG:clave}}`, y el script lo reemplaza in place.

---

## 2. Dónde viven las imágenes

**Las imágenes NO van a los repos de bosquejos ni de presentaciones.** Esos
repos contienen solo el entregable: el `.md` del bosquejo o el `.html` de la
SPA. Meter imágenes ahí los infla sin necesidad — la SPA es autocontenida
(lleva las imágenes en base64), así que no las necesita en runtime.

Las imágenes viven en un directorio **local**, fuera de todo repo:

```
<resources_root>/
├── assets/
│   ├── logo-<slug>.svg               ← identidad institucional
│   ├── paleta-<slug>.json               (ver identity-discovery.md)
│   └── imagenes-sermones/            ← imágenes de sermones, PLANO
│       ├── 20260601-gracia-restaura-portada.webp
│       ├── 20260601-gracia-restaura-manos.webp
│       └── credits.json              ← procedencia de todas
├── <entity.bosquejos_dir>/           ← repo git: solo .md
└── <entity.presentaciones_dir>/      ← repo git: solo .html
```

**Solo se guarda la versión optimizada.** No se conserva el original: el
`credits.json` registra el banco y la URL, que es el camino de vuelta al master
si alguna vez hace falta re-derivar en otro perfil.

`<resources_root>` sale de `config-local.md`, nunca hardcodeado.

**Sin subcarpeta por sermón.** Todo plano bajo `imagenes-sermones/`. Para evitar
colisiones (varios sermones usan claves como `portada` o `amanecer`), el nombre
lleva fecha y slug corto:

```
{YYYYMMDD}-{slug-corto}-{clave}.webp
```

El slug corto son las primeras 3-4 palabras significativas del slug del sermón,
sin artículos ni preposiciones.

**Nunca usar `/tmp` como destino.** Es efímero: si la imagen solo existe ahí y
en el base64 del HTML, se pierde el original y queda irrecuperable salvo
decodificando el HTML.

**El respaldo corre por cuenta del usuario.** Este directorio no está bajo
control de versiones a propósito. Si el usuario no tiene respaldo propio de
`<resources_root>`, avisarle una vez — no asumir que existe.

### Si los directorios no existen

Antes de escribir, verificar que `resources_root` y los directorios de la
entidad existan. Si falta alguno:

1. **Reportar** exactamente qué ruta falta y de qué campo del config sale.
2. **Ofrecer crear el esqueleto** (`assets/`, `bosquejos_dir`,
   `presentaciones_dir` y `assets/imagenes-sermones/`).
3. **No crear nada sin confirmación**, igual que con `config-local.md`.

Si `resources_root` apunta a una ruta que no existe *y* el usuario no confirma,
detenerse: no inventar una ruta alternativa ni escribir en el directorio actual.

---

## 3. Perfiles de optimización

Medidos sobre el corpus real. `binario` es el archivo `.webp`; `en HTML` es lo
que ocupa ya convertido a data URI (base64 agrega ~37%).

| Perfil | Resolución | Calidad | Binario | En HTML | Uso |
|---|---|---|---|---|---|
| `bg` | 1280×720 | 65 | ~32 KB | ~43 KB | Fondo atmosférico bajo scrim |
| `fg-half` | 960×1080 | 80 | ~55 KB | ~75 KB | Imagen al frente, media lámina |
| `fg-third` | 640×720 | 80 | ~30 KB | ~42 KB | Imagen al frente, un tercio |

**Por qué los fondos toleran más compresión:** van bajo `.slide-scrim`, un
radial-gradient que cubre del 12% al 80% de opacidad, más `text-shadow` encima.
A q65 el SSIM contra el original *ya compuesto bajo el velo* es 0.979 —
imperceptible en proyección. Una imagen al frente se mira directo: bajar de q80
sí se nota.

**No subir la calidad "por si acaso".** Un fondo a q90 pesa 3× y se ve igual
debajo del velo.

---

## 4. Sourcing

- **Fondos:** landscape 16:9 sirve bien (1600×900 típico de banco de imágenes).
- **Imágenes al frente en lámina dividida:** media lámina de 16:9 es ~8:9, casi
  vertical. **Buscar orientación portrait o cuadrada.** Recortar un landscape a
  vertical bota la mitad del encuadre y suele cortar mal a los sujetos.

`optimize-image.py` nunca agranda: si la fuente no da para el perfil pedido,
produce la mayor resolución posible y lo reporta. Si el resultado sale muy por
debajo del perfil, buscar una fuente mejor en vez de aceptarlo.

Usar `--focus top|center|bottom` cuando el sujeto no está centrado (retratos
casi siempre quieren `top`).

---

## 5. Comandos

Con `IMGS=<resources_root>/assets/imagenes-sermones` y `N={YYYYMMDD}-{slug-corto}`:

```bash
# Fondo atmosférico
python3 scripts/optimize-image.py FUENTE.jpg \
  --mode bg \
  --out "$IMGS/$N-portada.webp" \
  --credit "generada con IA"

# Imagen al frente, sujeto en la parte superior
python3 scripts/optimize-image.py FUENTE.jpg \
  --mode fg-half --focus top \
  --out "$IMGS/$N-manos.webp" \
  --credit "Unsplash · Nombre Autor · unsplash.com/photos/xyz"

# Inyectar en el HTML ya generado (reemplaza {{IMG:portada}})
python3 scripts/optimize-image.py \
  --inject SALIDA.html --key portada \
  --image "$IMGS/$N-portada.webp"

# Verificar que no quedó ningún placeholder sin inyectar
python3 scripts/optimize-image.py --check SALIDA.html
```

**Siempre correr `--check` antes de reportar al usuario.** Un placeholder sin
inyectar deja la lámina sin imagen y sale con código 1.

Cuando el sermón se duplica entre dos entidades, optimizar una sola vez y
ejecutar `--inject` sobre cada copia del HTML.

### Sin Pillow

Si `python3 -c "import PIL"` falla, el equivalente con ImageMagick:

```bash
magick FUENTE.jpg -resize 1280x720^ -gravity center -extent 1280x720 \
  -quality 65 -strip SALIDA.webp
```

Cambiar `-gravity` a `north`/`south` según el foco. La inyección igual se hace
con `optimize-image.py --inject`, que no requiere Pillow.

---

## 6. Atribución

El bloque de créditos de la SPA cubre la autoría del programa y la licencia
AGPL, pero **no cubre las imágenes**. Hay tres casos:

| Origen | `--credit` |
|---|---|
| Generada con IA | `"generada con IA"` |
| Provista por el predicador, propia | `"propia · {PREACHER}"` |
| Provista por el predicador, origen desconocido | `"por verificar"` |
| Banco de imágenes | `"Unsplash · Jane Doe · unsplash.com/photos/xyz"` |

Un sermón puede caer en tres escenarios: **solo imágenes de IA**, **mixto**
(IA + del predicador), o **solo del predicador**. La línea de créditos de la SPA
cambia en cada uno — ver `license-attribution.md` § 6. En el caso mixto nunca
decir solo "generadas con IA": sería falso sobre las del predicador.

**Cuando el predicador aporta imágenes, preguntar de dónde salieron** antes de
usarlas. Si vienen de internet, el crédito y la licencia son de otro, y el repo
de presentaciones es público.

Todo queda en `assets/imagenes-sermones/credits.json` y se lleva al frontmatter
del bosquejo — ver `license-attribution.md` § 6.

**Las imágenes de IA se declaran, no se acreditan.** No hay autor. Pero sí hay
que decirlo: en material de enseñanza, una imagen sintética no puede pasar por
documental. Y **nunca usar IA para ilustrar un hecho real** — un evento
histórico, un lugar concreto, una persona real. Ahí va fotografía real o no va
imagen.

Si una imagen no tiene procedencia conocida, **preguntar al usuario antes de
usarla**. Que alguien la haya aportado en el bosquejo no significa que tenga los
derechos.

---

## 7. Recuperar imágenes ya embebidas

Para presentaciones generadas antes de la v1.2.0, cuyas imágenes solo existen
como base64 dentro del HTML:

```bash
python3 scripts/recover-embedded-images.py PRESENTACION.html \
  --out <resources_root>/assets/imagenes-sermones/ --dry-run
```

Extrae cada imagen a disco sin recomprimir (son la única copia). Quitar
`--dry-run` para escribir. No modifica el HTML.

---

<small>

**Skill:** /sermon — generador de presentaciones homiléticas
**Licencia del skill:** AGPL-3.0-or-later
**Repo:** https://github.com/CafecitoTeologico/ct-skill-sermon

</small>
