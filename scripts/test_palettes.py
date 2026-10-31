# SPDX-License-Identifier: AGPL-3.0-or-later
# Pruebas del sistema de paletas de /sermon.
# Uso: python3 -m unittest discover -s scripts -p 'test_palettes.py' -v
import contextlib
import datetime as dt
import io
import json
import tempfile
import unittest
from pathlib import Path

import palette_calendar as cal
import palette_color as pc
import palettes as P


def paleta(pid, familia, bg, accent, temas, auto=True, modo='oscuro', conm=None):
    return {'id': pid, 'nombre': pid, 'familia': familia, 'modo': modo, 'auto': auto,
            'conmemoracion': conm, 'temas': temas, 'ancla': None, 'inspiracion': '',
            'tokens': P.derivar(bg, accent), 'reglas': []}


def catalogo_base():
    """Catálogo sintético: 5 paletas en rotación, una conmemorativa y una café a pedido."""
    return {
        'version': 1,
        'temas': ['esperanza', 'gozo', 'madre', 'familia', 'juicio', 'gracia'],
        'conmemoraciones': {'madre': {'nombre': 'Día de la Madre', 'regla': 'domingo:2:05',
                                      'ventana': 3, 'temas': ['madre']}},
        'paletas': [
            paleta('azul', 'azul', '#0A1428', '#5FA8FF', ['esperanza']),
            paleta('verde', 'verde', '#0B1A12', '#6FC79A', ['esperanza', 'gozo']),
            paleta('violeta', 'violeta', '#0C0F1D', '#8577F2', ['juicio']),
            paleta('rosa', 'rosa', '#12141B', '#DA6B87', ['gracia']),
            paleta('oro', 'oro', '#0C0E14', '#E2B13C', ['gozo']),
            paleta('madre', 'madre', '#1A0B16', '#F28DB2', ['madre'], auto=False, conm='madre'),
            paleta('cafe', 'cafe', '#1A0F0A', '#D4A574', ['esperanza'], auto=False),
        ]}


class TestColor(unittest.TestCase):
    def test_contraste_extremos(self):
        self.assertAlmostEqual(pc.contraste('#FFFFFF', '#000000'), 21.0, places=2)

    def test_ida_y_vuelta_oklch(self):
        for h in ('#0C0E14', '#E2B13C', '#4FD1BE', '#7A1820'):
            self.assertEqual(pc.oklch_a_hex(*pc.hex_a_oklch(h)), h)

    def test_cafe_acentos_conocidos(self):
        # Tostados, arenas y terracotas que el usuario lee como café.
        for h in ('#D4A574', '#B89878', '#A87858', '#E6BC85', '#B86838', '#C9743A', '#C8A858'):
            self.assertTrue(pc.es_cafe(h, 'acento'), h)

    def test_acentos_vivos_no_son_cafe(self):
        # Oros, ámbares y corales vivos de paletas reales que sí funcionaron.
        for h in ('#E2B13C', '#F3CE6A', '#D4AF37', '#FFCF52', '#E8A050', '#E5764A',
                  '#E08B3D', '#FFE3A3', '#B4D455', '#4FD1BE', '#B33A5E', '#FF6F61'):
            self.assertFalse(pc.es_cafe(h, 'acento'), h)

    def test_cafe_fondos_conocidos(self):
        for h in ('#1A0F0A', '#1C0E0A', '#2E160F'):
            self.assertTrue(pc.es_cafe(h, 'fondo'), h)

    def test_fondos_frios_y_joya_no_son_cafe(self):
        for h in ('#0C0E14', '#091417', '#0E1113', '#17091A', '#360A15', '#160E14',
                  '#0A1810', '#150B1F', '#0F1419', '#0D1F5C', '#06402F'):
            self.assertFalse(pc.es_cafe(h, 'fondo'), h)

    def test_ajustar_llega_al_objetivo(self):
        claro = pc.ajustar(0.5, 0.1, 85, '#0C0E14', 7, 'arriba')
        self.assertGreaterEqual(pc.contraste(claro, '#0C0E14'), 7)
        oscuro = pc.ajustar(0.6, 0.05, 260, '#EEEDE9', 7, 'abajo')
        self.assertGreaterEqual(pc.contraste(oscuro, '#EEEDE9'), 7)


