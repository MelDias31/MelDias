# -*- coding: utf-8 -*-
"""Páginas de sílabas: famílias silábicas, sílabas complexas e leitura guiada."""
from reportlab.lib.units import mm

from base import *
from letras import desenhar_letra
from contornos import desenhar_texto, medir
from figuras import emoji, emoji_quadro, checkbox
from conteudo import FAMILIAS, COMPLEXAS, NIVEIS_PALAVRAS

NOME_FAMILIA = {
    "B": "BA BE BI BO BU", "C": "CA CO CU", "D": "DA DE DI DO DU",
    "F": "FA FE FI FO FU", "G": "GA GO GU", "L": "LA LE LI LO LU",
    "M": "MA ME MI MO MU", "N": "NA NE NI NO NU", "P": "PA PE PI PO PU",
    "R": "RA RE RI RO RU", "S": "SA SE SI SO SU", "T": "TA TE TI TO TU",
    "V": "VA VE VI VO VU", "J": "JA JE JI JO JU", "Z": "ZA ZE ZI ZO ZU",
}


def palavra_com_destaque(c, palavra, destaque, x, y, size, cor_dest, cor_resto=INK,
                         espaco=0.8):
    """Escreve a palavra com o pedaço 'destaque' em cor diferente."""
    i = palavra.find(destaque)
    if i < 0:
        return desenhar_texto(c, palavra, x, y, size, "solido", INK,
                              espaco_extra=espaco, nome_fonte="Andika-Bold.ttf")
    px = x
    for pedaco, cor in ((palavra[:i], cor_resto), (destaque, cor_dest),
                        (palavra[i + len(destaque):], cor_resto)):
        if pedaco:
            px += desenhar_texto(c, pedaco, px, y, size, "solido", cor,
                                 espaco_extra=espaco, nome_fonte="Andika-Bold.ttf")
    return px - x


def familia(c, pag, total, item):
    letra, silabas, palavras = item
    idx = ["B", "C", "D", "F", "G", "J", "L", "M", "N", "P", "R", "S", "T",
           "V", "Z"].index(letra) % 7
    cor, cor_l = PALETA[idx], PALETA_L[idx]
    fundo(c)
    lista = silabas.split()
    if len(lista) < 5:
        sub = (f"{', '.join(lista[:-1])} e {lista[-1]} — "
               "com as outras vogais o som muda")
    else:
        sub = f"Junte a letra {letra} com as vogais"
    topo = faixa_titulo(c, f"FAMÍLIA DO {letra}", sub, cor, cor_l,
                        etiqueta="sílabas")
    larg_total = W - 2 * M

    # ---- sílabas grandes
    n = len(lista)
    y_sil = topo - 6 * mm
    alt_s = 34 * mm
    cw = larg_total / n
    for i, s in enumerate(lista):
        cx = M + i * cw
        rrect(c, cx + 1.5 * mm, y_sil - alt_s, cw - 3 * mm, alt_s, 9, WHITE, cor, 1.5)
        tam = 34
        desenhar_texto(c, s, cx + cw / 2 - medir(s, tam, "Andika-Bold.ttf") / 2,
                       y_sil - 14 * mm, tam, "solido", cor, nome_fonte="Andika-Bold.ttf")
        desenhar_texto(c, s, cx + cw / 2 - medir(s, 20) / 2, y_sil - 27 * mm, 20,
                       "guia", SOFT)

    # ---- palavras com figura
    y_base = y_sil - alt_s - 6 * mm
    cols = 2
    bh = 30 * mm
    for i, (pal, fig, sil) in enumerate(palavras):
        col, row = i % cols, i // cols
        x = M + col * (larg_total / 2) + 1 * mm
        y = y_base - row * (bh + 4 * mm) - bh
        rrect(c, x, y, larg_total / 2 - 3 * mm, bh, 10, cor_l if i % 2 == 0 else WHITE,
              None if i % 2 == 0 else cor)
        emoji(c, fig, x + 13 * mm, y + bh / 2 + 2 * mm, 19 * mm, cor)
        palavra_com_destaque(c, pal, sil, x + 26 * mm, y + bh / 2 - 1 * mm,
                             25 if len(pal) <= 6 else 18, cor)
        texto(c, x + 26 * mm, y + 4 * mm, f"{sil.lower()} de {pal.lower()}", 8,
              FONT, SOFT)

    # ---- linha de treino
    y_tr = y_base - 2 * (bh + 4 * mm) - 4 * mm
    y_box = M + 4 * mm
    bh_tr = y_tr - y_box
    rrect(c, M, y_box, larg_total, bh_tr, 10, WHITE, LINE, 1)
    texto(c, M + 5 * mm, y_box + bh_tr - 7 * mm, "CUBRA E ESCREVA", 9, FONT_B, cor)
    n_linhas = 5
    passo = (bh_tr - 14 * mm) / n_linhas
    alt_l = min(12 * mm, passo - 3 * mm)
    for k in range(n_linhas):
        yy = y_box + bh_tr - 12 * mm - k * passo
        pauta(c, M + 6 * mm, yy - alt_l, larg_total - 12 * mm, alt_l,
              HexColor("#DCE2E9"))
        xx = M + 8 * mm
        j = 0
        while xx < W - M - 18 * mm:
            s = lista[j % n]
            desenhar_texto(c, s, xx, yy - alt_l, alt_l,
                           "guia" if k < n_linhas - 1 else "pontilhado", SOFT)
            xx += medir(s, alt_l) + 7 * mm
            j += 1

    rodape(c, pag, total)


