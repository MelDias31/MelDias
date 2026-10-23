# -*- coding: utf-8 -*-
"""Traçado das letras maiúsculas de forma (bastão) em uma grade de 100 pontos."""
import math
from base import INK, SOFT, LINE, GREEN, TEAL, BLUE, WHITE, CORAL, AMBER, GUIDE

K = 0.5523


def _p(x, y):
    return (float(x), float(y))


def L(x1, y1, x2, y2, n=1):
    return [(_p(x1, y1), _p(x2, y2), [])] if n == 1 else []


def C(x0, y0, x1, y1, x2, y2, x3, y3, passos=16):
    pts = []
    for i in range(1, passos + 1):
        t = i / passos
        mt = 1 - t
        x = (mt ** 3 * x0 + 3 * mt * mt * t * x1 + 3 * mt * t * t * x2 + t ** 3 * x3)
        y = (mt ** 3 * y0 + 3 * mt * mt * t * y1 + 3 * mt * t * t * y2 + t ** 3 * y3)
        pts.append(_p(x, y))
    return pts


def A(cx, cy, rx, ry, a0, a1, passos=36):
    """Arco de elipse em graus (sentinela positivo = anti-horário)."""
    pts = []
    for i in range(1, passos + 1):
        t = a0 + (a1 - a0) * i / passos
        pts.append(_p(cx + rx * math.cos(math.radians(t)),
                       cy + ry * math.sin(math.radians(t))))
    return pts


# Cada letra: (largura, [ [pontos...], ... ])
def _defs():
    d = {}

    d["A"] = (66, [
        [_p(33, 100), _p(0, 0)],
        [_p(33, 100), _p(66, 0)],
        [_p(11, 33), _p(55, 33)],
    ])

    d["B"] = (58, [
        [_p(0, 100), _p(0, 0)],
        [_p(0, 100)] + C(0, 100, 40, 100, 56, 96, 56, 76) + C(56, 76, 56, 58, 40, 52, 0, 52),
        [_p(0, 52)] + C(0, 52, 44, 52, 58, 46, 58, 26) + C(58, 26, 58, 6, 44, 0, 0, 0),
    ])

    d["C"] = (62, [
        A(31, 50, 31, 48, 42, 318, 40),
    ])

    d["D"] = (58, [
        [_p(0, 100), _p(0, 0)],
        [_p(0, 100)] + C(0, 100, 44, 100, 58, 84, 58, 50)
        + C(58, 50, 58, 16, 44, 0, 0, 0),
    ])

    d["E"] = (54, [
        [_p(0, 100), _p(0, 0)],
        [_p(0, 100), _p(44, 100)],
        [_p(0, 50), _p(37, 50)],
        [_p(0, 0), _p(44, 0)],
    ])

    d["F"] = (52, [
        [_p(0, 100), _p(0, 0)],
        [_p(0, 100), _p(44, 100)],
        [_p(0, 50), _p(37, 50)],
    ])

    d["G"] = (62, [
        A(31, 50, 31, 48, 42, 340, 40),
        [_p(60.1, 33.6), _p(60.1, 50), _p(38, 50)],
    ])

    d["H"] = (62, [
        [_p(0, 100), _p(0, 0)],
        [_p(62, 100), _p(62, 0)],
        [_p(0, 50), _p(62, 50)],
    ])

    d["I"] = (26, [
        [_p(13, 100), _p(13, 0)],
        [_p(0, 100), _p(26, 100)],
        [_p(0, 0), _p(26, 0)],
    ])

    d["J"] = (46, [
        [_p(0, 100), _p(40, 100)],
        [_p(30, 100), _p(30, 30)] + C(30, 30, 30, 6, 8, 0, 2, 28),
    ])

    d["K"] = (56, [
        [_p(0, 100), _p(0, 0)],
        [_p(54, 100), _p(0, 40)],
        [_p(17, 58), _p(56, 0)],
    ])

    d["L"] = (46, [
        [_p(0, 100), _p(0, 0)],
        [_p(0, 0), _p(44, 0)],
    ])

    d["M"] = (78, [
        [_p(0, 0), _p(0, 100), _p(39, 40), _p(78, 100), _p(78, 0)],
    ])

    d["N"] = (66, [
        [_p(0, 0), _p(0, 100), _p(66, 0), _p(66, 100)],
    ])

    d["O"] = (66, [
        A(33, 50, 33, 48, 90, 450, 60),
    ])

    d["P"] = (58, [
        [_p(0, 100), _p(0, 0)],
        [_p(0, 100)] + C(0, 100, 42, 100, 56, 96, 56, 74)
        + C(56, 74, 56, 54, 42, 48, 0, 48),
    ])

    d["Q"] = (70, [
        A(33, 50, 33, 48, 90, 450, 60),
        [_p(42, 20), _p(70, -6)],
    ])

    d["R"] = (58, [
        [_p(0, 100), _p(0, 0)],
        [_p(0, 100)] + C(0, 100, 42, 100, 56, 96, 56, 74)
        + C(56, 74, 56, 54, 42, 48, 0, 48),
        [_p(24, 48), _p(56, 0)],
    ])

    d["S"] = (56, [
        [_p(49, 82)] + C(49, 82, 34, 100, 6, 98, 6, 78)
        + C(6, 78, 6, 60, 26, 58, 40, 48)
        + C(40, 48, 54, 38, 52, 10, 28, 3)
        + C(28, 3, 13, -1, 5, 6, 4, 16),
    ])

    d["T"] = (60, [
        [_p(0, 100), _p(60, 100)],
        [_p(30, 100), _p(30, 0)],
    ])

    d["U"] = (64, [
        [_p(0, 100), _p(0, 34)] + C(0, 34, 0, 2, 64, 2, 64, 34)
        + [_p(64, 34), _p(64, 100)],
    ])

    d["V"] = (64, [
        [_p(0, 100), _p(32, 0), _p(64, 100)],
    ])

    d["W"] = (80, [
        [_p(0, 100), _p(20, 0), _p(40, 62), _p(60, 0), _p(80, 100)],
    ])

    d["X"] = (60, [
        [_p(0, 100), _p(60, 0)],
        [_p(0, 0), _p(60, 100)],
    ])

    d["Y"] = (60, [
        [_p(0, 100), _p(30, 50)],
        [_p(30, 50), _p(30, 0)],
        [_p(60, 100), _p(30, 50)],
    ])

    d["Z"] = (56, [
        [_p(0, 100), _p(56, 100), _p(0, 0), _p(56, 0)],
    ])
    return d


