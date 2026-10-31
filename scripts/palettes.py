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
palettes.py — catálogo y elección de paletas para las SPA de /sermon.

El modelo traduce el sermón a temas del vocabulario; este script decide la
paleta: rotación sin repetir, conmemoraciones y nada de café.

    python3 scripts/palettes.py pick --fecha 2026-11-01 --predicador "Nombre Apellido" \\
        --temas esperanza,fe --dirs <presentaciones_dir> [<otro>…] [--css]
    python3 scripts/palettes.py fechas --anio 2026
    python3 scripts/palettes.py check
    python3 scripts/palettes.py derivar --bg '#0C0E14' --accent '#E2B13C'

Ver theme-mapping.md.
"""
import argparse
import datetime as dt
import hashlib
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import palette_calendar as cal  # noqa: E402
import palette_color as pc  # noqa: E402

CATALOGO = Path(__file__).resolve().parent.parent / 'palettes' / 'catalog.json'

# Mismos nombres que las variables CSS de las SPA (bg → --bg, bg_2 → --bg-2…).
TOKENS = ['bg', 'bg_2', 'text', 'text_muted', 'accent', 'accent_bright', 'accent_em',
          'paper', 'paper_2', 'ink', 'ink_soft', 'muted_ink', 'accent_ink',
          'print_ink', 'print_ink_soft', 'print_rule']
CLAVES = ['id', 'nombre', 'familia', 'modo', 'auto', 'conmemoracion', 'temas', 'ancla',
          'inspiracion', 'tokens', 'reglas']

# (texto, fondo, mínimo). Regla 1 de doctrine.md: objetivo 7:1, mínimo 4.5:1.
# `accent` es para trazos, filetes y titulares grandes (3:1); el texto de acento
# usa `accent_bright`, que `derivar` lleva a 7.5:1 y aquí se exige al mínimo.
UMBRALES = [
    ('text', 'bg', 7), ('text', 'bg_2', 7), ('accent_bright', 'bg', 4.5),
    ('text_muted', 'bg', 4.5), ('accent', 'bg', 3),
    ('ink', 'paper', 7), ('ink', 'paper_2', 7), ('ink_soft', 'paper', 7), ('ink_soft', 'paper_2', 7),
    ('muted_ink', 'paper', 4.5), ('muted_ink', 'paper_2', 4.5),
    ('accent_ink', 'paper', 4.5), ('accent_ink', 'paper_2', 4.5),
    ('print_ink', '#FFFFFF', 7), ('print_ink_soft', '#FFFFFF', 4.5),
]
CAFE = [('bg', 'fondo'), ('bg_2', 'fondo'), ('accent', 'acento'), ('accent_bright', 'acento'),
        ('paper', 'papel')]
HEX = re.compile(r'^#[0-9A-F]{6}$')
MINIMO_ROTACION = 60

# Rotación: una paleta no vuelve antes de 13 semanas; el mismo predicador no
# repite familia en 26; las SPA de la misma semana se separan ≥ 45° de matiz.
VENTANA_SEMANAS = 13
VENTANA_PREDICADOR = 26
MISMA_SEMANA_DIAS = 3
MATIZ_MINIMO = 45

NOMBRE_SPA = re.compile(r'^(\d{8})-.*-([^-]+)-([^-]+)\.html$')
META = re.compile(r'<meta\s+name="sermon-palette"\s+content="([^"]+)"', re.I)
COMENTARIO = re.compile(r'[Pp]aleta\s*[«"“`\']?([a-z]+(?:-[a-z]+)*)')


def cargar(ruta=CATALOGO):
    return json.loads(Path(ruta).read_text(encoding='utf-8'))


def _apagado(h):
    """Café (bronce, tostado) u oliva: lo que queda al oscurecer oros, naranjas y limones."""
    L, C, H = pc.hex_a_oklch(h)
    return pc.es_cafe(h, 'acento') or (95 <= H <= 125 and C > 0.03)


def derivar(bg, accent):
    """Los 16 tokens de una paleta a partir de su fondo y su acento."""
    bg, accent = bg.upper(), accent.upper()
    Lb, Cb, Hb = pc.hex_a_oklch(bg)
    La, Ca, Ha = pc.hex_a_oklch(accent)
    t = {'bg': bg, 'accent': accent}
    t['text'] = pc.ajustar(0.95, min(Cb, 0.015), Hb, bg, 12, 'arriba')
    # Segundo tono del fondo, para degradados y superficies: un paso que se note,
    # como en las paletas reales (ΔE ≈ 0.05). En un fondo joya el paso de luz se
    # percibe poco, así que además gira un poco el matiz, hacia el lado que no
    # acerca al café (un carmín girado al naranja da ladrillo). El texto se lee encima.
    if Cb >= 0.05:
        for giro in (12, -12):
            t['bg_2'] = pc.ajustar(Lb + 0.07, Cb * 1.1, (Hb + giro) % 360, t['text'], 7.3, 'abajo')
            if not pc.es_cafe(t['bg_2'], 'fondo'):
                break
    else:
        t['bg_2'] = pc.ajustar(Lb + 0.055, Cb, Hb, t['text'], 7.3, 'abajo')
    t['text_muted'] = pc.ajustar(0.66, min(Cb, 0.03), Hb, bg, 5.5, 'arriba')
    # El brillante es el acento para texto. Si el acento ya es claro, o es un coral
    # o un naranja (25–75°, que muy aclarados no caben saturados en sRGB y se vuelven
    # durazno tostado), sube apenas y los cálidos conservan su croma; `ajustar` sube
    # más solo si falta contraste. Si llegar a 7.5:1 lo lava hasta casi blanco o lo
    # vuelve café (fondos joya claros), basta el mínimo de doctrine partiendo del
    # propio acento: si ya lo cumple, el brillante es el acento mismo.
    calido = 25 <= Ha < 75
    if calido or La >= 0.82:
        l_brillo, c_brillo = La + 0.03, Ca if calido else Ca * 0.85
    else:
        l_brillo, c_brillo = max(La + 0.07, 0.8), Ca * 0.85
    brillo = pc.ajustar(l_brillo, c_brillo, Ha, bg, 7.5, 'arriba')
    if pc.hex_a_oklch(brillo)[1] < 0.05 <= Ca or pc.es_cafe(brillo, 'acento'):
        brillo = pc.ajustar(La, c_brillo, Ha, bg, 4.6, 'arriba')
    t['accent_bright'] = brillo
    t['accent_em'] = pc.oklch_a_hex(0.93, Ca * 0.35, Ha)
    # Láminas claras: papel apenas teñido con el matiz del fondo.
    t['paper'] = pc.oklch_a_hex(0.955, 0.008, Hb)
    t['paper_2'] = pc.oklch_a_hex(0.925, 0.01, Hb)
    t['ink'] = (bg if pc.contraste(bg, t['paper_2']) >= 7.2
                else pc.ajustar(0.2, Cb, Hb, t['paper_2'], 7.5, 'abajo'))
    t['ink_soft'] = pc.ajustar(0.34, Cb, Hb, t['paper_2'], 7.5, 'abajo')
    t['muted_ink'] = pc.ajustar(0.47, min(Cb, 0.04), Hb, t['paper_2'], 5, 'abajo')
    # Un oro o un naranja oscurecidos para tinta se vuelven bronce, y un limón,
    # oliva: en esos casos no hay tinta de acento, y el énfasis va en `ink` y peso
    # (regla de kemet-oro). Lo mismo para el filete de impresión.
    tinta = pc.ajustar(min(La, 0.5), min(Ca, 0.16), Ha, t['paper_2'], 5, 'abajo')
    t['accent_ink'] = None if _apagado(tinta) else tinta
    t['print_ink'] = pc.oklch_a_hex(0.2, min(Cb, 0.02), Hb)
    t['print_ink_soft'] = pc.ajustar(0.42, min(Cb, 0.02), Hb, '#FFFFFF', 5, 'abajo')
    filete = pc.ajustar(min(La, 0.62), Ca, Ha, '#FFFFFF', 3, 'abajo')
    t['print_rule'] = t['print_ink_soft'] if _apagado(filete) else filete
    return {k: t[k] for k in TOKENS}


def validar(cat, minimo_rotacion=MINIMO_ROTACION):
    """Lista de errores del catálogo (vacía si está bien)."""
    errores = []
    vocab = set(cat.get('temas', []))
    conms = cat.get('conmemoraciones', {})
    paletas = cat.get('paletas', [])
    vistos = set()
    for p in paletas:
        pid = p.get('id', '?')
        faltan = [k for k in CLAVES if k not in p]
        if faltan:
            errores.append(f'{pid}: faltan claves: {", ".join(faltan)}')
            continue
        if pid in vistos:
            errores.append(f'{pid}: id duplicado')
        vistos.add(pid)
        if p['modo'] not in ('oscuro', 'claro'):
            errores.append(f'{pid}: modo inválido ({p["modo"]})')
        errores += [f'{pid}: tema fuera del vocabulario: {t}' for t in p['temas'] if t not in vocab]
        if p['conmemoracion'] and p['conmemoracion'] not in conms:
            errores.append(f'{pid}: conmemoración desconocida: {p["conmemoracion"]}')
        tok = p['tokens']
        malos = [k for k in TOKENS
                 if k not in tok
                 or (tok[k] is None and k != 'accent_ink')
                 or (tok[k] is not None and not HEX.match(str(tok[k])))]
        if malos:
            errores.append(f'{pid}: tokens inválidos o faltantes: {", ".join(malos)}')
            continue
        for texto, fondo, minimo in UMBRALES:
            if tok[texto] is None:
                continue
            r = pc.contraste(tok[texto], tok.get(fondo, fondo))
            if r < minimo:
                errores.append(f'{pid}: contraste {texto}/{fondo} = {r:.2f} < {minimo}')
        if p['auto']:
            errores += [f'{pid}: café en {k} ({tok[k]})' for k, rol in CAFE if pc.es_cafe(tok[k], rol)]

    # Distinción: dos paletas de familias distintas no pueden tener a la vez fondo
    # y acento casi iguales. Las variantes de una misma familia sí se parecen.
    rotacion = [p for p in paletas if p.get('auto') and p.get('modo') == 'oscuro'
                and isinstance(p.get('tokens'), dict) and 'bg' in p['tokens']]
    for i, a in enumerate(rotacion):
        for b in rotacion[i + 1:]:
            if a['familia'] == b['familia']:
                continue
            d_bg = pc.distancia(a['tokens']['bg'], b['tokens']['bg'])
            d_ac = pc.distancia(a['tokens']['accent'], b['tokens']['accent'])
            if d_bg < 0.02 and d_ac < 0.05:
                errores.append(f'{a["id"]} y {b["id"]}: casi iguales (fondo {d_bg:.3f}, acento {d_ac:.3f})')

    for cid in conms:
        n = sum(1 for p in paletas if p.get('conmemoracion') == cid)
        if n != 1:
            errores.append(f'conmemoración {cid}: {n} paletas (debe haber 1)')

    n = sum(1 for p in rotacion if not p.get('conmemoracion'))
    if n < minimo_rotacion:
        errores.append(f'rotación: {n} paletas automáticas oscuras, mínimo {minimo_rotacion}')
    return errores


def normalizar(nombre):
    """'María Peña' y 'Maria-Pena' → 'maria-pena'."""
    s = unicodedata.normalize('NFKD', nombre).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def _var_css(nombre, texto):
    m = re.search(r'--' + nombre + r'\s*:\s*(#[0-9A-Fa-f]{6})\b', texto)
    return m.group(1).upper() if m else None


# Las SPA anteriores a las paletas con nombre llamaban distinto a sus colores.
VARS_FONDO = ('bg', 'bg-dark-1', 'bg-1')
VARS_ACENTO = ('accent', 'accent-gold', 'accent-coral', 'gold')


def _primera_var(nombres, texto):
    return next((v for v in (_var_css(n, texto) for n in nombres) if v), None)


def inventario(dirs, cat):
    """Paletas usadas en las SPA de `dirs`. Fecha y predicador salen del nombre
    de archivo ({YYYYMMDD}-{Slug}-{Nombre}-{Apellido}.html); la paleta, del
    <meta name="sermon-palette">, o en SPA anteriores, del nombre en un
    comentario o del par --bg/--accent."""
    por_id = {p['id']: p for p in cat['paletas']}
    por_hex = {(p['tokens']['bg'], p['tokens']['accent']): p for p in cat['paletas']}
    usos = []
    for d in dirs:
        for f in sorted(Path(d).glob('*.html')):
            m = NOMBRE_SPA.match(f.name)
            if not m:
                continue
            try:
                fecha = dt.datetime.strptime(m.group(1), '%Y%m%d').date()
            except ValueError:
                continue
            texto = f.read_text(encoding='utf-8', errors='replace')
            meta = META.search(texto)
            p = por_id.get(meta.group(1)) if meta else None
            if p is None:
                p = next((por_id[c] for c in COMENTARIO.findall(texto) if c in por_id), None)
            bg, acento = _primera_var(VARS_FONDO, texto), _primera_var(VARS_ACENTO, texto)
            if p is None and bg and acento:
                p = por_hex.get((bg, acento))
            usos.append({'fecha': fecha, 'predicador': normalizar(f'{m.group(2)} {m.group(3)}'),
                         'id': p['id'] if p else None, 'familia': p['familia'] if p else None,
                         'acento': p['tokens']['accent'] if p else acento, 'archivo': f.name})
    return usos


def reglas_conmemoracion(cat, extra=None):
    """id → (regla, ventana). `extra` (de config-local.md) sobrescribe reglas por id."""
    reglas = {cid: (c.get('regla'), c.get('ventana', 3))
              for cid, c in cat.get('conmemoraciones', {}).items()}
    for cid, regla in (extra or {}).items():
        if cid in reglas:
            reglas[cid] = (regla or None, reglas[cid][1])
    return reglas


def _puntaje(p, temas):
    return sum(2 if i == 0 else 1 for i, t in enumerate(temas) if t in p['temas'])


def _admitida(p, fecha, pred, usos, matices_semana, semanas, regla_pred):
    if semanas is None:
        return True
    for u in usos:
        dias = abs((u['fecha'] - fecha).days)
        misma = u['id'] == p['id'] or u['familia'] == p['familia']
        if misma and dias < semanas * 7:
            return False
        if (regla_pred and u['predicador'] == pred and u['familia'] == p['familia']
                and dias < VENTANA_PREDICADOR * 7):
            return False
    h = pc.hex_a_oklch(p['tokens']['accent'])[2]
    return all(pc.dif_matiz(h, m) >= MATIZ_MINIMO for m in matices_semana)


def _resultado(p, razon, nivel, alternativas):
    return {'id': p['id'], 'nombre': p['nombre'], 'razon': razon, 'nivel': nivel,
            'alternativas': alternativas, 'paleta': p}


def elegir(cat, fecha, predicador, temas, usos, paleta=None, excluir=(), extra_reglas=None):
    """Paleta para un sermón. `temas`: del vocabulario, el principal primero.
    Nunca falla: si las reglas dejan el catálogo vacío, las relaja por niveles."""
    por_id = {p['id']: p for p in cat['paletas']}
    pred = normalizar(predicador)
    temas = list(temas)
    if paleta:
        if paleta not in por_id:
            raise ValueError(f'paleta desconocida: {paleta}')
        return _resultado(por_id[paleta], 'pedida explícitamente', 0, [])

    semana = [u for u in usos if abs((u['fecha'] - fecha).days) <= MISMA_SEMANA_DIAS]
    # Si dos conmemoraciones coinciden (p. ej. Pastor y Reforma a fin de octubre),
    # gana la que toca el tema más importante del sermón.
    candidatas = []
    for cid in cal.activas(fecha, reglas_conmemoracion(cat, extra_reglas)):
        posiciones = [i for i, t in enumerate(temas) if t in cat['conmemoraciones'][cid]['temas']]
        if posiciones:
            candidatas.append((posiciones[0], cid))
    for _, cid in sorted(candidatas):
        p = next((p for p in cat['paletas'] if p['conmemoracion'] == cid), None)
        if p and p['id'] not in excluir and p['id'] not in {u['id'] for u in semana}:
            return _resultado(p, f'conmemoración: {cat["conmemoraciones"][cid]["nombre"]}', 0, [])

    matices_semana = [pc.hex_a_oklch(u['acento'])[2] for u in semana if u['acento']]
    ultimo = {}
    for u in usos:
        if u['id']:
            ultimo[u['id']] = max(ultimo.get(u['id'], dt.date.min), u['fecha'])
    pool = [p for p in cat['paletas'] if p['auto'] and p['modo'] == 'oscuro'
            and not p['conmemoracion'] and p['id'] not in excluir]
    niveles = [(VENTANA_SEMANAS, True), (VENTANA_SEMANAS, False), (8, False), (4, False),
               (0, False), (None, False)]
    for nivel, (semanas, regla_pred) in enumerate(niveles):
        cand = [p for p in pool
                if _admitida(p, fecha, pred, usos, matices_semana, semanas, regla_pred)]
        if not cand:
            continue
        # Más temas en común; a igualdad, la menos usada; luego un desempate estable.
        cand.sort(key=lambda p: (-_puntaje(p, temas), ultimo.get(p['id'], dt.date.min),
                                 hashlib.sha256(f'{fecha}|{pred}|{p["id"]}'.encode()).hexdigest()))
        elegida = cand[0]
        comunes = [t for t in temas if t in elegida['temas']]
        razon = (f'rotación; temas en común: {", ".join(comunes)}' if comunes
                 else 'rotación; ningún tema coincide, va la menos usada')
        if nivel:
            razon += f' (reglas relajadas, nivel {nivel})'
        return _resultado(elegida, razon, nivel, [p['id'] for p in cand[1:3]])
    raise ValueError('no hay paletas en rotación')


def css(p):
    """Bloque :root con las variables de la paleta y sus reglas como comentario."""
    nota = [f'Paleta "{p["id"]}" — {p["nombre"]}.'] + list(p.get('reglas', []))
    lineas = ['  /* ' + nota[0]] + ['     ' + r for r in nota[1:]]
    lineas[-1] += ' */'
    lineas += [f'  --{k.replace("_", "-")}: {p["tokens"][k]};' for k in TOKENS if p['tokens'][k]]
    return ':root {\n' + '\n'.join(lineas) + '\n}'


_ESTILO_MUESTRARIO = """
body { margin: 0; padding: 28px; background: #26262B; color: #E8E8EC;
       font: 14px/1.45 system-ui, 'Noto Sans', sans-serif; }