def _pedaco_destaque(palavra, titulo):
    for cand in (titulo.split("/")[0].strip(), titulo.split("/")[-1].strip()):
        for ped in cand.split():
            if ped and ped in palavra:
                return ped
    return palavra[:2]


def complexas(c, pag, total, item):
    titulo, silabas, palavras = item
    cor, cor_l = PURPLE, PURPLE_L
    fundo(c)
    topo = faixa_titulo(c, titulo, "Sílabas que precisam de atenção",
                        cor, cor_l, etiqueta="sílabas especiais")
    larg_total = W - 2 * M

    # faixa de sílabas (um grupo por linha; QU/GU vira duas linhas)
    grupos = [g.split() for g in silabas.split("/") if g.split()]
    if not grupos:
        grupos = [[]]
    grupos = [g[:5] for g in grupos[:2]]
    lista = grupos[0]
    duas = len(grupos) > 1
    alt_s = 19 * mm if duas else 26 * mm
    gap_s = 4 * mm
    y_sil = topo - 6 * mm
    for gi, grupo in enumerate(grupos):
        n = max(1, len(grupo))
        cw = larg_total / n
        topo_lin = y_sil - gi * (alt_s + gap_s)
        for i, s in enumerate(grupo):
            cx = M + i * cw
            rrect(c, cx + 1 * mm, topo_lin - alt_s, cw - 2 * mm, alt_s, 8,
                  WHITE, cor, 1.3)
            tam = (24 if len(s) <= 3 else 18) if duas else (26 if len(s) <= 3 else 20)
            desenhar_texto(c, s, cx + cw / 2 - medir(s, tam, "Andika-Bold.ttf") / 2,
                           topo_lin - (8.5 * mm if duas else 12.5 * mm), tam,
                           "solido", cor, nome_fonte="Andika-Bold.ttf")
            tam_g = 15 if duas else 20
            desenhar_texto(c, s, cx + cw / 2 - medir(s, tam_g) / 2,
                           topo_lin - (16 * mm if duas else 20.5 * mm), tam_g,
                           "guia", SOFT)

    # cartões de palavras
    y = (y_sil - len(grupos) * alt_s - (len(grupos) - 1) * gap_s - 6 * mm)
    bh = 33 * mm
    for i, (pal, fig) in enumerate(palavras):
        col, row = i % 2, i // 2
        x = M + col * (larg_total / 2) + 1 * mm
        yy = y - row * (bh + 4 * mm) - bh
        rrect(c, x, yy, larg_total / 2 - 3 * mm, bh, 10,
              cor_l if i % 2 == 0 else WHITE, None if i % 2 == 0 else cor)
        emoji(c, fig, x + 14 * mm, yy + bh / 2, 21 * mm, cor)
        dest = _pedaco_destaque(pal, titulo)
        tam = 24 if len(pal) <= 6 else (19 if len(pal) <= 8 else 15)
        px = palavra_com_destaque(c, pal, dest, x + 28 * mm, yy + bh - 13 * mm, tam, cor)
        desenhar_texto(c, pal, x + 28 * mm, yy + 8 * mm, 11, "guia", SOFT)

    # treino
    y_tr = y - 2 * (bh + 4 * mm) - 2 * mm
    y_box = M + 22 * mm
    rrect(c, M, y_box, larg_total, y_tr - y_box, 10, WHITE, LINE, 1)
    texto(c, M + 5 * mm, y_tr - 7 * mm, "CUBRA E ESCREVA", 9, FONT_B, cor)
    altura_disp = y_tr - 12 * mm - y_box
    n_lin = max(3, min(7, int(altura_disp / (14 * mm))))
    passo = altura_disp / n_lin
    for k in range(n_lin):
        yy = y_tr - 12 * mm - k * passo
        pauta(c, M + 6 * mm, yy - 11 * mm, larg_total - 12 * mm, 11 * mm,
              HexColor("#DCE2E9"))
        grupo = grupos[k % len(grupos)]
        n = max(1, len(grupo))
        xx = M + 8 * mm
        j = 0
        while xx < W - M - 22 * mm:
            s = grupo[j % n]
            desenhar_texto(c, s, xx, yy - 11 * mm, 11 * mm,
                           "guia" if k < n_lin - 2 else "pontilhado", SOFT)
            xx += medir(s, 11 * mm) + 8 * mm
            j += 1

    # dica final
    rrect(c, M, M + 3 * mm, larg_total, 16 * mm, 8, AMBER_L, None)
    texto(c, M + 5 * mm, M + 13 * mm, "DICA:", 9, FONT_B, AMBER)
    paragrafo(c, M + 19 * mm, M + 13 * mm, larg_total - 24 * mm,
              "Leia as sílabas devagar, apontando com o dedo. Depois leia as palavras "
              "duas vezes: uma soletrando e outra de uma vez só.", 8.4, FONT, INK)
    rodape(c, pag, total)


