# -*- coding: utf-8 -*-
"""Base de desenho: fontes, cores, elementos de página e utilidades."""
import os
import math
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as rl_canvas

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTES = os.path.join(RAIZ, "fontes")
PDF = os.path.join(RAIZ, "pdf")

W, H = A4                      # 595.27 x 841.89 pt
M = 15 * mm                    # margem padrão

# ---------------------------------------------------------------- paleta
INK    = HexColor("#2B2D42")
SOFT   = HexColor("#6B6F80")
LINE   = HexColor("#C9CDD4")
GUIDE  = HexColor("#AEB6C2")

TEAL   = HexColor("#1F8A7E")
TEAL_L = HexColor("#D6EFEA")
CORAL  = HexColor("#E0674B")
CORAL_L= HexColor("#FBE0D8")
AMBER  = HexColor("#D9902F")
AMBER_L= HexColor("#FCEFD6")
BLUE   = HexColor("#3E6F8E")
BLUE_L = HexColor("#DCEAF2")
PURPLE = HexColor("#6F5E86")
PURPLE_L=HexColor("#E9E2F0")
PINK   = HexColor("#D2719A")
PINK_L = HexColor("#F9E2EB")
GREEN  = HexColor("#4F8A4B")
GREEN_L= HexColor("#E2F0DC")
WHITE  = HexColor("#FFFFFF")
PAPER  = HexColor("#FFFFFF")
CREAM  = HexColor("#FDF8EE")

PALETA = [TEAL, CORAL, BLUE, PURPLE, AMBER, GREEN, PINK]
PALETA_L = [TEAL_L, CORAL_L, BLUE_L, PURPLE_L, AMBER_L, GREEN_L, PINK_L]

FONT = "Andika"
FONT_B = "Andika-Bold"
FONT_I = "Andika-Italic"


def registrar_fontes():
    pdfmetrics.registerFont(TTFont(FONT, os.path.join(FONTES, "Andika-Regular.ttf")))
    pdfmetrics.registerFont(TTFont(FONT_B, os.path.join(FONTES, "Andika-Bold.ttf")))
    pdfmetrics.registerFont(TTFont(FONT_I, os.path.join(FONTES, "Andika-Italic.ttf")))
    pdfmetrics.registerFontFamily(FONT, normal=FONT, bold=FONT_B, italic=FONT_I,
                                  boldItalic=FONT_B)


# ---------------------------------------------------------------- texto
def largura(txt, size, font=FONT):
    return pdfmetrics.stringWidth(txt, font, size)


def texto(c, x, y, txt, size=11, font=FONT, cor=INK, align="l", charspace=0.0):
    c.setFont(font, size)
    c.setFillColor(cor)
    if charspace:
        c._charSpace = charspace
    if align == "l":
        c.drawString(x, y, txt)
    elif align == "c":
        c.drawCentredString(x, y, txt)
    else:
        c.drawRightString(x, y, txt)
    if charspace:
        c._charSpace = 0


def quebrar(txt, larg, size, font=FONT):
    palavras, linhas, atual = txt.split(), [], ""
    for p in palavras:
        teste = (atual + " " + p).strip()
        if largura(teste, size, font) <= larg:
            atual = teste
        else:
            if atual:
                linhas.append(atual)
            atual = p
    if atual:
        linhas.append(atual)
    return linhas


def paragrafo(c, x, y, larg, txt, size=11, font=FONT, cor=INK, entrelinha=None,
              align="l"):
    entrelinha = entrelinha or size * 1.42
    for i, ln in enumerate(quebrar(txt, larg, size, font)):
        if align == "c":
            texto(c, x + larg / 2, y - i * entrelinha, ln, size, font, cor, "c")
        else:
            texto(c, x, y - i * entrelinha, ln, size, font, cor, align)


def paragrafo_altura(txt, larg, size, font=FONT, entrelinha=None):
    entrelinha = entrelinha or size * 1.42
    return len(quebrar(txt, larg, size, font)) * entrelinha


# ---------------------------------------------------------------- formas
def rrect(c, x, y, w, h, r=8, fill=None, stroke=None, lw=1.2, dash=None):
    c.saveState()
    if fill is not None:
        c.setFillColor(fill)
    if stroke is not None:
        c.setStrokeColor(stroke)
        c.setLineWidth(lw)
        c.setLineJoin(1)
        c.setLineCap(1)
    if dash:
        c.setDash(dash)
    c.roundRect(x, y, w, h, r, stroke=1 if stroke is not None else 0,
                fill=1 if fill is not None else 0)
    c.restoreState()


