# Roadmap

Mejoras pendientes del skill `/sermon`, ordenadas por prioridad estimada.

Lo ya entregado vive en [`CHANGELOG.md`](./CHANGELOG.md).

---

## v2.0.0 — motor canónico y vocabulario de láminas cerrado

Hoy el motor de la SPA — cliente MQTT, lógica de modos, cronómetro, shell HTML — se reconstruye completo en cada generación, sin existir como fuente única. Eso hace que dos presentaciones del mismo skill puedan diferir en cosas que deberían ser idénticas.

**Plan:**

- Partir del motor de las presentaciones más recientes, no de `reference-example.html`: el reference es de mayo de 2026 y quedó atrás (no tiene fragmentos por lámina ni el selector de 3 botones). Primer paso: reemplazarlo por una SPA reciente propia, ya usada en un culto, recortada si hace falta para no inflar el contexto.
- Extraer a plantilla mantenida lo que es invariante: cliente MQTT, lógica de modos, cronómetro, shell HTML/meta y los tres bloques de licencia. Sustitución de variables + el array `SLIDES` serializado.
- **Dejar fuera de la plantilla** el `renderSlide` y el CSS por tipo de lámina: el vocabulario visual todavía está evolucionando, y congelarlo en plantilla la dejaría obsoleta enseguida.
- Cerrar el vocabulario canónico de tipos de lámina en `reference-example.html` + `doctrine.md`, para que dejen de aparecer variantes nuevas por sermón. **Este es el cambio que justifica el MAJOR**: el skill pierde una libertad que hoy tiene.

Efecto secundario buscado: hoy `reference-example.html` se lee entero como referencia estructural y es la mitad del contexto que consume una invocación. Con una plantilla, deja de hacer falta leerlo.

Las presentaciones ya generadas no se rompen — son archivos autónomos.

## v2.0.0 — láminas con imagen al frente (`split`)

Hoy las imágenes solo se usan como fondo atmosférico bajo scrim. Falta el patrón clásico: imagen a un lado, texto al otro.

**Plan:**

- Tipos `split` (imagen izquierda) y `split-reverse` (derecha). Alternarlos da ritmo visual.
- La imagen sangra hasta el borde, no flotando con margen. Proporción ~5:7 — el texto lleva la proposición, la imagen acompaña.
- Regla de foco: si la imagen es **evocativa**, el texto manda; si es **informativa** (mapa, obra, diagrama), ella es el foco y el texto se reduce a un pie corto.
- La regla 19 de `doctrine.md` (`text-shadow` sobre imagen) no aplica en `split`: el texto va sobre fondo sólido, con mejor legibilidad que el full-bleed.
- Comportamiento por modo: `presentation`/`screen` lado a lado; `print` decidir si la imagen va o se omite; `control` miniatura, para que el predicador sepa qué ve la congregación; móvil apilado.
- Sourcing en orientación portrait o cuadrada (ver `image-pipeline.md` § 4).
- `object-position` configurable por lámina — `--focus` ya existe en `optimize-image.py`.

Conviene hacerlo junto con el motor canónico.

## Carga condicional de los documentos de referencia

`SKILL.md` declara seis documentos como "leer antes de actuar". Varios no hacen falta en todos los sermones: `identity-discovery.md` solo aplica si la entidad tiene assets propios, e `image-pipeline.md` solo si hay imágenes (ya marcado condicional en la v1.2.0).

Revisar cuáles son realmente obligatorios y marcar el resto como lectura bajo condición, para no cargar en cada invocación lo que no se va a usar.

## Compatibilidad móvil para `presentation` y `print`

Los modos `presentation` y `print` solo funcionan bien en PC con orientación landscape. En móvil portrait fallan por:

- Aspect ratio 16:9 forzado (regla 17 de `doctrine.md`).
- Container queries con `cqh`/`cqw` que producen escalado roto en portrait.
- Falta de breakpoint para portrait.

**Plan cuando se implemente:**

- Agregar `@media (orientation: portrait)` o `@media (max-width: 768px)` que reescale slides al viewport, no a 16:9.
- Agregar swipe táctil además del click para navegación móvil.
- `control` ya funciona en móvil: el selector dejó de recargar la página. `screen` sigue siendo solo PC, porque la proyección siempre sale de una PC.
- Actualizar regla 17 de `doctrine.md`: "16:9 lógico canon en PC; móvil-portrait fallback de revisión, NO flujo de presentación."
- Mantener PC-landscape como **flujo principal y prioridad de diseño**.

**Estado:** roadmap. Implementar cuando aparezca un caso de uso real recurrente.

## Plantilla v5 de bosquejo

Consolidar la v4 y las iteraciones de campo en una v5 explícita, con la frase clave del sermón obligatoria y la aplicación con eje contextual. Hoy la referencia a "v4" y "v5" no es consistente entre documentos, y el parser depende de esa distinción.

## Regla de slug determinista

La convención de filename deja hoy un margen de criterio en la capitalización de conectores cortos, y eso produce resultados inconsistentes entre sermones. Definir una regla cerrada — por ejemplo, una lista fija de palabras que siempre van en minúscula — antes de automatizar la generación de filenames.

## Skills hermanos

Reutilizando el motor visual + MQTT del `/sermon`:

- **`/clase-biblica`** — presentaciones para enseñanza didáctica.
- **`/reunion-ministerial`** — presentaciones de decisiones para liderazgo pastoral.
- **`/bosquejo`** — asistente para redactar bosquejos siguiendo la plantilla v4/v5. Distinto de `/sermon`, que parte de un bosquejo ya terminado.

Dependen del motor canónico: mientras la SPA se reconstruya en cada generación, no hay motor que reutilizar.

## Otros pendientes

- **Validación de simetría más rica:** además de contar ideas secundarias, comparar longitud de cada punto en palabras/oraciones para detectar desequilibrio temporal.
- **Detección de pasaje y autoaviso de versión bíblica:** si el bosquejo cita versículos sin traducción explícita, comparar con APIs públicas y sugerir cuál coincide.
- **Variantes anuales de las conmemorativas:** hoy cada fecha tiene una sola paleta. Con dos o tres por fecha, la Navidad no se vería igual todos los años.
- **Paletas institucionales registradas:** el override de `assets/paleta-{slug}.json` existe, pero ninguna entidad tiene sus colores registrados todavía.
- **Memoria del control tras una recarga:** si el teléfono recarga la pestaña, la lámina se recupera de la cabina por MQTT, pero el cronómetro vuelve a cero. Guardar lámina y cronómetro en `localStorage`, dentro de `try/catch`, lo resolvería.
- **Cronómetro adaptativo:** umbrales (verde/naranja/rojo) configurables por predicador en el frontmatter del bosquejo (`target_minutes: 35`).
- **Entropía real en el topic MQTT:** el segmento `random10` debe generarse con una fuente de aleatoriedad real, no aproximado por el modelo.

---

<small>

**Skill:** /sermon — generador de presentaciones homiléticas
**Licencia del skill:** AGPL-3.0-or-later
**Repo:** https://github.com/CafecitoTeologico/ct-skill-sermon

</small>