def niveis(c, pag, total):
    """Leitura em escada: palavras curtas -> longas."""
    fundo(c)
    topo = faixa_titulo(c, "ESCADA DAS PALAVRAS",
                        "Comece pelas curtinhas. Só passe para a próxima quando estiver fácil.",
                        BLUE, BLUE_L, etiqueta="leitura")
    larg_total = W - 2 * M
    y = topo - 5 * mm
    alturas = [56, 66, 70]
    for i, (titulo, palavras) in enumerate(NIVEIS_PALAVRAS):
        alt = alturas[i] * mm
        rrect(c, M, y - alt, larg_total, alt, 10, WHITE, LINE, 1)
        c.setFillColor(BLUE)
        c.roundRect(M, y - alt, 4, alt, 2, stroke=0, fill=1)
        texto(c, M + 7 * mm, y - 8 * mm, titulo.upper(), 10, FONT_B, BLUE)
        n = len(palavras)
        cw = (larg_total - 12 * mm) / n
        for j, (pal, fig) in enumerate(palavras):
            cx = M + 6 * mm + j * cw
            emoji(c, fig, cx + cw / 2, y - 24 * mm, 17 * mm, BLUE)
            size = 12 if len(pal) <= 7 else 10
            desenhar_texto(c, pal, cx + cw / 2 - medir(pal, size, "Andika-Bold.ttf") / 2,
                           y - 41 * mm, size, "solido", INK, nome_fonte="Andika-Bold.ttf")
            # quadradinho: já leu?
            checkbox(c, cx + cw / 2 - 3.2 * mm, y - alt + 7 * mm, 6.4 * mm, LINE, 1)
            texto(c, cx + cw / 2, y - alt + 3.6 * mm, "já leu", 8, FONT, SOFT, "c")
        y -= alt + 5 * mm
    rodape(c, pag, total)