def caixa(c, x, y, w, h, fill=None, stroke=None, lw=1.2, dash=None, r=0):
    rrect(c, x, y, w, h, r, fill, stroke, lw, dash)


def linha(c, x1, y1, x2, y2, cor=LINE, lw=1, dash=None):
    c.saveState()
    c.setStrokeColor(cor)
    c.setLineWidth(lw)
    c.setLineCap(1)
    if dash:
        c.setDash(dash)
    c.line(x1, y1, x2, y2)
    c.restoreState()


def estrela(c, cx, cy, r, fill=AMBER, stroke=None, lw=1.2, pontos=5):
    c.saveState()
    c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
        c.setLineWidth(lw)
    p = c.beginPath()
    for i in range(pontos * 2):
        ang = math.pi / 2 + i * math.pi / pontos
        rr = r if i % 2 == 0 else r * 0.42
        x, y = cx + rr * math.cos(ang), cy + rr * math.sin(ang)
        if i == 0:
            p.moveTo(x, y)
        else:
            p.lineTo(x, y)
    p.close()
    c.drawPath(p, stroke=1 if stroke else 0, fill=1)
    c.restoreState()


def coracao(c, cx, cy, r, fill=CORAL, stroke=None):
    c.saveState()
    c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
        c.setLineWidth(1)
    p = c.beginPath()
    p.moveTo(cx, cy - r * 0.9)
    p.curveTo(cx - r * 1.5, cy + r * 0.35, cx - r * 0.5, cy + r * 1.35, cx, cy + r * 0.45)
    p.curveTo(cx + r * 0.5, cy + r * 1.35, cx + r * 1.5, cy + r * 0.35, cx, cy - r * 0.9)
    p.close()
    c.drawPath(p, stroke=1 if stroke else 0, fill=1)
    c.restoreState()


def check(c, cx, cy, r, cor=GREEN, lw=2.4):
    c.saveState()
    c.setStrokeColor(cor)
    c.setLineWidth(lw)
    c.setLineCap(1)
    c.setLineJoin(1)
    p = c.beginPath()
    p.moveTo(cx - r, cy)
    p.lineTo(cx - r * 0.25, cy - r * 0.8)
    p.lineTo(cx + r, cy + r * 0.85)
    c.drawPath(p)
    c.restoreState()


def seta(c, x1, y1, x2, y2, cor=INK, lw=2, tamanho=6):
    ang = math.atan2(y2 - y1, x2 - x1)
    linha(c, x1, y1, x2, y2, cor, lw)
    c.saveState()
    c.setFillColor(cor)
    c.translate(x2, y2)
    c.rotate(math.degrees(ang))
    p = c.beginPath()
    p.moveTo(0, 0)
    p.lineTo(-tamanho * 1.6, tamanho * 0.8)
    p.lineTo(-tamanho * 1.6, -tamanho * 0.8)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()


# ---------------------------------------------------------------- linha-guia
def pauta(c, x, y, w, altura, cor=GUIDE, mostrar_meio=True, lw=0.9):
    """Linha do céu (topo), linha do meio (tracejada) e linha da grama (base)."""
    linha(c, x, y + altura, x + w, y + altura, cor, lw)
    if mostrar_meio:
        linha(c, x, y + altura / 2, x + w, y + altura / 2, cor, lw * 0.8, dash=[3, 4])
    linha(c, x, y, x + w, y, cor, lw)


# ---------------------------------------------------------------- página
def fundo(c, cor=WHITE):
    c.setFillColor(cor)
    c.rect(0, 0, W, H, stroke=0, fill=1)


