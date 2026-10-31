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
palette_calendar.py — fechas conmemorativas para las paletas de /sermon.

Reglas (texto, para que config-local.md pueda sobrescribirlas):
  fija:MM-DD            fecha fija, p. ej. fija:10-31
  domingo:N:MM          N-ésimo domingo del mes, p. ej. domingo:2:05
  pascua:±D             días desde Pascua, p. ej. pascua:-7 (Ramos)
  adviento              del 1.er domingo de Adviento al 25 de diciembre
  rango:MM-DD:MM-DD     rango fijo; puede cruzar el año

Las fechas puntuales valen con una ventana de ±N días: el domingo de un día
que cae entre semana también cuenta.
"""
import datetime as dt


def pascua(anio):
    """Domingo de Pascua (algoritmo gregoriano anónimo de Meeus/Jones/Butcher)."""
    a = anio % 19
    b, c = divmod(anio, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mes, dia = divmod(h + l - 7 * m + 114, 31)
    return dt.date(anio, mes, dia + 1)


def domingo_n(anio, mes, n):
    primero = dt.date(anio, mes, 1)
    primero += dt.timedelta(days=(6 - primero.weekday()) % 7)
    return primero + dt.timedelta(weeks=n - 1)


def inicio_adviento(anio):
    """Primer domingo de Adviento: cuatro domingos antes de Navidad."""
    navidad = dt.date(anio, 12, 25)
    cuarto = navidad - dt.timedelta(days=(navidad.weekday() + 1) % 7 or 7)
    return cuarto - dt.timedelta(weeks=3)


def rango(regla, anio, ventana):
    """(inicio, fin) de la conmemoración en `anio`, o None si la regla no tiene fecha."""
    if not regla:
        return None
    tipo, _, arg = regla.partition(':')
    if tipo == 'adviento':
        return inicio_adviento(anio), dt.date(anio, 12, 25)
    if tipo == 'rango':
        desde, hasta = (tuple(map(int, x.split('-'))) for x in arg.split(':'))
        fin_anio = anio + 1 if hasta < desde else anio
        return dt.date(anio, *desde), dt.date(fin_anio, *hasta)
    if tipo == 'fija':
        mes, dia = map(int, arg.split('-'))
        centro = dt.date(anio, mes, dia)
    elif tipo == 'domingo':
        n, mes = map(int, arg.split(':'))
        centro = domingo_n(anio, mes, n)
    elif tipo == 'pascua':
        centro = pascua(anio) + dt.timedelta(days=int(arg))
    else:
        raise ValueError(f'regla desconocida: {regla}')
    margen = dt.timedelta(days=ventana)
    return centro - margen, centro + margen


def activas(fecha, reglas):
    """Ids de las conmemoraciones cuya ventana contiene `fecha`.
    `reglas`: id → (regla o None, ventana en días)."""
    ids = []
    for cid, (regla, ventana) in reglas.items():
        for anio in (fecha.year - 1, fecha.year):  # los rangos pueden venir del año anterior
            r = rango(regla, anio, ventana)
            if r and r[0] <= fecha <= r[1]:
                ids.append(cid)
                break
    return ids
