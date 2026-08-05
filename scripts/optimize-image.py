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
optimize-image.py — prepara imágenes para las SPA de sermones.

Convierte una imagen a WebP con los perfiles medidos para cada uso, y
opcionalmente la inyecta como data URI en un placeholder del HTML.

IMPORTANTE: el data URI nunca se imprime a stdout por defecto. La inyección
la hace este script directamente sobre el archivo, de modo que el string
base64 no pasa por el contexto del modelo.

Perfiles (medidos sobre el corpus real, ver image-pipeline.md):

  bg         1280x720  q65   ~32 KB   fondo atmosférico bajo scrim
  fg-half     960x1080 q80   ~55 KB   imagen al frente, media lámina (split)
  fg-third    640x720  q80   ~30 KB   imagen al frente, un tercio de lámina

Las imágenes viven en <resources_root>/assets/imagenes-sermones/, plano, con
nombre {YYYYMMDD}-{slug-corto}-{clave}.webp. Ver image-pipeline.md.

Uso:
  optimize-image.py FUENTE --mode bg --out IMGS/20260601-gracia-restaura-portada.webp
  optimize-image.py FUENTE --mode fg-half --focus top --out IMGS/20260601-gracia-restaura-manos.webp
  optimize-image.py --inject presentacion.html --key portada --image IMGS/20260601-gracia-restaura-portada.webp

Requiere Pillow (python3 -m pip install --user Pillow).
"""

import argparse
import base64
import json
import os
import re
import sys

PROFILES = {
    "bg":       {"size": (1280, 720),  "quality": 65},
    "fg-half":  {"size": (960, 1080),  "quality": 80},
    "fg-third": {"size": (640, 720),   "quality": 80},
}

FOCUS = {"top": 0.0, "center": 0.5, "bottom": 1.0, "left": 0.0, "right": 1.0}


def die(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def load_pillow():
    try:
        from PIL import Image
        return Image
    except ImportError:
        die("Pillow no está instalado. Instalar con: python3 -m pip install --user Pillow\n"
            "       Alternativa sin Pillow: magick FUENTE -resize 1280x720^ -gravity center "
            "-extent 1280x720 -quality 65 -strip SALIDA.webp")


def cover_resize(im, target, focus="center"):
    """Redimensiona cubriendo el target y recorta el excedente según el foco.

    Equivalente a `background-size: cover` + `object-position`. Nunca escala
    hacia arriba: si la fuente es menor que el target, se conserva su tamaño
    y solo se ajusta la relación de aspecto.
    """
    Image = load_pillow()
    tw, th = target
    sw, sh = im.size

    # No agrandar: si la fuente no da para el target, bajamos el target.
    scale = min(sw / tw, sh / th)
    if scale < 1.0:
        tw, th = max(1, int(tw * scale)), max(1, int(th * scale))

    src_ratio, dst_ratio = sw / sh, tw / th
    if src_ratio > dst_ratio:          # fuente más ancha: recortar a los lados
        new_w = int(sh * dst_ratio)
        off = int((sw - new_w) * FOCUS.get(focus, 0.5))
        im = im.crop((off, 0, off + new_w, sh))
    elif src_ratio < dst_ratio:        # fuente más alta: recortar arriba/abajo
        new_h = int(sw / dst_ratio)
        off = int((sh - new_h) * FOCUS.get(focus, 0.5))
        im = im.crop((0, off, sw, off + new_h))

    return im.resize((tw, th), Image.LANCZOS)


def optimize(src, mode, out, focus="center", quality=None, credit=None):
    Image = load_pillow()
    prof = PROFILES[mode]
    q = quality if quality is not None else prof["quality"]

    try:
        im = Image.open(src)
    except Exception as e:
        die(f"no se pudo abrir {src}: {e}")

    im = im.convert("RGB")  # descarta alpha y perfiles raros; también quita EXIF
    im = cover_resize(im, prof["size"], focus)

    os.makedirs(os.path.dirname(os.path.abspath(out)) or ".", exist_ok=True)
    im.save(out, "WEBP", quality=q, method=6)

    before = os.path.getsize(src)
    after = os.path.getsize(out)
    print(f"{os.path.basename(src)} -> {os.path.basename(out)}  "
          f"{im.size[0]}x{im.size[1]} q{q}  "
          f"{before/1024:.0f} KB -> {after/1024:.0f} KB  "
          f"({100*after/before:.0f}%, ~{after*1.37/1024:.0f} KB en base64)")

    if credit:
        record_credit(out, credit)
    return out


def record_credit(image_path, credit):
    """Guarda la procedencia junto a la imagen, para el bloque de atribución."""
    d = os.path.dirname(os.path.abspath(image_path))
    path = os.path.join(d, "credits.json")
    data = {}
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            data = {}
    data[os.path.basename(image_path)] = credit
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    print(f"  crédito registrado en {os.path.relpath(path)}")


def data_uri(path):
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    mime = {"webp": "image/webp", "jpg": "image/jpeg", "jpeg": "image/jpeg",
            "png": "image/png"}.get(ext)
    if not mime:
        die(f"extensión no soportada para data URI: {path}")
    with open(path, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode("ascii")


def inject(html_path, key, image_path):
    """Reemplaza el placeholder {{IMG:key}} por el data URI, in place.

    El base64 nunca pasa por stdout ni por el contexto del modelo.
    """
    if not os.path.exists(html_path):
        die(f"no existe {html_path}")
    with open(html_path, encoding="utf-8") as f:
        html = f.read()

    placeholder = "{{IMG:%s}}" % key
    n = html.count(placeholder)
    if n == 0:
        die(f"no se encontró el placeholder {placeholder} en {html_path}")

    uri = data_uri(image_path)
    html = html.replace(placeholder, uri)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"inyectado {placeholder} <- {os.path.basename(image_path)}  "
          f"({len(uri)/1024:.0f} KB base64, {n} ocurrencia(s))")


def check_leftovers(html_path):
    with open(html_path, encoding="utf-8") as f:
        left = re.findall(r"\{\{IMG:([^}]+)\}\}", f.read())
    if left:
        print(f"AVISO: quedan placeholders sin inyectar: {', '.join(sorted(set(left)))}",
              file=sys.stderr)
        return 1
    print("sin placeholders pendientes")
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("source", nargs="?", help="imagen de entrada")
    p.add_argument("--mode", choices=sorted(PROFILES), help="perfil de optimización")
    p.add_argument("--out", help="ruta de salida .webp")
    p.add_argument("--focus", choices=sorted(FOCUS), default="center",
                   help="hacia dónde recortar (default: center)")
    p.add_argument("--quality", type=int, help="sobrescribe la calidad del perfil")
    p.add_argument("--credit",
                   help='procedencia: "generada con IA", "propia", o '
                        '"Unsplash · Jane Doe · unsplash.com/photos/xyz"')
    p.add_argument("--inject", metavar="HTML", help="inyectar un data URI en este HTML")
    p.add_argument("--key", help="clave del placeholder {{IMG:key}}")
    p.add_argument("--image", help="imagen ya optimizada a inyectar")
    p.add_argument("--check", metavar="HTML", help="verificar que no queden placeholders")
    a = p.parse_args()

    if a.check:
        sys.exit(check_leftovers(a.check))

    if a.inject:
        if not (a.key and a.image):
            die("--inject requiere --key y --image")
        inject(a.inject, a.key, a.image)
        return

    if not (a.source and a.mode and a.out):
        p.print_help()
        die("se requiere FUENTE --mode --out (o --inject / --check)")

    optimize(a.source, a.mode, a.out, a.focus, a.quality, a.credit)


if __name__ == "__main__":
    main()