def faixa_titulo(c, titulo, sub=None, cor=TEAL, cor_fundo=TEAL_L, icone=None,
                 etiqueta=None):
    """Cabeçalho compacto: uma faixa arredondada no topo."""
    topo = H - M
    alt = 26 * mm if sub else 19 * mm
    rrect(c, M, topo - alt, W - 2 * M, alt, 10, cor_fundo, None)
    # barrinha colorida à esquerda
    c.setFillColor(cor)
    c.roundRect(M, topo - alt, 6, alt, 3, stroke=0, fill=1)

    x = M + 11 * mm
    if icone:
        icone(c, M + 12 * mm, topo - alt / 2, 7.5 * mm, cor)
        x = M + 23 * mm
    y = topo - 8.6 * mm if sub else topo - alt / 2 - 3.2 * mm
    texto(c, x, y, titulo, 17, FONT_B, cor)
    if etiqueta:
        texto(c, W - M - 5 * mm, y, etiqueta, 9, FONT, SOFT, align="r")
    if sub:
        texto(c, x, y - 6.2 * mm, sub, 10.5, FONT, INK)
    return topo - alt


def rodape(c, pag=None, total=None, nota="Material de apoio à alfabetização • uso livre em casa e na escola", cor=SOFT):
    y = M - 6
    linha(c, M, y + 9, W - M, y + 9, HexColor("#E4E7EC"), 0.8)
    texto(c, M, y - 1, nota, 7.5, FONT, cor)
    if pag is not None:
        txt = f"{pag}" if total is None else f"{pag} / {total}"
        texto(c, W - M, y - 1, txt, 8, FONT_B, cor, align="r")


def cantos_decorativos(c, cor=AMBER_L):
    """Pequenos enfeites discretos nos cantos (não competem com a tarefa)."""
    c.saveState()
    c.setFillColor(cor)
    c.circle(W - M - 2 * mm, H - M - 2 * mm, 1.6 * mm, stroke=0, fill=1)
    c.restoreState()


# ---------------------------------------------------------------- mascote
def coruja(c, cx, cy, r, corpo=AMBER, asa=AMBER_L, olho=WHITE, bico=CORAL, cor_linha=INK, dormindo=False):
    """Mascote: uma coruja simples e amigável. r = raio aproximado (altura/2)."""
    lw = max(0.9, r * 0.035)
    c.saveState()
    c.setLineJoin(1)
    # corpo
    c.setFillColor(corpo)
    c.setStrokeColor(cor_linha)
    c.setLineWidth(lw)
    p = c.beginPath()
    p.moveTo(cx - r * 0.82, cy + r * 0.15)
    p.curveTo(cx - r * 0.95, cy - r * 1.05, cx + r * 0.95, cy - r * 1.05, cx + r * 0.82, cy + r * 0.15)
    p.curveTo(cx + r * 0.72, cy + r * 0.85, cx + r * 0.42, cy + r * 0.95, cx + r * 0.26, cy + r * 0.72)
    p.lineTo(cx, cy + r * 0.9)
    p.lineTo(cx - r * 0.26, cy + r * 0.72)
    p.curveTo(cx - r * 0.42, cy + r * 0.95, cx - r * 0.72, cy + r * 0.85, cx - r * 0.82, cy + r * 0.15)
    p.close()
    c.drawPath(p, stroke=1, fill=1)

    # orelhas/tufos (integrados ao corpo)
    c.setFillColor(corpo)
    c.setStrokeColor(cor_linha)
    c.setLineWidth(lw)
    for s in (-1, 1):
        p = c.beginPath()
        p.moveTo(cx + s * r * 0.74, cy + r * 0.52)
        p.curveTo(cx + s * r * 0.92, cy + r * 0.95, cx + s * r * 0.78, cy + r * 1.18,
                  cx + s * r * 0.66, cy + r * 1.22)
        p.curveTo(cx + s * r * 0.52, cy + r * 1.00, cx + s * r * 0.40, cy + r * 0.86,
                  cx + s * r * 0.30, cy + r * 0.78)
        p.close()
        c.drawPath(p, stroke=1, fill=1)

    # olhos
    for s in (-1, 1):
        c.setFillColor(olho)
        c.setStrokeColor(cor_linha)
        c.setLineWidth(lw)
        c.circle(cx + s * r * 0.34, cy + r * 0.34, r * 0.29, stroke=1, fill=1)
        if dormindo:
            c.setStrokeColor(cor_linha)
            c.setLineWidth(lw * 1.4)
            c.arc(cx + s * r * 0.34 - r * 0.18, cy + r * 0.28,
                  cx + s * r * 0.34 + r * 0.18, cy + r * 0.42, 200, 140)
        else:
            c.setFillColor(INK)
            c.circle(cx + s * r * 0.34 + s * r * 0.04, cy + r * 0.32, r * 0.115, stroke=0, fill=1)
            c.setFillColor(WHITE)
            c.circle(cx + s * r * 0.34 + s * r * 0.09, cy + r * 0.37, r * 0.042, stroke=0, fill=1)

    # bico
    c.setFillColor(bico)
    p = c.beginPath()
    p.moveTo(cx - r * 0.13, cy + r * 0.17)
    p.lineTo(cx + r * 0.13, cy + r * 0.17)
    p.lineTo(cx, cy - r * 0.02)
    p.close()
    c.drawPath(p, stroke=1, fill=1)

    # asas em forma de gota
    c.setFillColor(asa)
    c.setStrokeColor(cor_linha)
    c.setLineWidth(lw * 0.7)
    for s in (-1, 1):
        p = c.beginPath()
        p.moveTo(cx + s * r * 0.76, cy + r * 0.12)
        p.curveTo(cx + s * r * 0.98, cy - r * 0.35, cx + s * r * 0.72, cy - r * 0.78,
                  cx + s * r * 0.46, cy - r * 0.60)
        p.curveTo(cx + s * r * 0.50, cy - r * 0.35, cx + s * r * 0.60, cy - r * 0.10,
                  cx + s * r * 0.76, cy + r * 0.12)
        p.close()
        c.drawPath(p, stroke=1, fill=1)

    # pezinhos
    c.setFillColor(bico)
    for s in (-1, 1):
        c.circle(cx + s * r * 0.28, cy - r * 0.92, r * 0.10, stroke=0, fill=1)
    c.restoreState()