class TestCalendario(unittest.TestCase):
    def test_pascua(self):
        for anio, esperada in ((2024, dt.date(2024, 3, 31)), (2025, dt.date(2025, 4, 20)),
                               (2026, dt.date(2026, 4, 5)), (2027, dt.date(2027, 3, 28))):
            self.assertEqual(cal.pascua(anio), esperada)

    def test_domingos_ecuador_2026(self):
        self.assertEqual(cal.domingo_n(2026, 5, 2), dt.date(2026, 5, 10))   # Día de la Madre
        self.assertEqual(cal.domingo_n(2026, 6, 3), dt.date(2026, 6, 21))   # Día del Padre

    def test_adviento(self):
        self.assertEqual(cal.inicio_adviento(2026), dt.date(2026, 11, 29))
        self.assertEqual(cal.inicio_adviento(2022), dt.date(2022, 11, 27))  # Navidad en domingo

    def test_ventanas(self):
        reglas = {'ramos': ('pascua:-7', 3), 'viernes-santo': ('pascua:-2', 1),
                  'fin-de-ano': ('rango:12-26:01-07', 0), 'reforma': ('fija:10-31', 3)}
        self.assertEqual(cal.activas(dt.date(2026, 3, 29), reglas), ['ramos'])
        self.assertIn('viernes-santo', cal.activas(dt.date(2026, 4, 3), reglas))
        self.assertEqual(cal.activas(dt.date(2027, 1, 3), reglas), ['fin-de-ano'])
        self.assertEqual(cal.activas(dt.date(2026, 11, 1), reglas), ['reforma'])
        self.assertEqual(cal.activas(dt.date(2026, 7, 12), reglas), [])

    def test_regla_sin_fecha(self):
        self.assertIsNone(cal.rango(None, 2026, 3))
        self.assertEqual(cal.activas(dt.date(2026, 10, 11), {'pastor': (None, 3)}), [])

    def test_regla_desconocida(self):
        with self.assertRaises(ValueError):
            cal.rango('luna:1', 2026, 3)


