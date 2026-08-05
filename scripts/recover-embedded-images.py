#!/usr/bin/env python3
#
# Parte del skill /sermon — https://github.com/CafecitoTeologico/ct-skill-sermon
# Copyright (C) 2026 Jonathan Ricardo Proaño Alcívar
#
# Este programa es software libre: puedes redistribuirlo y/o modificarlo bajo los
# términos de la GNU Affero General Public License, versión 3 o posterior, tal
# como la publica la Free Software Foundation. Se distribuye con la esperanza de
# que sea útil, pero SIN NINGUNA GARANTÍA. Ver LICENSE en la raíz del repo o
# https://www.gnu.org/licenses/agpl-3.0.html
#
# SPDX-License-Identifier: AGPL-3.0-or-later
"""
recover-embedded-images.py — rescata imágenes atrapadas en un HTML.

Las presentaciones generadas antes de la v1.2.0 embebían las imágenes como
data URI base64 sin guardar el original en disco. Este script las extrae de
vuelta a archivos, para que exista una fuente recuperable.

Extrae SIN recomprimir: el base64 del HTML es la única copia que queda, así que
la recuperación debe ser sin pérdida. Optimizar después, si hace falta, con
optimize-image.py.

No modifica el HTML de entrada.

Uso:
  recover-embedded-images.py PRESENTACION.html --out DESTINO/ --dry-run
  recover-embedded-images.py PRESENTACION.html --out DESTINO/
  recover-embedded-images.py *.html --out-root RAIZ/     # una subcarpeta por sermón
"""

import argparse
import base64
import binascii
import hashlib
import os
import re
import sys

EXT = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp",
       "image/gif": "gif", "image/svg+xml": "svg"}

# Captura `clave: 'data:image/xxx;base64,...'` y también data URIs sueltos.
NAMED = re.compile(
    r"""(?P<key>[A-Za-z_][\w-]*)\s*:\s*['"]data:(?P<mime>image/[\w+.-]+);base64,(?P<b64>[A-Za-z0-9+/=\s]+?)['"]""",
    re.VERBOSE)
BARE = re.compile(r"""data:(?P<mime>image/[\w+.-]+);base64,(?P<b64>[A-Za-z0-9+/=]{200,})""")


def slug_from_filename(path):
    """20260315-Titulo-Del-Sermon-Nombre-Apellido.html -> titulo-del-sermon

    Quita la fecha inicial y el nombre del predicador del final (2 palabras).
    Heurística: si no calza el patrón, devuelve el basename normalizado.
    """
    stem = os.path.splitext(os.path.basename(path))[0]
    m = re.match(r"^\d{8}-(.+)$", stem)
    if not m:
        return stem.lower()
    rest = m.group(1).split("-")
    if len(rest) > 3:            # asume Nombre-Apellido al final
        rest = rest[:-2]
    return "-".join(rest).lower()


def extract(html_path):
    """Devuelve [(clave, mime, bytes)] deduplicado por contenido."""
    with open(html_path, encoding="utf-8", errors="replace") as f:
        html = f.read()

    found, seen, spans = [], set(), []
    for m in NAMED.finditer(html):
        spans.append((m.start(), m.end()))
        blob = decode(m.group("b64"), m.group("key"), html_path)
        if blob is None:
            continue
        h = hashlib.md5(blob).hexdigest()
        if h in seen:
            continue
        seen.add(h)
        found.append((m.group("key"), m.group("mime"), blob))

    # data URIs que no venían con clave (ej. dentro de un style inline)
    for i, m in enumerate(BARE.finditer(html)):
        if any(s <= m.start() < e for s, e in spans):
            continue
        blob = decode(m.group("b64"), f"img-{i+1}", html_path)
        if blob is None:
            continue
        h = hashlib.md5(blob).hexdigest()
        if h in seen:
            continue
        seen.add(h)
        found.append((f"img-{i+1}", m.group("mime"), blob))

    return found


def decode(b64, key, src):
    try:
        return base64.b64decode(re.sub(r"\s+", "", b64), validate=True)
    except (binascii.Error, ValueError) as e:
        print(f"  AVISO: '{key}' en {os.path.basename(src)} no decodifica ({e})",
              file=sys.stderr)
        return None


def run(html_path, out_dir, dry):
    imgs = extract(html_path)
    name = os.path.basename(html_path)
    if not imgs:
        print(f"{name}: sin imágenes embebidas")
        return 0

    print(f"{name}: {len(imgs)} imagen(es) -> {out_dir}")
    total = 0
    for key, mime, blob in imgs:
        ext = EXT.get(mime, "bin")
        dest = os.path.join(out_dir, f"{key}.{ext}")
        total += len(blob)
        mark = ""
        if os.path.exists(dest) and not dry:
            with open(dest, "rb") as f:
                if hashlib.md5(f.read()).hexdigest() == hashlib.md5(blob).hexdigest():
                    print(f"  = {key}.{ext:4s} {len(blob)/1024:6.0f} KB  (ya existe, idéntica)")
                    continue
            dest = os.path.join(out_dir, f"{key}-{hashlib.md5(blob).hexdigest()[:6]}.{ext}")
            mark = "  (colisión de nombre, se renombró)"
        print(f"  {'·' if dry else '+'} {os.path.basename(dest):28s} {len(blob)/1024:6.0f} KB{mark}")
        if not dry:
            os.makedirs(out_dir, exist_ok=True)
            with open(dest, "wb") as f:
                f.write(blob)
    print(f"  total: {total/1024:.0f} KB{' (simulación)' if dry else ''}")
    return total


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("html", nargs="+", help="presentación(es) .html")
    p.add_argument("--out", help="directorio destino (un solo sermón)")
    p.add_argument("--out-root", help="raíz; crea una subcarpeta por sermón usando su slug")
    p.add_argument("--dry-run", action="store_true", help="mostrar sin escribir")
    a = p.parse_args()

    if not a.out and not a.out_root:
        p.error("se requiere --out o --out-root")
    if a.out and len(a.html) > 1:
        p.error("--out solo admite un HTML; usar --out-root para varios")

    grand = 0
    for h in a.html:
        if not os.path.exists(h):
            print(f"error: no existe {h}", file=sys.stderr)
            continue
        out = a.out or os.path.join(a.out_root, slug_from_filename(h))
        grand += run(h, out, a.dry_run)
    if len(a.html) > 1:
        print(f"\nTOTAL RECUPERADO: {grand/1024:.0f} KB{' (simulación)' if a.dry_run else ''}")


if __name__ == "__main__":
    main()