def estrelinha_fofa(c, cx, cy, r, fill=AMBER):
    estrela(c, cx, cy, r, fill)


# ---------------------------------------------------------------- marcadores
def chip(c, x, y, txt, cor=TEAL, fundo=TEAL_L, size=8.5, pad_x=6, h=13, icone=None):
    w = largura(txt, size, FONT_B) + pad_x * 2
    rrect(c, x, y, w, h, h / 2, fundo, None)
    texto(c, x + w / 2, y + h / 2 - size * 0.34, txt, size, FONT_B, cor, "c")
    return w


def numero_passo(c, cx, cy, n, r=8, cor=WHITE, fundo=TEAL, size=10):
    c.setFillColor(fundo)
    c.circle(cx, cy, r, stroke=0, fill=1)
    texto(c, cx, cy - size * 0.34, str(n), size, FONT_B, cor, "c")


def tesoura(c, x, y, tam=8, cor=SOFT):
    c.saveState()
    c.setStrokeColor(cor)
    c.setLineWidth(1)
    c.circle(x - tam * 0.28, y - tam * 0.35, tam * 0.18, stroke=1, fill=0)
    c.circle(x - tam * 0.28, y + tam * 0.35, tam * 0.18, stroke=1, fill=0)
    c.line(x - tam * 0.12, y - tam * 0.28, x + tam * 0.55, y + tam * 0.22)
    c.line(x - tam * 0.12, y + tam * 0.28, x + tam * 0.55, y - tam * 0.22)
    c.restoreState()


def marcas_de_corte(c, cor="#C9CDD4"):
    """Cruzinhas nos quatro cantos da margem: guia para a tesoura."""
    for (x, y) in ((M, M), (W - M, M), (M, H - M), (W - M, H - M)):
        c.saveState()
        c.setStrokeColor(HexColor(cor))
        c.setLineWidth(0.6)
        c.line(x - 4, y, x + 4, y)
        c.line(x, y - 4, x, y + 4)
        c.restoreState()


def linha_de_corte(c, x1, y1, x2, y2):
    linha(c, x1, y1, x2, y2, HexColor("#B9C0C9"), 0.8, dash=[4, 4])
    tesoura(c, (x1 + x2) / 2 - 4, (y1 + y2) / 2 + 5, 9, HexColor("#9AA3AF"))


def novo_canvas(nome):
    os.makedirs(PDF, exist_ok=True)
    return rl_canvas.Canvas(os.path.join(PDF, nome), pagesize=A4,
                            pageCompression=1)


def metadados(c, titulo, assunto, autor="Material de apoio à alfabetização"):
    c.setTitle(titulo)
    c.setSubject(assunto)
    c.setAuthor(autor)
    c.setCreator("Gerado com ReportLab + fonte Andika (SIL OFL)")