DEFS = _defs()


def _amostrar(pontos, passo=0.8):
    """Reamostra a polilinha em passos aproximadamente iguais."""
    saida = [pontos[0]]
    for i in range(1, len(pontos)):
        x1, y1 = saida[-1]
        x2, y2 = pontos[i]
        d = math.hypot(x2 - x1, y2 - y1)
        if d < 1e-9:
            continue
        n = max(1, int(d / passo))
        for k in range(1, n + 1):
            saida.append((x1 + (x2 - x1) * k / n, y1 + (y2 - y1) * k / n))
    return saida


def pontos_letra(letra):
    return [p for stroke in DEFS[letra][1] for p in stroke]


class Transform:
    def __init__(self, x, y, altura, largura_extra=0):
        self.larg = DEFS and 0
        self.x = x
        self.y = y
        self.s = altura / 100.0
        self.wletra = 0

    def __call__(self, p):
        return (self.x + p[0] * self.s, self.y + p[1] * self.s)


def _pts(stroke, tr):
    return [tr(p) for p in _amostrar(stroke)]


def desenhar_letra(c, letra, x, y, altura, modo="guia", cor=None, largura_linha=None,
                   mostrar_numeros=False, mostrar_seta=True, mostrar_inicio=True,
                   cor_numero=TEAL, fonte_num=None):
    """Desenha o traçado da letra.

    modo: 'solido' | 'guia' (tracejado) | 'pontilhado' | 'cheio' (preenchido bem claro)
    """
    larg, strokes = DEFS[letra]
    tr = Transform(x, y, altura)
    lw = largura_linha if largura_linha is not None else max(1.0, altura * 0.018)
    cor = cor or (SOFT if modo != "solido" else INK)

    c.saveState()
    c.setLineCap(1)
    c.setLineJoin(1)
    for idx, stroke in enumerate(strokes):
        pts = _pts(stroke, tr)
        if modo == "guia":
            _tracejado(c, pts, cor, lw, 4.5, 3.6)
        elif modo == "pontilhado":
            r_ponto = max(0.9, min(2.0, altura * 0.020, lw * 1.1))
            _pontilhado(c, pts, cor, r_ponto, max(3.2, r_ponto * 3.4))
        elif modo == "solido":
            c.setStrokeColor(cor)
            c.setLineWidth(lw)
            p = c.beginPath()
            p.moveTo(*pts[0])
            for q in pts[1:]:
                p.lineTo(*q)
            c.drawPath(p)
        elif modo == "cheio":
            # traço grosso e bem claro (letra "de bolinha" para colorir)
            c.setStrokeColor(cor)
            c.setLineWidth(altura * 0.20)
            c.setLineCap(1)
            p = c.beginPath()
            p.moveTo(*pts[0])
            for q in pts[1:]:
                p.lineTo(*q)
            c.drawPath(p)

    # marcador de início (bolinha verde) ou número do passo
    if mostrar_inicio and not mostrar_numeros:
        p0 = tr(_amostrar(strokes[0])[0])
        c.setFillColor(GREEN)
        c.circle(p0[0], p0[1], max(2.0, altura * 0.035), stroke=0, fill=1)
        c.setFillColor(WHITE)
        c.circle(p0[0], p0[1], max(0.8, altura * 0.013), stroke=0, fill=1)

    if mostrar_seta:
        for stroke in strokes:
            pts = _pts(stroke, tr)
            _seta_fim(c, pts, cor if modo != "solido" else INK, max(1.2, lw * 0.9),
                      max(3.0, altura * 0.05))

    if mostrar_numeros:
        fn = fonte_num or max(6.0, altura * 0.105)
        raio = fn * 0.95
        # centro da letra (para empurrar os números para fora)
        todos = [p for st in strokes for p in _pts(st, tr)]
        cxs = sum(p[0] for p in todos) / len(todos)
        cys = sum(p[1] for p in todos) / len(todos)
        postos = []
        base = math.radians(90)
        for i, stroke in enumerate(strokes):
            pts = _pts(stroke, tr)
            px, py = pts[0]
            ang0 = math.atan2(py - cys, px - cxs)
            escolhido = None
            for k in range(48):
                ang = ang0 + base * (0 if k == 0 else ((k + 1) // 2) * (1 if k % 2 else -1) / 2)
                dist = raio * (1.6 + 0.55 * (k // 12))
                cx = px + math.cos(ang) * dist
                cy = py + math.sin(ang) * dist
                if all(math.hypot(cx - ax, cy - ay) > raio * 2.4 for ax, ay in postos):
                    escolhido = (cx, cy)
                    break
            if escolhido is None:
                escolhido = (px, py + raio * 2)
            postos.append(escolhido)
            _numero(c, escolhido[0], escolhido[1], i + 1, fn, cor_numero)
    c.restoreState()
    return larg * tr.s


def _numero(c, cx, cy, n, tam, cor):
    r = tam * 0.86
    c.setFillColor(WHITE)
    c.setStrokeColor(cor)
    c.setLineWidth(max(0.8, tam * 0.10))
    c.circle(cx, cy, r, stroke=1, fill=1)
    c.setFillColor(cor)
    c.setFont("Andika-Bold", tam)
    c.drawCentredString(cx, cy - tam * 0.34, str(n))


def _tracejado(c, pts, cor, lw, dash, gap):
    c.setStrokeColor(cor)
    c.setLineWidth(lw)
    c.setLineCap(0)
    c.setDash([dash, gap])
    p = c.beginPath()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    c.drawPath(p)
    c.setDash([])


def _pontilhado(c, pts, cor, r, espaco):
    c.setFillColor(cor)
    acum, ant = 0.0, pts[0]
    c.circle(ant[0], ant[1], r, stroke=0, fill=1)
    for q in pts[1:]:
        d = math.hypot(q[0] - ant[0], q[1] - ant[1])
        acum += d
        if acum >= espaco:
            c.circle(q[0], q[1], r, stroke=0, fill=1)
            acum = 0
        ant = q


def _seta_fim(c, pts, cor, lw, tam):
    if len(pts) < 3:
        return
    (x1, y1), (x2, y2) = pts[-6], pts[-1]
    ang = math.atan2(y2 - y1, x2 - x1)
    c.saveState()
    c.setFillColor(cor)
    c.translate(x2, y2)
    c.rotate(math.degrees(ang))
    p = c.beginPath()
    p.moveTo(0, 0)
    p.lineTo(-tam * 1.7, tam * 0.9)
    p.lineTo(-tam * 1.7, -tam * 0.9)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()


def letra_solida(c, letra, x, y, altura, cor, largura_linha=None, alpha_pontos=False):
    desenhar_letra(c, letra, x, y, altura, "solido", cor, largura_linha,
                   False, False, False)


def desenhar_glifo(c, letra, x, y, tamanho_fonte, modo="contorno", cor=None,
                   largura=1.2):
    """Desenha o glifo real da fonte Andika (para referência visual)."""
    c.saveState()
    c.setFont("Andika-Bold", tamanho_fonte)
    if modo == "contorno":
        c.setStrokeColor(cor or LINE)
        c.setLineWidth(largura)
        c.setFillColor(WHITE)
        c.setLineJoin(1)
        c.setTextRenderMode(1)
        c.drawString(x, y, letra)
        c.setTextRenderMode(0)
    else:
        c.setFillColor(cor or INK)
        c.drawString(x, y, letra)
    c.restoreState()