# ------------------------------------------------------------------ extras
def capa(c, pag, total):
    fundo(c, CREAM)
    c.setFillColor(BLUE)
    c.rect(0, H - 96 * mm, W, 96 * mm, stroke=0, fill=1)
    texto(c, W / 2, H - 34 * mm, "SÍLABAS E PALAVRAS", 30, FONT_B, WHITE, "c")
    texto(c, W / 2, H - 44 * mm, "juntar letras para formar sons", 12, FONT, BLUE_L, "c")
    # amostras
    for i, s in enumerate(["BA", "BE", "BI", "BO", "BU"]):
        cx = W / 2 + (i - 2) * 30 * mm
        c.setFillColor(WHITE)
        c.roundRect(cx - 12 * mm, H - 74 * mm, 24 * mm, 20 * mm, 6, stroke=0, fill=1)
        texto(c, cx, H - 68 * mm, s, 20, FONT_B, BLUE, "c")

    y = H - 112 * mm
    texto(c, W / 2, y, "Como usar", 14, FONT_B, INK, "c")
    paragrafo(c, M + 14 * mm, y - 10 * mm, W - 2 * M - 28 * mm,
              "Cada folha de família silábica trabalha uma consoante com as cinco vogais. "
              "Leia a sílaba, aponte a figura, leia a palavra e só depois treine a escrita. "
              "As sílabas especiais (CH, LH, NH, RR, SS, ÃO) vêm por último — são as mais difíceis.",
              10, FONT, SOFT, align="c")
    dicas = [
        "Escolha o momento: criança descansada, barriga cheia, sem tela por perto.",
        "De 5 a 10 minutos bastam. Pare no meio, com vontade de voltar amanhã.",
        "Uma família por dia — ou uma por semana, se estiver difícil.",
        "Repita a mesma folha em dias diferentes antes de ir para a próxima.",
    ]
    box_h = 12 * mm + len(dicas) * 6.4 * mm + 6 * mm
    box_y = M + 13 * mm
    box_topo = box_y + box_h

    y2 = y - 32 * mm
    passo = (y2 - (box_topo + 8 * mm)) / 3
    for i, (fig, txt) in enumerate([
            ("👂", "Primeiro ouça: diga a sílaba e peça para ela repetir."),
            ("👀", "Depois veja: mostre a sílaba escrita na folha."),
            ("✍️", "Por último escreva: cubra o tracejado com o dedo, depois com o lápis.")]):
        yy = y2 - i * passo
        rrect(c, M + 10 * mm, yy - 15 * mm, W - 2 * M - 20 * mm, 17 * mm, 7,
              WHITE, HexColor("#E3E7EC"), 1)
        emoji(c, fig, M + 20 * mm, yy - 6.5 * mm, 10 * mm, BLUE)
        texto(c, M + 30 * mm, yy - 7.5 * mm, txt, 9.5, FONT, INK)

    rrect(c, M + 10 * mm, box_y, W - 2 * M - 20 * mm, box_h, 9, AMBER_L, None)
    texto(c, M + 18 * mm, box_topo - 8.5 * mm, "PARA DAR CERTO NO DIA A DIA",
          9, FONT_B, AMBER)
    for i, t in enumerate(dicas):
        texto(c, M + 18 * mm, box_topo - 16 * mm - i * 6.4 * mm, "•  " + t, 8.6,
              FONT, INK)
    rodape(c, pag, total)


def niveis2(c, pag, total):
    """Continuação: palavras longas + sílabas para ler rápido."""
    fundo(c)
    topo = faixa_titulo(c, "PALAVRAS MAIORES", "Quando as curtas já estão fáceis.",
                        BLUE, BLUE_L, etiqueta="leitura")
    larg = W - 2 * M
    y = topo - 8 * mm
    palavras = [("BORBOLETA", "🦋"), ("TARTARUGA", "🐢"), ("JACARÉ", "🐊"),
                ("ELEFANTE", "🐘"), ("GELADEIRA", "🧊"), ("BICICLETA", "🚲"),
                ("CHOCOLATE", "🍫"), ("DINOSSAURO", "🦕"), ("ABACAXI", "🍍"),
                ("FORMIGA", "🐜"), ("JANELA", "🪟"), ("SAPATO", "👟")]
    cols, rows = 2, 6
    cw = (larg - 4 * mm) / cols
    ch = (y - (M + 26 * mm)) / rows
    for i, (pal, fig) in enumerate(palavras):
        col, row = i % cols, i // cols
        x = M + col * (cw + 4 * mm)
        yy = y - (row + 1) * ch
        cor, cor_l = PALETA[i % 7], PALETA_L[i % 7]
        rrect(c, x, yy + 1 * mm, cw, ch - 3 * mm, 8, cor_l, None)
        emoji(c, fig, x + 11 * mm, yy + ch / 2, 12 * mm, cor)
        tam = 17 if len(pal) <= 8 else 14
        desenhar_texto(c, pal, x + 20 * mm, yy + ch / 2 + 1, tam, "solido", INK,
                       nome_fonte="Andika-Bold.ttf")
        # dividir em sílabas
        from p_leitura import _dividir_silabas
        sil = " - ".join(_dividir_silabas(pal))
        texto(c, x + 20 * mm, yy + ch / 2 - 6 * mm, sil.lower(), 7.6, FONT, SOFT)

    yb = M + 20 * mm
    rrect(c, M, M + 4 * mm, larg, yb - M - 4 * mm, 10, AMBER_L, None)
    texto(c, M + 5 * mm, yb - 6 * mm, "DICA", 8.5, FONT_B, AMBER)
    paragrafo(c, M + 18 * mm, yb - 6 * mm, larg - 24 * mm,
              "Leia primeiro batendo palma em cada sílaba. Depois leia sem bater. "
              "Se travar, volte para a família silábica daquela consoante.", 8.5, FONT, INK)
    rodape(c, pag, total)