class TestCatalogo(unittest.TestCase):
    def test_derivar_cumple_umbrales(self):
        for bg, ac in (('#0C0E14', '#E2B13C'), ('#0D1F5C', '#FFC94A'), ('#06402F', '#FFD966'),
                       ('#1A0B18', '#FF8FC2'), ('#061A1F', '#33D6E8')):
            cat = {'version': 1, 'temas': ['gozo'], 'conmemoraciones': {},
                   'paletas': [paleta('p', 'p', bg, ac, ['gozo'])]}
            self.assertEqual(P.validar(cat, minimo_rotacion=0), [], (bg, ac))

    def test_derivar_brillo_calido_no_cafe(self):
        # Aclarar un naranja quitándole croma da durazno tostado: el brillante debe seguir vivo.
        for bg, ac in (('#04191C', '#FF8F3A'), ('#0B2A6B', '#FF9F45'), ('#0B3A47', '#FF9E80')):
            brillo = P.derivar(bg, ac)['accent_bright']
            self.assertFalse(pc.es_cafe(brillo, 'acento'), (ac, brillo))

    def test_derivar_brillo_no_se_lava(self):
        # En un fondo joya claro, 7.5:1 exigiría blanco: el brillante debe conservar color.
        brillo = P.derivar('#035E63', '#FFA24C')['accent_bright']
        self.assertGreaterEqual(pc.hex_a_oklch(brillo)[1], 0.05, brillo)
        self.assertGreaterEqual(pc.contraste(brillo, '#035E63'), 4.5)

    def test_derivar_sin_tinta_oliva(self):
        # Un limón o una lima oscurecidos para tinta o filete se vuelven oliva apagado.
        def oliva(h):
            L, C, H = pc.hex_a_oklch(h)
            return 95 <= H <= 125 and C > 0.03

        for bg, ac in (('#24125E', '#F2F55A'), ('#0E3A5C', '#C8F25A'), ('#44093A', '#C8F560')):
            t = P.derivar(bg, ac)
            self.assertFalse(t['accent_ink'] and oliva(t['accent_ink']), (ac, t['accent_ink']))
            self.assertFalse(oliva(t['print_rule']), (ac, t['print_rule']))

    def test_derivar_fondo_con_profundidad(self):
        # El segundo tono del fondo (degradados, superficies) tiene que notarse, como en
        # las paletas reales (ΔE ≈ 0.05), también en los fondos joya; y el texto se lee encima.
        for bg, ac in (('#0E0F16', '#FF4F72'), ('#1A0B18', '#FF8FC2'), ('#0D1F5C', '#FFC94A'),
                       ('#06402F', '#FFD966'), ('#4A0D1E', '#FFD166'), ('#024A4F', '#FF6FD8')):
            t = P.derivar(bg, ac)
            self.assertGreaterEqual(pc.distancia(t['bg'], t['bg_2']), 0.05, (bg, t['bg_2']))
            self.assertGreaterEqual(pc.contraste(t['text'], t['bg_2']), 7, (bg, t['bg_2']))
            self.assertFalse(pc.es_cafe(t['bg_2'], 'fondo'), (bg, t['bg_2']))

    def test_derivar_sin_tinta_cafe(self):
        tinta = P.derivar('#0C0E14', '#E2B13C')['accent_ink']
        self.assertTrue(tinta is None or not pc.es_cafe(tinta, 'acento'), tinta)

    def test_catalogo_base_valido(self):
        self.assertEqual(P.validar(catalogo_base(), minimo_rotacion=5), [])

    def test_validar_contraste_bajo(self):
        cat = catalogo_base()
        cat['paletas'][0]['tokens']['text'] = '#333333'
        self.assertTrue(any('text/bg' in e for e in P.validar(cat, 5)))

    def test_validar_cafe_en_rotacion(self):
        cat = catalogo_base()
        cat['paletas'][-1]['auto'] = True
        self.assertTrue(any('café' in e for e in P.validar(cat, 5)))

    def test_validar_tema_fuera_de_vocabulario(self):
        cat = catalogo_base()
        cat['paletas'][0]['temas'] = ['foo']
        self.assertTrue(any('foo' in e for e in P.validar(cat, 5)))

    def test_validar_ids_duplicados(self):
        cat = catalogo_base()
        cat['paletas'][1]['id'] = 'azul'
        self.assertTrue(any('duplicado' in e for e in P.validar(cat, 5)))

    def test_validar_conmemoracion_sin_paleta(self):
        cat = catalogo_base()
        cat['paletas'] = [p for p in cat['paletas'] if p['id'] != 'madre']
        self.assertTrue(any('madre' in e for e in P.validar(cat, 5)))

    def test_validar_minimo_rotacion(self):
        self.assertTrue(any('rotación' in e for e in P.validar(catalogo_base(), 99)))

    def test_validar_distincion(self):
        cat = catalogo_base()
        cat['paletas'].append(paleta('azul2', 'azul2', '#0A1428', '#60A8FF', ['esperanza']))
        self.assertTrue(any('casi iguales' in e for e in P.validar(cat, 5)))


class TestCatalogoReal(unittest.TestCase):
    def test_catalogo_real_valido(self):
        self.assertEqual(P.validar(P.cargar()), [])


FECHA = dt.date(2026, 11, 1)


