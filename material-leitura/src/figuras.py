# -*- coding: utf-8 -*-
"""Figuras (ícones monocromáticos Noto Emoji) e blocos visuais de apoio."""
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from base import (FONTES, INK, SOFT, WHITE, LINE, rrect, texto, largura,
                  PALETA, PALETA_L, TEAL, TEAL_L, CORAL, CORAL_L, BLUE_L,
                  AMBER, AMBER_L, PURPLE_L, GREEN_L, PINK_L, GUIDE, linha)

EMOJI = "NotoEmoji"
_registrado = False


def registrar_emoji():
    global _registrado
    if not _registrado:
        pdfmetrics.registerFont(TTFont(EMOJI, os.path.join(FONTES, "NotoEmoji.ttf")))
        _registrado = True


def emoji(c, ch, cx, cy, size, cor=INK):
    """Desenha um emoji monocromático centrado em (cx, cy)."""
    registrar_emoji()
    if "\ufe0f" in ch:
        ch = ch.replace("\ufe0f", "")
    c.saveState()
    c.setFont(EMOJI, size)
    c.setFillColor(cor)
    w = pdfmetrics.stringWidth(ch, EMOJI, size)
    # a altura visual dos emojis ~0.75 do corpo da fonte
    c.drawString(cx - w / 2, cy - size * 0.36, ch)
    c.restoreState()
    return w


def emoji_quadro(c, ch, x, y, w, h, fundo=None, borda=None, r=10, cor=INK,
                 escala=1.0, lw=1.2):
    if fundo is not None:
        rrect(c, x, y, w, h, r, fundo, borda, lw)
    elif borda is not None:
        rrect(c, x, y, w, h, r, None, borda, lw)
    size = min(w, h) * 0.74 * escala
    emoji(c, ch, x + w / 2, y + h / 2, size, cor)


def cartao_figura(c, ch, x, y, w, h, cor_idx=0, legenda=None, size_legenda=15):
    """Bloco colorido com figura e legenda opcional."""
    fundo, borda = PALETA_L[cor_idx % len(PALETA_L)], PALETA[cor_idx % len(PALETA)]
    rrect(c, x, y, w, h, 12, fundo, None)
    alvo = h - (size_legenda * 1.9 if legenda else 0)
    emoji(c, ch, x + w / 2, y + h - alvo / 2 - (size_legenda * 1.4 if legenda else 0),
          min(w, alvo) * 0.72, borda)
    if legenda:
        texto(c, x + w / 2, y + 9, legenda, size_legenda, "Andika-Bold", INK, "c")


def bolinhas_progresso(c, x, y, n, feito=0, r=6, espaco=18, cor=AMBER, cor_vazia=LINE):
    for i in range(n):
        cx = x + i * espaco
        if i < feito:
            c.setFillColor(cor)
            c.circle(cx, y, r, stroke=0, fill=1)
        else:
            c.setFillColor(WHITE)
            c.setStrokeColor(cor_vazia)
            c.setLineWidth(1)
            c.circle(cx, y, r, stroke=1, fill=1)


def checkbox(c, x, y, tam=13, cor=LINE, lw=1.3):
    rrect(c, x, y, tam, tam, 3, WHITE, cor, lw)


def quadro_vazio(c, x, y, w, h, legenda=None, cor=GUIDE, dash=(4, 4)):
    rrect(c, x, y, w, h, 6, None, cor, 0.9, dash)
    if legenda:
        texto(c, x + w / 2, y + h / 2 - 4, legenda, 9, "Andika", SOFT, "c")
