# Theme mapping — cómo se elige la paleta

La paleta de cada sermón la elige `scripts/palettes.py` con las reglas de este documento. El modelo no elige colores a ojo: traduce el sermón a temas y corre el script. Así cada semana sale distinta, nada cae en café y no hace falta preguntarle al usuario.

Las paletas viven en [`palettes/catalog.json`](./palettes/catalog.json). No hace falta leerlo: el script devuelve solo la paleta elegida.

## Principio rector

> El tema oscuro nunca debe sentirse «tinieblas». Siempre lleva un acento luminoso que evoque presencia, gracia o esperanza, incluso en sermones sobre juicio o sufrimiento.

Esquema **Luminous Dark**: fondo oscuro (casi negro con un tinte, o joya profunda y saturada), texto claro y un acento vivo. Fondo oscuro y texto claro se leen mejor en el proyector, a distancia.

## Cómo se elige

1. **El modelo traduce el sermón a temas** del vocabulario de abajo, el principal primero, a partir del tema, el propósito, el título y el pasaje.
2. **El script elige** (`palettes.py pick`):
   - Paleta pedida explícitamente (`--paleta`): esa, sin filtros.
   - Fecha conmemorativa y sermón sobre esa fecha: la conmemorativa.
   - Si no, **rotación** entre las paletas automáticas: gana la que comparte más temas, con estas reglas:
     - nunca una usada en las últimas **13 semanas** en cualquier repo de presentaciones;
     - el mismo predicador no repite familia en **26 semanas**;
     - las SPA de la misma semana se separan al menos **45°** de matiz.
   - Si las reglas dejan el catálogo vacío, se relajan por niveles: el script nunca falla.
3. **No se pregunta.** Se usa la paleta y se reporta al final, con su porqué. Solo si el usuario quiere elegir: mostrar la elegida y sus dos alternativas, o pasar `--paleta` con la que pida.

```bash
python3 scripts/palettes.py pick --fecha 2026-11-01 --predicador "Nombre Apellido" \
  --temas esperanza,fe --dirs <resources_root>/<presentaciones_dir> … [--css]
```

- `--dirs`: los `presentaciones_dir` de **todas** las entidades del config. El script lee qué paleta usó cada SPA.
- `--css`: imprime el bloque `:root` listo para la SPA. Sin `--css`, devuelve JSON con la paleta, las alternativas, la razón y el `<meta>`.

## Vocabulario de temas

| Temas | Palabras clave |
|---|---|
| `gracia`, `perdon` | gracia, perdón, restauración, misericordia |
| `identidad` | identidad, hijo/hija de Dios, nombre, etiqueta |
| `esperanza`, `fe` | esperanza, promesa, futuro, confiar, creer |
| `juicio`, `santidad` | juicio, santidad, temor de Dios, advertencia, pecado |
| `arrepentimiento` | arrepentimiento, volverse a Dios, confesión |
| `mision`, `evangelio` | misión, llamado, ir, anunciar, hacer discípulos |
| `cruz` | cruz, sacrificio, sangre, Calvario |
| `espiritu` | Espíritu Santo, fuego, dones, llenura |
| `sabiduria`, `palabra` | sabiduría, Proverbios, consejo, Escritura, enseñanza |
| `lamento`, `consuelo` | lamento, duelo, llanto, pérdida, consuelo |
| `sufrimiento`, `perseverancia` | prueba, aflicción, Job, perseverar |
| `gozo`, `gratitud`, `alabanza` | gozo, celebración, gratitud, alabanza, adoración |
| `pacto`, `fidelidad` | pacto, alianza, fidelidad de Dios, promesa cumplida |
| `reino`, `liderazgo` | Reino, realeza de Cristo, autoridad, liderazgo |
| `oracion`, `humildad` | oración, intimidad, súplica, humildad |
| `creacion`, `providencia` | creación, naturaleza, cuidado y provisión de Dios |
| `profecia` | profecía, «así dice el Señor», denuncia |
| `encarnacion` | encarnación, el Verbo hecho carne |
| `resurreccion`, `victoria` | resurrección, vida nueva, victoria |
| `discipulado`, `servicio` | discipulado, formación, servir |
| `transformacion` | cambio de vida, nueva criatura, renovación |
| `paz`, `reconciliacion` | paz, perdón entre hermanos, reconciliación |
| `familia`, `matrimonio`, `amor` | familia, hogar, matrimonio, amor |
| `paternidad`, `maternidad`, `ninez`, `juventud`, `vejez` | padres, madres, niños, jóvenes, ancianos |
| `iglesia`, `generosidad` | iglesia, comunidad, cuerpo de Cristo, dar, ofrenda |
| Fechas | `navidad`, `ano-nuevo`, `ramos`, `viernes-santo`, `pentecostes`, `reforma`, `pastor`, `amistad` |

Distinguir:
- `cruz` (el sufrimiento de Cristo) de `sufrimiento` (el del creyente);
- `juicio` (la santidad de Dios) de `profecia` (la voz que denuncia);
- `mision` (el Reino que avanza) de `reino` (su realeza).

## Conmemoraciones