class TestSeleccion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cat = catalogo_base()
        cls.por_id = {p['id']: p for p in cls.cat['paletas']}

    def uso(self, pid, dias, pred='ana-paz', acento=None):
        p = self.por_id.get(pid)
        return {'fecha': FECHA - dt.timedelta(days=dias), 'predicador': pred,
                'id': pid if p else None, 'familia': p['familia'] if p else None,
                'acento': p['tokens']['accent'] if p else acento, 'archivo': f'{pid}.html'}

    def elegir(self, temas, usos=(), fecha=FECHA, pred='María Peña', **kw):
        return P.elegir(self.cat, fecha, pred, temas, list(usos), **kw)

    def test_explicita_gana(self):
        self.assertEqual(self.elegir(['juicio'], paleta='cafe')['id'], 'cafe')

    def test_por_tema(self):
        self.assertEqual(self.elegir(['juicio'])['id'], 'violeta')

    def test_no_repite_13_semanas(self):
        self.assertEqual(self.elegir(['esperanza'], [self.uso('azul', 14)])['id'], 'verde')
        usos = [self.uso('azul', 14 * 7), self.uso('verde', 14)]
        self.assertEqual(self.elegir(['esperanza'], usos)['id'], 'azul')

    def test_mismo_predicador_26_semanas(self):
        usos = [self.uso('verde', 20 * 7, pred='maria-pena'), self.uso('azul', 7)]
        self.assertNotIn(self.elegir(['esperanza'], usos)['id'], ('azul', 'verde'))
        self.assertEqual(self.elegir(['esperanza'], usos, pred='Otro Nombre')['id'], 'verde')

    def test_misma_semana_matiz(self):
        # Otra SPA de la misma semana con acento naranja: el oro queda a < 45° y se descarta.
        usos = [self.uso('desconocida', 1, acento='#E5764A')]
        self.assertEqual(self.elegir(['gozo'], usos)['id'], 'verde')

    def test_conmemoracion_con_tema(self):
        r = self.elegir(['madre', 'familia'], fecha=dt.date(2026, 5, 10))
        self.assertEqual(r['id'], 'madre')

    def test_conmemoracion_sin_tema(self):
        self.assertEqual(self.elegir(['juicio'], fecha=dt.date(2026, 5, 10))['id'], 'violeta')

    def test_conmemorativa_fuera_de_fecha(self):
        self.assertNotEqual(self.elegir(['madre'], fecha=dt.date(2026, 7, 12))['id'], 'madre')

    def test_determinista(self):
        self.assertEqual(self.elegir(['familia'])['id'], self.elegir(['familia'])['id'])

    def test_relaja_sin_fallar(self):
        usos = [self.uso(pid, 7 * i) for i, pid in enumerate(('azul', 'verde', 'violeta', 'rosa', 'oro'))]
        self.assertGreater(self.elegir(['gozo'], usos)['nivel'], 0)

    def test_inventario(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d, '20261011-Algo-Maria-Pena.html').write_text(
                '<head><meta name="sermon-palette" content="oro"></head>')
            Path(d, '20260920-Otro-Ana-Paz.html').write_text('/* Paleta "rosa" — prueba */')
            Path(d, '20260801-Tres-Ana-Paz.html').write_text(':root { --bg: #0A1428; --accent: #5FA8FF; }')
            Path(d, '20260705-Cuatro-Ana-Paz.html').write_text(
                ':root { --bg-dark-1: #0B1A12; --accent-gold: #6FC79A; }')
            Path(d, 'notas.html').write_text('<p>sin fecha</p>')
            usos = sorted(P.inventario([d], self.cat), key=lambda u: u['fecha'])
        self.assertEqual([u['id'] for u in usos], ['verde', 'azul', 'rosa', 'oro'])
        self.assertEqual(usos[3]['predicador'], 'maria-pena')

    def test_normalizar(self):
        self.assertEqual(P.normalizar('María Peña'), 'maria-pena')
        self.assertEqual(P.normalizar('Maria-Pena'), 'maria-pena')

    def test_css(self):
        p = self.por_id['oro']
        c = P.css(p)
        for esperado in ('--bg:', '--accent-bright:', 'oro'):
            self.assertIn(esperado, c)
        if p['tokens']['accent_ink'] is None:
            self.assertNotIn('--accent-ink', c)

    def _cli(self, *argv):
        with tempfile.TemporaryDirectory() as d:
            ruta = Path(d, 'catalog.json')
            ruta.write_text(json.dumps(self.cat), encoding='utf-8')
            salida = io.StringIO()
            with contextlib.redirect_stdout(salida):
                codigo = P.main([*argv, '--catalogo', str(ruta)])
        return codigo, salida.getvalue()

    def test_muestrario(self):
        with tempfile.TemporaryDirectory() as d:
            ruta = Path(d, 'muestrario.html')
            P.muestrario(self.cat, ruta)
            texto = ruta.read_text(encoding='utf-8')
        for p in self.cat['paletas']:
            self.assertIn(f'data-id="{p["id"]}"', texto)
        self.assertIn('Día de la Madre', texto)

    def test_cli_fechas(self):
        codigo, salida = self._cli('fechas', '--anio', '2026')
        self.assertEqual(codigo, 0)
        self.assertIn('2026-05-07', salida)

    def test_cli_pick(self):
        codigo, salida = self._cli('pick', '--fecha', '2026-11-01', '--predicador', 'María Peña',
                                   '--temas', 'juicio')
        self.assertEqual(codigo, 0)
        self.assertEqual(json.loads(salida)['id'], 'violeta')


if __name__ == '__main__':
    unittest.main()
