# -*- coding: utf-8 -*-
"""Extração de contornos de glifos (Andika) para gerar letras pontilhadas/tracejadas.

Permite desenhar *qualquer* texto (minúsculas, sílabas, acentos) no mesmo estilo
de traçado usado nas letras maiúsculas construídas.
"""
import math
import os
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen

from base import FONTES

_CACHE = {}


def _fonte(nome="Andika-Regular.ttf"):
    if nome not in _CACHE:
        caminho = os.path.join(FONTES, nome)
        f = TTFont(caminho, lazy=False)
        _CACHE[nome] = (f, f.getGlyphSet(), f["head"].unitsPerEm,
                        f.getBestCmap(), f["hmtx"])
    return _CACHE[nome]


def _flatten_quad(p0, c, p1, passos=14):
    pts = []
    for i in range(1, passos + 1):
        t = i / passos
        mt = 1 - t
        x = mt * mt * p0[0] + 2 * mt * t * c[0] + t * t * p1[0]
        y = mt * mt * p0[1] + 2 * mt * t * c[1] + t * t * p1[1]
        pts.append((x, y))
    return pts


def _flatten_cubic(p0, c1, c2, p1, passos=18):
    pts = []
    for i in range(1, passos + 1):
        t = i / passos
        mt = 1 - t
        x = (mt ** 3 * p0[0] + 3 * mt * mt * t * c1[0] + 3 * mt * t * t * c2[0] + t ** 3 * p1[0])
        y = (mt ** 3 * p0[1] + 3 * mt * mt * t * c1[1] + 3 * mt * t * t * c2[1] + t ** 3 * p1[1])
        pts.append((x, y))
    return pts


def glifo_polidx(char, nome_fonte="Andika-Regular.ttf"):
    """Devolve (largura, [polilinha...]) em unidades da fonte."""
    f, gs, upm, cmap, hmtx = _fonte(nome_fonte)
    gname = cmap.get(ord(char))
    if gname is None:
        return 0, [], upm
    pen = DecomposingRecordingPen(gs)
    gs[gname].draw(pen)
    pen.replay  # já decomposto
    linhas, atual = [], []
    pos = (0, 0)
    inicio = (0, 0)
    for op, args in pen.value:
        if op == "moveTo":
            if len(atual) > 1:
                linhas.append(atual)
            pos = args[0]
            inicio = pos
            atual = [pos]
        elif op == "lineTo":
            pos = args[0]
            atual.append(pos)
        elif op == "qCurveTo":
            pontos = list(args)
            if pontos[-1] is None:  # contorno fechado com ponto implícito
                pontos = pontos[:-1]
                # ponto implícito = média entre primeiro e último
                medio = ((pontos[0][0] + pontos[-1][0]) / 2,
                         (pontos[0][1] + pontos[-1][1]) / 2)
                pontos = pontos + [medio]
            for i in range(len(pontos) - 1):
                ctrl = pontos[i]
                fim = pontos[i + 1]
                atual.extend(_flatten_quad(pos, ctrl, fim))
                pos = fim
        elif op == "curveTo":
            pts = list(args)
            while len(pts) >= 3:
                c1, c2, fim = pts[0], pts[1], pts[2]
                atual.extend(_flatten_cubic(pos, c1, c2, fim))
                pos = fim
                pts = pts[3:]
        elif op == "closePath":
            if len(atual) > 1:
                atual.append(inicio)
                linhas.append(atual)
            atual = []
    if len(atual) > 1:
        linhas.append(atual)
    larg = hmtx[gname][0]
    return larg, linhas, upm


def texto_contornos(txt, nome_fonte="Andika-Regular.ttf", espaco_extra=0.0):
    """Contornos do texto inteiro, alinhados à esquerda na linha de base."""
    x = 0.0
    todas, upm = [], 1000
    for ch in txt:
        if ch == " ":
            x += upm * 0.28 + espaco_extra
            continue
        larg, linhas, upm = glifo_polidx(ch, nome_fonte)
        for ln in linhas:
            todas.append([(x + p[0], p[1]) for p in ln])
        x += larg + espaco_extra
    return x, todas, upm


def medir(txt, size, nome_fonte="Andika-Regular.ttf", espaco_extra=0.0):
    _, _, upm0 = texto_contornos(txt, nome_fonte)
    larg_u, _, upm = texto_contornos(txt, nome_fonte, espaco_extra * upm0 / size if size else 0)
    return larg_u * size / upm


def desenhar_texto(c, txt, x, y, size, modo="solido", cor=None, lw=None,
                   espaco_extra=0.0, nome_fonte="Andika-Regular.ttf",
                   mostrar_inicio=False, dot_espaco=None):
    """Desenha o texto com contornos.

    modo: 'solido' | 'guia' | 'pontilhado' | 'cheio'
    """
    from base import INK, SOFT
    _, _, upm0 = texto_contornos(txt, nome_fonte)
    cor = cor or (INK if modo == "solido" else SOFT)
    larg_u, linhas, upm = texto_contornos(txt, nome_fonte, espaco_extra * upm0 / size)
    s = size / upm
    lw = lw if lw is not None else max(0.7, size * 0.012)
    c.saveState()
    c.setLineCap(1)
    c.setLineJoin(1)
    if modo in ("solido", "cheio"):
        # um único caminho com todos os contornos -> furos (a, o, b) preservados
        cam = c.beginPath()
        for ln in linhas:
            pts = [(x + p[0] * s, y + p[1] * s) for p in ln]
            cam.moveTo(*pts[0])
            for q in pts[1:]:
                cam.lineTo(*q)
            cam.close()
        c.setFillColor(cor)
        # fillMode=1 (nonzero): contornos que se sobrepõem (travessão do t, do f)
        # continuam sólidos; com o modo par-ímpar aparece um quadrado branco.
        c.drawPath(cam, stroke=0, fill=1, fillMode=1)
    else:
        for ln in linhas:
            pts = [(x + p[0] * s, y + p[1] * s) for p in ln]
            if modo == "guia":
                _tracejado(c, pts, cor, lw, max(2.6, size * 0.05), max(2.2, size * 0.04))
            elif modo == "pontilhado":
                r_ponto = max(0.62, min(2.0, size * 0.014))
                _pontilhado(c, pts, cor, r_ponto,
                            dot_espaco or max(3.2, r_ponto * 3.6))
    c.restoreState()
    return larg_u * s


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
    acum, ant = 1e9, pts[0]
    c.circle(ant[0], ant[1], r, stroke=0, fill=1)
    for q in pts[1:]:
        d = math.hypot(q[0] - ant[0], q[1] - ant[1])
        acum += d
        if acum >= espaco:
            c.circle(q[0], q[1], r, stroke=0, fill=1)
            acum = 0
        ant = q