| Fecha | Regla (Ecuador) | Paleta |
|---|---|---|
| Navidad | del 1.er domingo de Adviento al 25-dic | `estrella-de-belen` |
| Fin de año / Año nuevo | 26-dic a 7-ene | `todo-nuevo` |
| Domingo de Ramos | Pascua − 7 | `ramos-hosanna` |
| Viernes Santo | Pascua − 2 | `viernes-santo` |
| Domingo de Resurrección | Pascua | `alba-de-resurreccion` |
| Pentecostés | Pascua + 49 | `lenguas-de-fuego` |
| Día de la Madre | 2.º domingo de mayo | `amor-de-madre` |
| Día del Padre | 3.er domingo de junio | `abrazo-del-padre` |
| Día del Niño | 1 de junio | `dia-del-nino` |
| Amor y Amistad | 14 de febrero | `amor-y-amistad` |
| Día de la Reforma | 31 de octubre | `rosa-de-lutero` |
| Día del Pastor | sin fecha por defecto (varía por país) | `buen-pastor` |

- Las fechas puntuales valen ±3 días (el domingo cercano); Viernes Santo, ±1.
- **Se usan solas** si el sermón cae en la fecha **y** trata de ella (los temas incluyen el de la fecha). En la fecha, con otro tema, va la rotación. Fuera de fecha, solo si se pide o el tema es inequívoco: pasar `--paleta`.
- Otro país, o la fecha del Día del Pastor: sección `conmemoraciones` de `config-local.md`, que se pasa con `--regla id=REGLA`. Formatos: `fija:MM-DD`, `domingo:N:MM`, `pascua:±D`, `rango:MM-DD:MM-DD`. Para ver las fechas de un año: `palettes.py fechas --anio 2027`.

## Nada de café

Es una restricción dura, no una preferencia. El script la aplica a toda paleta automática, y vale igual para cualquier paleta hecha a mano:

- **Fondos:** nada de oscuros teñidos de cálido (espresso, chocolate, tabaco).
- **Acentos:**
  - nada de naranjas o amarillos oscuros (terracota, cobre, bronce);
  - nada de cálidos sin saturación (arena, tostado, khaki, beige);
  - oros, ámbares y corales **vivos**, sí.
- **El oro va solo en trazos, filetes y texto.** Un resplandor o un relleno dorado sobre oscuro da café.
- **Al oscurecer para tinta de lámina clara**, un oro o un naranja sale bronce y un limón sale oliva. En esos casos no hay tinta de acento (`accent_ink` vacío) y el énfasis va en `ink` con peso.

## Cómo usar la paleta en la SPA

- Pegar el `:root` de `pick --css`:
  - fondo y texto: `--bg`, `--bg-2` (degradados y superficies), `--text`, `--text-muted`;
  - acentos: `--accent` (trazos, filetes y titulares grandes), `--accent-bright` (texto de acento: kickers, énfasis), `--accent-em` (destellos);
  - láminas claras: `--paper`, `--paper-2`, `--ink`, `--ink-soft`, `--muted-ink`, `--accent-ink` (solo si existe);
  - impresión: `--print-ink`, `--print-ink-soft`, `--print-rule`.
- Poner `<meta name="sermon-palette" content="{id}">` en el `<head>`, para que la próxima elección sepa que esta paleta ya se usó.
- Respetar las `reglas` de la paleta, que vienen en el JSON y en el comentario del `:root`.
- Regla 13 de `doctrine.md`: un acento y sus variantes tonales. Las excepciones (`dia-del-nino`, `carmesi-real`) están en las reglas de cada paleta.

## Paletas a pedido

Tienen `auto: false` en el catálogo: el script nunca las elige solo. Se piden con `--paleta id`.

- **Café:** las originales del skill que no pasan la regla (`grace`, `default`, `covenant`, `joy`, `wisdom`…).
- **Claras:** `lino-y-vino`, para cuando el evento trae su propio arte claro.
- **`prayer`:** se veía apagada y muy parecida a `hope-twilight`.

## Agregar una paleta

1. `python3 scripts/palettes.py derivar --bg '#…' --accent '#…'`: completa los 16 tokens con los contrastes de doctrine.
2. Agregarla a `palettes/catalog.json` con `id`, `nombre`, `familia`, `temas` (del vocabulario), `ancla`, `inspiracion` y `reglas`. Dos paletas muy parecidas van en la misma `familia`, así la rotación no las pone seguidas.
3. `python3 scripts/palettes.py check`: revisa contraste, anti-café, que no se parezca a otra y el mínimo de 60 en rotación.
4. `python3 scripts/palettes.py muestrario --out muestrario.html`: revisarla a ojo junto a las demás.

## Override institucional

Si la entidad tiene `<resources_root>/assets/paleta-{slug}.json` (ver `identity-discovery.md`):

- Mantener `bg`, `bg_2`, `text` y `text_muted` de la paleta elegida.
- Reemplazar `accent` y `accent_bright` por los institucionales, y verificarlos con `check` (contraste y anti-café).
- Mantener `accent_em`.

## Entidad no reconocida

Usar la paleta de `pick`, sin override ni logo, y ofrecer registrar la entidad:

> «No reconocí la entidad 'X' en assets/. ¿Quieres registrarla para futuros sermones? Si sí, ¿dónde guardo su logo y cuál es su paleta?»

---

<small>

**Skill:** /sermon — generador de presentaciones homiléticas
**Autor del skill:** Jonathan Ricardo Proaño Alcívar (Parlox), con asistencia de IA Claude (Anthropic).
**Licencia del skill:** AGPL-3.0-or-later (todo el skill — documentos y código que genera).
**Licencia del bosquejo .md generado:** CC BY-SA 4.0 (contenido es obra del predicador, no del skill).
**Licencia de la SPA HTML generada:** AGPL-3.0-or-later (programa ejecutable).
**Repo:** https://github.com/CafecitoTeologico/ct-skill-sermon

</small>