def treino_leitura(c, pag, total):
    """Cartões de leitura rápida (fluência)."""
    fundo(c)
    topo = faixa_titulo(c, "LEITURA RÁPIDA",
                        "Leia a coluna de cima para baixo. Marque o tempo e tente melhorar.",
                        TEAL, TEAL_L, etiqueta="fluência")
    larg = W - 2 * M
    colunas = [
        ["BA", "BE", "BI", "BO", "BU", "BÃO"],
        ["CA", "CO", "CU", "CHA", "CHE", "CHI"],
        ["DA", "DE", "DI", "DO", "DU", "DÃO"],
        ["LA", "LE", "LI", "LO", "LU", "LÃO"],
        ["MA", "ME", "MI", "MO", "MU", "MÃO"],
    ]
    cw = larg / len(colunas)
    y = topo - 8 * mm
    hh = 76 * mm
    for i, col in enumerate(colunas):
        x = M + i * cw
        rrect(c, x + 1 * mm, y - hh, cw - 2 * mm, hh, 6, WHITE, HexColor("#DDE3EA"), 1)
        for j, s in enumerate(col):
            cy = y - 12 * mm - j * 11 * mm
            texto(c, x + cw / 2, cy, s, 16, FONT_B, INK, "c")
            linha(c, x + 4 * mm, cy + 5 * mm, x + cw - 4 * mm, cy + 5 * mm,
                  HexColor("#EDF1F5"), 0.7)
        checkbox(c, x + cw / 2 - 3 * mm, y - hh + 3 * mm, 6 * mm, HexColor("#B9C0C9"), 1)
        texto(c, x + cw / 2, y - hh - 5 * mm, "feito", 6.5, FONT, SOFT, "c")

    # cronômetro
    y2 = y - hh - 12 * mm
    rrect(c, M, M + 4 * mm, larg, y2 - M - 4 * mm, 10, HexColor("#F7F9FB"), LINE, 1)
    texto(c, M + 6 * mm, y2 - 9 * mm, "MEU TEMPO", 9, FONT_B, TEAL)
    for k in range(3):
        x = M + 6 * mm + k * 60 * mm
        texto(c, x, y2 - 18 * mm, ["1ª vez:", "2ª vez:", "3ª vez:"][k], 8.5, FONT, INK)
        linha(c, x + 16 * mm, y2 - 19 * mm, x + 46 * mm, y2 - 19 * mm,
              HexColor("#B9C0C9"), 0.9)
        texto(c, x + 47 * mm, y2 - 18 * mm, "seg", 7.5, FONT, SOFT)
    paragrafo(c, M + 6 * mm, y2 - 28 * mm, larg - 12 * mm,
              "A meta não é ser rápido: é ler sem parar para adivinhar. Se errar, "
              "volte uma linha e leia de novo. Repetir 3 vezes na mesma sessão já "
              "melhora o reconhecimento automático.", 8.4, FONT, SOFT)

    # anotações do adulto
    linha(c, M + 6 * mm, y2 - 44 * mm, W - M - 6 * mm, y2 - 44 * mm,
          HexColor("#DCE3EA"), 0.8)
    texto(c, M + 6 * mm, y2 - 52 * mm, "O QUE FOI DIFÍCIL HOJE", 9, FONT_B, TEAL)
    texto(c, M + 6 * mm, y2 - 58 * mm,
          "Anote a sílaba ou a palavra que travou: ela volta amanhã.", 8, FONT, SOFT)
    for k in range(6):
        yy = y2 - 70 * mm - k * 12 * mm
        linha(c, M + 6 * mm, yy, W - M - 6 * mm, yy, HexColor("#D3DAE2"), 1)
    rodape(c, pag, total)