h1 { font-size: 22px; margin: 0 0 4px; } h2 { font-size: 18px; margin: 34px 0 12px; }
.sub { color: #A8A8B3; margin: 0 0 8px; }
.grilla { display: grid; grid-template-columns: repeat(auto-fill, minmax(330px, 1fr)); gap: 18px; }
.tarjeta { background: #1C1C20; border: 1px solid #3A3A42; border-radius: 12px; overflow: hidden; }
.oscura, .clara { aspect-ratio: 16 / 9; padding: 16px 20px; display: flex; flex-direction: column;
                  justify-content: center; gap: 6px; }
.oscura .kicker, .clara .kicker { font-size: 11px; letter-spacing: .14em; text-transform: uppercase; }
.oscura .titulo, .clara .titulo { font: 600 21px/1.15 'Iowan Old Style', Georgia, 'Noto Serif', serif; }
.filete { width: 56px; height: 3px; border-radius: 2px; }
.texto { font-size: 12.5px; }
.chip { display: inline-block; padding: 1px 8px; border-radius: 99px; font-size: 11px; }
.clara { aspect-ratio: auto; padding: 12px 20px; }
.impresion { background: #FFFFFF; padding: 8px 20px; display: flex; gap: 10px; align-items: center; font-size: 12px; }
.ficha { padding: 10px 14px 12px; font-size: 12px; color: #C9C9D1; }
.ficha code { color: #FFFFFF; font-size: 12.5px; }
.ficha .temas { color: #9A9AA6; }
.ficha .nums { color: #7E7E8A; font-family: ui-monospace, monospace; font-size: 11px; }
"""


def _tarjeta(p, conms):
    t = p['tokens']
    e = html.escape
    tinta = (f'<span style="color:{t["accent_ink"]};font-weight:700">tinta de acento</span>'
             if t['accent_ink'] else f'<span style="color:{t["ink"]};font-weight:800">énfasis en tinta y peso</span>')
    conm = f' · <b>{e(conms[p["conmemoracion"]])}</b>' if p['conmemoracion'] else ''
    nums = (f'texto {pc.contraste(t["text"], t["bg"]):.1f} · acento {pc.contraste(t["accent"], t["bg"]):.1f} · '
            f'brillante {pc.contraste(t["accent_bright"], t["bg"]):.1f} · tinta {pc.contraste(t["ink"], t["paper"]):.1f}')
    clara = p['modo'] == 'claro'  # en las claras, el papel es la identidad y lo oscuro es la interfaz
    oscura = f"""
  <div class="oscura" style="background:linear-gradient(160deg,{t['bg']} 55%,{t['bg_2']})">
    <div class="kicker" style="color:{t['accent_bright']}">{e('Selector y control' if clara else p['ancla'] or 'Lámina')}</div>
    <div class="titulo" style="color:{t['text']}">{e('Interfaz' if clara else p['nombre'])}</div>
    <div class="filete" style="background:{t['accent']}"></div>
    <div class="texto" style="color:{t['text_muted']}">{e('Fondo del selector y del modo control.' if clara else p['inspiracion'])}</div>
    <div><span class="chip" style="background:{t['bg_2']};color:{t['accent_em']};border:1px solid {t['accent']}">énfasis</span></div>
  </div>"""
    papel = f"""
  <div class="clara" style="background:linear-gradient(90deg,{t['paper']} 60%,{t['paper_2']}){';aspect-ratio:16/9' if clara else ''}">
    <div class="kicker" style="color:{t['muted_ink']}">{e(p['ancla'] or 'Lámina') if clara else 'Lámina clara'}</div>
    <div class="titulo" style="color:{t['ink']};font-size:{21 if clara else 17}px">{e(p['nombre']) if clara else 'Así se lee en papel'}</div>
    <div class="texto" style="color:{t['ink_soft']}">{e(p['inspiracion']) + ' · ' if clara else 'Cuerpo del versículo · '}{tinta}</div>
  </div>"""
    return f"""
<div class="tarjeta" data-id="{e(p['id'])}">{papel + oscura if clara else oscura + papel}
  <div class="impresion">
    <span style="color:{t['print_ink']};font-weight:700">Impresión</span>
    <span style="color:{t['print_ink_soft']}">texto secundario</span>
    <span class="filete" style="background:{t['print_rule']};width:40px"></span>
  </div>
  <div class="ficha">
    <code>{e(p['id'])}</code> · {e(p['modo'])}{conm}<br>
    <span class="temas">{e(' · '.join(p['temas']))}</span><br>
    <span class="nums">{nums}</span>
  </div>
</div>"""


def muestrario(cat, salida):
    """HTML con todas las paletas, para revisarlas a ojo antes de usarlas."""
    paletas = cat['paletas']
    conms = {cid: c['nombre'] for cid, c in cat['conmemoraciones'].items()}
    grupos = [
        ('En rotación', 'Las elige el script según los temas, sin repetir.',
         [p for p in paletas if p['auto'] and p['modo'] == 'oscuro' and not p['conmemoracion']]),
        ('Conmemorativas', 'Se usan en su fecha cuando el sermón toca el tema, o si se piden.',
         [p for p in paletas if p['conmemoracion']]),
        ('Solo a pedido', 'Café, claras u originales que no pasan la regla anti-café: solo si se piden.',
         [p for p in paletas if not p['auto'] and not p['conmemoracion']]),
    ]
    cuerpo = ''.join(f'<h2>{e} ({len(ps)})</h2><p class="sub">{html.escape(sub)}</p>'
                     f'<div class="grilla">{"".join(_tarjeta(p, conms) for p in ps)}</div>'
                     for e, sub, ps in grupos)
    doc = (f'<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">'
           f'<meta name="viewport" content="width=device-width, initial-scale=1">'
           f'<title>Muestrario de paletas · /sermon</title><style>{_ESTILO_MUESTRARIO}</style></head>'
           f'<body><h1>Muestrario de paletas · /sermon</h1>'
           f'<p class="sub">{len(paletas)} paletas. Cada tarjeta: lámina oscura, lámina clara, impresión y contrastes.</p>'
           f'{cuerpo}</body></html>')
    Path(salida).write_text(doc, encoding='utf-8')


def _cmd_muestrario(args):
    muestrario(cargar(args.catalogo), args.out)
    print(args.out)
    return 0


def _reglas_extra(lista):
    return dict(r.split('=', 1) for r in lista)


def _cmd_pick(args):
    cat = cargar(args.catalogo)
    temas = [t.strip() for t in args.temas.split(',') if t.strip()]
    fuera = [t for t in temas if t not in cat['temas']]
    if fuera:
        print(f'aviso: temas fuera del vocabulario, se ignoran: {", ".join(fuera)}', file=sys.stderr)
    r = elegir(cat, args.fecha, args.predicador, [t for t in temas if t not in fuera],
               inventario(args.dirs, cat), paleta=args.paleta,
               excluir=[x for x in args.excluir.split(',') if x], extra_reglas=_reglas_extra(args.regla))
    if args.css:
        print(css(r['paleta']))
        return 0
    p = r.pop('paleta')
    r.update({'meta': f'<meta name="sermon-palette" content="{p["id"]}">',
              'ancla': p['ancla'], 'reglas': p['reglas'], 'tokens': p['tokens']})
    print(json.dumps(r, indent=2, ensure_ascii=False))
    return 0


def _cmd_fechas(args):
    cat = cargar(args.catalogo)
    for cid, (regla, ventana) in reglas_conmemoracion(cat, _reglas_extra(args.regla)).items():
        r = cal.rango(regla, args.anio, ventana)
        print(f'{cid:14} {r[0]} → {r[1]}' if r else f'{cid:14} (sin fecha: configúrala en config-local.md)')
    return 0


def _cmd_check(args):
    cat = cargar(args.catalogo)
    paletas = cat['paletas']
    rot = sum(1 for p in paletas if p['auto'] and p['modo'] == 'oscuro' and not p['conmemoracion'])
    conm = sum(1 for p in paletas if p['conmemoracion'])
    print(f'{len(paletas)} paletas: {rot} en rotación, {conm} conmemorativas, '
          f'{len(paletas) - rot - conm} solo a pedido')
    errores = validar(cat)
    for e in errores:
        print('  ✗', e)
    print('OK' if not errores else f'{len(errores)} errores')
    return 1 if errores else 0


def _cmd_derivar(args):
    t = derivar(args.bg, args.accent)
    contrastes = {f'{a}/{b}': round(pc.contraste(t[a], t.get(b, b)), 2)
                  for a, b, _ in UMBRALES if t[a] is not None}
    print(json.dumps({'tokens': t, 'contrastes': contrastes}, indent=2, ensure_ascii=False))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog='palettes.py', description='Paletas de /sermon.')
    sub = ap.add_subparsers(dest='cmd', required=True)
    c = sub.add_parser('check', help='valida el catálogo')
    c.add_argument('--catalogo', default=str(CATALOGO))
    d = sub.add_parser('derivar', help='tokens completos a partir de fondo y acento')
    d.add_argument('--bg', required=True)
    d.add_argument('--accent', required=True)
    k = sub.add_parser('pick', help='elige la paleta de un sermón')
    k.add_argument('--fecha', required=True, type=dt.date.fromisoformat)
    k.add_argument('--predicador', required=True)
    k.add_argument('--temas', default='', help='del vocabulario, separados por coma; el principal primero')
    k.add_argument('--paleta', help='forzar una paleta (incluye café, claras y conmemorativas)')
    k.add_argument('--excluir', default='', help='ids separados por coma')
    k.add_argument('--dirs', nargs='*', default=[], help='presentaciones_dir de las entidades')
    k.add_argument('--regla', action='append', default=[], help='id=REGLA, p. ej. pastor=domingo:2:10')
    k.add_argument('--css', action='store_true', help='imprimir solo el bloque :root')
    k.add_argument('--catalogo', default=str(CATALOGO))
    f = sub.add_parser('fechas', help='conmemoraciones de un año')
    f.add_argument('--anio', type=int, required=True)
    f.add_argument('--regla', action='append', default=[], help='id=REGLA')
    f.add_argument('--catalogo', default=str(CATALOGO))
    m = sub.add_parser('muestrario', help='HTML con todas las paletas para revisarlas a ojo')
    m.add_argument('--out', required=True)
    m.add_argument('--catalogo', default=str(CATALOGO))
    args = ap.parse_args(argv)
    return {'check': _cmd_check, 'derivar': _cmd_derivar, 'pick': _cmd_pick,
            'fechas': _cmd_fechas, 'muestrario': _cmd_muestrario}[args.cmd](args)


if __name__ == '__main__':
    sys.exit(main())
