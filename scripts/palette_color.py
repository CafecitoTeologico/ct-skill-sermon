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
palette_color.py — color para las paletas de /sermon.

Conversión sRGB ↔ OKLab/OKLCH, contraste WCAG, distancia perceptual y
detección de café. Funciones puras, sin dependencias. Las usa palettes.py.
"""
import math


def hex_a_rgb(h):
    h = h.lstrip('#')
    if len(h) != 6:
        raise ValueError(f'hex inválido: #{h}')
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def rgb_a_hex(rgb):
    return '#' + ''.join(f'{round(max(0.0, min(1.0, c)) * 255):02X}' for c in rgb)


def _lineal(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _srgb(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def luminancia(h):
    r, g, b = (_lineal(c) for c in hex_a_rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(a, b):
    """Razón de contraste WCAG 2.x entre dos colores (1 a 21)."""
    claro, oscuro = sorted((luminancia(a), luminancia(b)), reverse=True)
    return (claro + 0.05) / (oscuro + 0.05)


def hex_a_oklab(h):
    r, g, b = (_lineal(c) for c in hex_a_rgb(h))
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m, s = (math.copysign(abs(v) ** (1 / 3), v) for v in (l, m, s))
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


def _oklab_a_lineal(L, a, b):
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    return (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)


def hex_a_oklch(h):
    """(L, C, H) con H en grados, 0 a 360."""
    L, a, b = hex_a_oklab(h)
    return L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360


def oklch_a_hex(L, C, H):
    """Convierte a hex. Si el color no cabe en sRGB, baja el croma hasta que quepa."""
    for _ in range(60):
        rgb = _oklab_a_lineal(L, C * math.cos(math.radians(H)), C * math.sin(math.radians(H)))
        if all(-1e-7 <= c <= 1 + 1e-7 for c in rgb):
            return rgb_a_hex(tuple(_srgb(max(0.0, min(1.0, c))) for c in rgb))
        C *= 0.95
    return rgb_a_hex(tuple(_srgb(max(0.0, min(1.0, c))) for c in _oklab_a_lineal(L, 0, 0)))


def distancia(a, b):
    """Distancia euclídea en OKLab: ~0.02 apenas se nota; ~0.1 es otro color."""
    return math.dist(hex_a_oklab(a), hex_a_oklab(b))


def dif_matiz(h1, h2):
    d = abs(h1 - h2) % 360
    return min(d, 360 - d)


# Zona café. El usuario lee como café los naranjas y amarillos oscuros (terracota,
# cobre, tostado), los cálidos sin saturación (arena, khaki, beige) y los fondos
# oscuros teñidos de cálido (espresso). Calibrado con test_palettes.TestColor.
def es_cafe(h, rol):
    L, C, H = hex_a_oklch(h)
    if rol == 'fondo':
        return 15 <= H <= 100 and C >= 0.012 and L < 0.5
    if rol == 'acento':
        return 38 <= H <= 100 and (L < 0.68 or (C < 0.11 and L < 0.88))
    if rol == 'papel':
        return 30 <= H <= 100 and C > 0.02
    raise ValueError(f'rol desconocido: {rol}')


def ajustar(L, C, H, contra, objetivo, hacia):
    """Color OKLCH con la luz más cercana a L que alcance `objetivo` de contraste
    contra `contra`. `hacia`: 'arriba' (aclarar) o 'abajo' (oscurecer)."""
    meta = objetivo * 1.03  # margen para el redondeo a hex

    def pasa(l):
        return contraste(oklch_a_hex(l, C, H), contra) >= meta

    if pasa(L):
        return oklch_a_hex(L, C, H)
    lo, hi = (L, 1.0) if hacia == 'arriba' else (0.0, L)
    for _ in range(40):
        mid = (lo + hi) / 2
        if hacia == 'arriba':
            lo, hi = (lo, mid) if pasa(mid) else (mid, hi)
        else:
            lo, hi = (mid, hi) if pasa(mid) else (lo, mid)
    return oklch_a_hex(hi if hacia == 'arriba' else lo, C, H)
