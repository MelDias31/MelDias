# -*- coding: utf-8 -*-
"""Jogos imprimíveis: memória, bingo, trilha, ligue-ligue, caça-palavras, dominó."""
import random
from reportlab.lib.units import mm

from base import *
from contornos import desenhar_texto, medir
from figuras import emoji, checkbox, bolinhas_progresso
from conteudo import MEMORIA, BINGO_POOL, LIGUE, CACA, TRILHA, DOMINO


def _marcas_de_corte(c):
    """Cantinhos de corte discretos em todas as páginas de jogos."""
    for (x, y) in ((M, M), (W - M, M), (M, H - M), (W - M, H - M)):
        c.saveState()
        c.setStrokeColor(HexColor("#C9CDD4"))
        c.setLineWidth(0.6)
        c.line(x - 4, y, x + 4, y)
        c.line(x, y - 4, x, y + 4)
        c.restoreState()


def _tabuleiro(c, x, y, w, h, cols, rows, desenhar, gap=3):
    cw = (w - gap * (cols - 1)) / cols
    ch = (h - gap * (rows - 1)) / rows
    for i in range(cols * rows):
        col, row = i % cols, i // cols
        cx = x + col * (cw + gap)
        cy = y + h - (row + 1) * ch - row * gap
        desenhar(i, cx, cy, cw, ch)
    return cw, ch


def memoria(c, pag, total, metade=0):
    """Cartas 6x4 (24 cartas = 12 pares) por folha; metade 0 e 1."""
    fundo(c)
    pares = MEMORIA[metade * 6:(metade + 1) * 6]
    rnd = random.Random(7 + metade)
    cartas = []
    for pal, fig in pares:
        cartas += [("fig", fig, pal), ("pal", fig, pal)]
    rnd.shuffle(cartas)

    topo = H - M - 24 * mm
    texto(c, W / 2, H - M - 6 * mm, "JOGO DA MEMÓRIA", 16, FONT_B, TEAL, "c")
    texto(c, W / 2, H - M - 12 * mm,
          "Recorte as cartas. Vire de costas e encontre os pares: figura + palavra.",
          9.5, FONT, SOFT, "c")
    texto(c, W / 2, H - M - 17 * mm, "PARA PODER JOGAR DE NOVO, COLE NO CARTOLINA ANTES DE RECORTAR.",
          8, FONT_B, AMBER, "c")

    x0, y0 = M, topo
    larg, alt = W - 2 * M, topo - M
    cols, rows = 4, 3
    gap = 5

    def desenhar(i, x, y, w, h):
        pal, fig, tipo = cartas[i][2], cartas[i][1], cartas[i][0]
        cor = PALETA[i % 7]
        rrect(c, x, y, w, h, 8, WHITE, cor, 1.4)
        if tipo == "fig":
            emoji(c, fig, x + w / 2, y + h / 2 + 3, min(w, h) * 0.60, cor)
        else:
            tam = 15
            while medir(pal, tam, "Andika-Bold.ttf") > w - 8 and tam > 7:
                tam -= 0.5
            desenhar_texto(c, pal, x + w / 2 - medir(pal, tam, "Andika-Bold.ttf") / 2,
                           y + h / 2 - 4, tam, "solido", INK, nome_fonte="Andika-Bold.ttf")

    _tabuleiro(c, x0, M, larg, alt, cols, rows, desenhar, gap)
    _marcas_de_corte(c)
    rodape(c, pag, total, "Jogo da memória • recorte e brinque")


def bingo(c, pag, total):
    """6 cartelas de bingo de sílabas/palavras."""
    fundo(c)
    texto(c, W / 2, H - M - 6 * mm, "BINGO DE PALAVRAS", 16, FONT_B, PURPLE, "c")
    texto(c, W / 2, H - M - 12 * mm,
          "Recorte as 6 cartelas. Quem canta sorteia as figuras (página ao lado).",
          9.5, FONT, SOFT, "c")
    rnd = random.Random(21)
    x0, y0 = M, H - M - 20 * mm
    larg, alt = W - 2 * M, y0 - M
    cols, rows = 2, 3
    cw = (larg - 8 * mm) / cols
    ch = (alt - 8 * mm) / rows

    for k in range(6):
        col, row = k % cols, k // cols
        x = x0 + col * (cw + 8 * mm)
        y = y0 - (row + 1) * ch - row * 8 * mm
        rrect(c, x, y, cw, ch, 8, WHITE, PURPLE, 1.3)
        texto(c, x + cw / 2, y + ch - 6 * mm, f"CARTELA {k + 1}", 8.5, FONT_B, PURPLE, "c")
        pool = MEMORIA[:]
        rnd.shuffle(pool)
        escolhas = pool[:9]
        cw2 = (cw - 6 * mm) / 3
        ch2 = (ch - 12 * mm) / 3
        for i in range(9):
            cc, rr = i % 3, i // 3
            bx = x + 3 * mm + cc * cw2
            by = y + 3 * mm + (2 - rr) * ch2
            pal = escolhas[i][0]
            if i == 4:
                texto(c, bx + cw2 / 2, by + ch2 / 2 - 3, "★", 14, FONT, AMBER, "c")
                continue
            rrect(c, bx + 0.6 * mm, by + 0.6 * mm, cw2 - 1.2 * mm, ch2 - 1.2 * mm,
                  4, None, HexColor("#C9CDD4"), 0.8)
            tam = 11 if len(pal) <= 5 else 8.5
            desenhar_texto(c, pal, bx + cw2 / 2 - medir(pal, tam, "Andika-Bold.ttf") / 2,
                           by + ch2 / 2 - 3.5, tam, "solido", INK,
                           nome_fonte="Andika-Bold.ttf")
    rodape(c, pag, total, "Bingo de palavras • 6 cartelas")


def bingo_fichas(c, pag, total):
    """Fichas para recortar (sorteio do bingo)."""
    fundo(c)
    texto(c, W / 2, H - M - 6 * mm, "FICHAS DO BINGO", 16, FONT_B, PURPLE, "c")
    texto(c, W / 2, H - M - 12 * mm,
          "Recorte, dobre e coloque num saquinho. Sorteie uma por vez e mostre a figura.",
          9.5, FONT, SOFT, "c")
    itens = MEMORIA + BINGO_POOL
    itens = list(dict((p, f) for p, f in itens).items())
    cols = 4
    x0, y0 = M, H - M - 20 * mm
    larg = W - 2 * M
    cw = larg / cols
    ch = 20 * mm
    for i, (pal, fig) in enumerate(itens):
        col, row = i % cols, i // cols
        x = x0 + col * cw
        y = y0 - (row + 1) * ch
        if y < M:
            break
        rrect(c, x + 1 * mm, y + 1 * mm, cw - 2 * mm, ch - 2 * mm, 6, WHITE,
              HexColor("#D3D9E1"), 0.9)
        emoji(c, fig, x + 9 * mm, y + ch / 2, 11 * mm, PURPLE)
        tam = 11 if len(pal) <= 6 else 9
        desenhar_texto(c, pal, x + 17 * mm, y + ch / 2 - 4, tam, "solido", INK,
                       nome_fonte="Andika-Bold.ttf")
    rodape(c, pag, total, "Fichas do bingo • recorte")


def _trilha_tab(c, x, y, w, h):
    n = len(TRILHA)
    cols = 5
    rows = (n + cols - 1) // cols
    gap = 2.5 * mm
    cw = (w - gap * (cols - 1)) / cols
    ch = (h - gap * (rows - 1)) / rows
    for i, (conteudo, tipo) in enumerate(TRILHA):
        col, row = i % cols, i // cols
        if row % 2 == 1:
            col = cols - 1 - col
        cx = x + col * (cw + gap)
        cy = y + h - (row + 1) * ch - row * gap
        centro_x, centro_y = cx + cw / 2, cy + ch / 2
        if tipo == 0:
            rrect(c, cx, cy, cw, ch, 6, WHITE, HexColor("#C9CDD4"), 1.1)
            tam = 17
            desenhar_texto(c, conteudo, centro_x - medir(conteudo, tam, "Andika-Bold.ttf") / 2,
                           centro_y - 6, tam, "solido", INK, nome_fonte="Andika-Bold.ttf")
        elif tipo == 1:      # dado: jogue de novo
            rrect(c, cx, cy, cw, ch, 6, AMBER_L, AMBER, 1.2)
            lado = min(cw, ch) * 0.46
            rrect(c, centro_x - lado / 2, centro_y - lado / 2, lado, lado, 3, WHITE, AMBER, 1.3)
            for dx, dy in ((-0.24, 0.24), (0, 0), (0.24, -0.24)):
                c.setFillColor(AMBER)
                c.circle(centro_x + dx * lado, centro_y + dy * lado, lado * 0.075,
                         stroke=0, fill=1)
        elif tipo == 2:      # estrela: avance
            rrect(c, cx, cy, cw, ch, 6, GREEN_L, GREEN, 1.2)
            estrela(c, centro_x, centro_y + 1, min(cw, ch) * 0.26, GREEN)
        else:                # seta de volta
            rrect(c, cx, cy, cw, ch, 6, CORAL_L, CORAL, 1.2)
            r = min(cw, ch) * 0.24
            c.setStrokeColor(CORAL)
            c.setLineWidth(2.4)
            c.setLineCap(1)
            p = c.beginPath()
            p.moveTo(centro_x + r * 0.75, centro_y + r * 0.15)
            p.curveTo(centro_x + r * 0.75, centro_y + r, centro_x - r * 0.5,
                      centro_y + r, centro_x - r * 0.75, centro_y + r * 0.05)
            c.drawPath(p)
            # ponta da seta
            c.setFillColor(CORAL)
            pp = c.beginPath()
            pp.moveTo(centro_x - r * 0.78, centro_y - r * 0.55)
            pp.lineTo(centro_x - r * 1.05, centro_y + r * 0.20)
            pp.lineTo(centro_x - r * 0.45, centro_y + r * 0.22)
            pp.close()
            c.drawPath(pp, fill=1, stroke=0)
        texto(c, cx + 1.8 * mm, cy + 1.2 * mm, str(i + 1), 6.5, FONT_B, SOFT)
    return cw, ch


def trilha(c, pag, total):
    fundo(c)
    topo = faixa_titulo(c, "TRILHA DA LEITURA",
                        "Jogue com um dado. Leia a sílaba da casa em voz alta.",
                        GREEN, GREEN_L, etiqueta="jogo")
    # painel de regras à direita
    larg = W - 2 * M
    y = topo - 6 * mm
    alt = 92 * mm
    rrect(c, M, y - alt, larg, alt, 10, WHITE, LINE, 1)
    _trilha_tab(c, M + 4 * mm, y - alt + 4 * mm, larg - 8 * mm, alt - 8 * mm)

    # legenda + regras
    y2 = y - alt - 8 * mm
    h_regras = 62 * mm
    rrect(c, M, y2 - h_regras, larg, h_regras, 10, HexColor("#F7F9FB"), LINE, 1)
    texto(c, M + 6 * mm, y2 - 8 * mm, "COMO JOGAR", 10, FONT_B, GREEN)
    regras = [
        "Cada jogador escolhe uma tampinha para andar na trilha.",
        "Jogue o dado e ande o número de casas.",
        "Leia a sílaba em voz alta. Se acertar, fica na casa; se errar, o adulto lê e a criança repete.",
        "Casa verde (estrela): avance 1 casa. Casa laranja (seta): volte 1 casa. Casa amarela (dado): jogue de novo.",
        "Ganham todos que chegam ao fim. Não precisa ter só um vencedor.",
    ]
    yy = y2 - 15 * mm
    for i, r in enumerate(regras):
        numero_passo(c, M + 9 * mm, yy + 2.2 * mm, i + 1, 4.4, WHITE, GREEN, 6.8)
        linhas = quebrar(r, larg - 24 * mm, 8.4, FONT)
        for j, ln in enumerate(linhas):
            texto(c, M + 14 * mm, yy - j * 4.0 * mm, ln, 8.4, FONT, INK)
        yy -= (len(linhas) * 4.0 + 2.4) * mm

    # dado e peões para recortar
    y_d = y2 - h_regras - 6 * mm
    if y_d > M + 42 * mm:
        _dado_e_peoes(c, M, M + 4 * mm, larg, y_d - M - 4 * mm)

    rodape(c, pag, total, "Trilha da leitura • use tampinhas, feijões ou os peões desta folha")


def _dado_e_peoes(c, x, y, w, h):
    rrect(c, x, y, w, h, 10, WHITE, LINE, 1)
    texto(c, x + 5 * mm, y + h - 7 * mm, "RECORTE AQUI: DADO E PEÕES", 8, FONT_B, GREEN)
    linha_de_corte(c, x + 4 * mm, y + 4 * mm, x + w - 4 * mm, y + 4 * mm)
    # dado (planificação 3x3 simplificada: 6 faces em cruz)
    lado = min(11 * mm, (h - 20 * mm) / 2)
    ox = x + 12 * mm
    oy = y + 10 * mm
    faces = [(0, 1, 1), (1, 0, 2), (1, 1, 6), (1, 2, 3), (2, 1, 4), (3, 1, 5)]
    pos = {1: [(0.5, 0.5)], 2: [(0.25, 0.75), (0.75, 0.25)],
           3: [(0.25, 0.75), (0.5, 0.5), (0.75, 0.25)],
           4: [(0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75)],
           5: [(0.25, 0.25), (0.75, 0.25), (0.5, 0.5), (0.25, 0.75), (0.75, 0.75)],
           6: [(0.25, 0.2), (0.75, 0.2), (0.25, 0.5), (0.75, 0.5), (0.25, 0.8), (0.75, 0.8)]}
    for cx, cy, n in faces:
        rrect(c, ox + cx * lado, oy + (3 - cy) * lado, lado, lado, 2, WHITE, INK, 1)
        for (px, py) in pos[n]:
            c.setFillColor(INK)
            c.circle(ox + cx * lado + px * lado, oy + (3 - cy) * lado + py * lado,
                     lado * 0.075, stroke=0, fill=1)
    # peões (círculos coloridos)
    px0 = x + 70 * mm
    labels = ["Jogador 1", "Jogador 2", "Jogador 3", "Jogador 4"]
    for i in range(4):
        cx = px0 + (i % 4) * 26 * mm
        cy = y + h - 24 * mm
        c.setFillColor(PALETA[i])
        c.circle(cx, cy, 8 * mm, stroke=0, fill=1)
        c.setFillColor(WHITE)
        c.circle(cx, cy, 4.5 * mm, stroke=0, fill=1)
        texto(c, cx, cy - 2.5, str(i + 1), 7, FONT_B, PALETA[i], "c")
        texto(c, cx, cy - 11 * mm, labels[i], 6.5, FONT, SOFT, "c")


def ligue(c, pag, total, item):
    fundo(c)
    topo = faixa_titulo(c, "LIGUE A FIGURA À PALAVRA",
                        "Passe o dedo (ou o lápis) de cada figura até a palavra certa.",
                        BLUE, BLUE_L, etiqueta="jogo")
    larg = W - 2 * M
    y = topo - 10 * mm
    alt = (y - (M + 34 * mm)) / len(item)
    # embaralha a coluna de palavras (semente fixa: mesmo PDF sempre igual)
    rnd = random.Random(sum(len(p) for p, _ in item) + 3)
    palavras = [p for p, _ in item]
    ordem = list(range(len(palavras)))
    while True:
        rnd.shuffle(ordem)
        if all(ordem[i] != i for i in range(len(palavras))):
            break

    # coluna de palavras à direita
    x_fig = M + 24 * mm
    x_pal = W - M - 34 * mm
    for i, (pal, fig) in enumerate(item):
        yy = y - i * alt - alt / 2
        # linha zebrada
        rrect(c, M, y - (i + 1) * alt + 1 * mm, larg, alt - 2 * mm, 8,
              WHITE if i % 2 == 0 else HexColor("#F5F8FA"), None)
        emoji(c, fig, x_fig, yy + 1 * mm, min(alt * 0.62, 15 * mm), BLUE)
        c.setFillColor(HexColor("#9AA3AF"))
        c.circle(x_fig + 12 * mm, yy, 1.7, stroke=0, fill=1)
        # palavra (ordem embaralhada)
        p_alvo = palavras[ordem[i]]
        c.setFillColor(HexColor("#9AA3AF"))
        c.circle(x_pal - 6 * mm, yy, 1.7, stroke=0, fill=1)
        tam = 16 if len(p_alvo) <= 6 else 13
        desenhar_texto(c, p_alvo, x_pal, yy - 5, tam, "solido", INK,
                       nome_fonte="Andika-Bold.ttf")

    # linhas-guia tracejadas para ligar
    for i in range(len(item)):
        yy = y - i * alt - alt / 2
        linha(c, x_fig + 12 * mm, yy, x_pal - 6 * mm, yy,
              HexColor("#EDF1F5"), 0.7, dash=[2, 6])

    yf = y - len(item) * alt - 6 * mm
    rrect(c, M, yf - 26 * mm, larg, 26 * mm, 10, AMBER_L, None)
    texto(c, M + 5 * mm, yf - 8 * mm, "VALE MAIS DE UMA TENTATIVA", 8.5, FONT_B, AMBER)
    paragrafo(c, M + 5 * mm, yf - 14 * mm, larg - 10 * mm,
              "Se ligar errado, apague e tente de novo. O erro mostra qual som ainda "
              "precisa ser treinado — não é motivo para parar a atividade.", 8.4, FONT, INK)
    rodape(c, pag, total, "Ligue a figura à palavra • jogo de pareamento")


def caca_palavras(c, pag, total, item):
    titulo, palavras, grade, dicas = item
    fundo(c)
    topo = faixa_titulo(c, "CAÇA-PALAVRAS", "Encontre as palavras escondidas. Elas estão na horizontal.",
                        CORAL, CORAL_L, etiqueta="jogo")
    larg = W - 2 * M
    # grade
    linhas, cols = len(grade), max(len(r) for r in grade)
    y0 = topo - 8 * mm
    gh = 78 * mm
    cw = (larg - 10 * mm) / cols
    ch = gh / linhas
    x0 = M + 5 * mm
    for i, row in enumerate(grade):
        for j, ch_ in enumerate(row):
            cx = x0 + j * cw
            cy = y0 - (i + 1) * ch
            rrect(c, cx + 0.4 * mm, cy + 0.4 * mm, cw - 0.8 * mm, ch - 0.8 * mm,
                  2, None, HexColor("#DCE2E9"), 0.6)
            texto(c, cx + cw / 2, cy + ch / 2 - 3.4, ch_, 11, FONT_B, INK, "c")
    # palavras + dicas
    yb = y0 - gh - 8 * mm
    texto(c, M, yb, "PALAVRAS PARA ENCONTRAR", 9, FONT_B, CORAL)
    yb -= 7 * mm
    cols_w = (larg) / 2
    for i, (pal, fig) in enumerate(dicas):
        col, row = i % 2, i // 2
        x = M + col * cols_w
        yy = yb - row * 12 * mm
        emoji(c, fig, x + 6 * mm, yy + 1 * mm, 10 * mm, CORAL)
        desenhar_texto(c, pal, x + 14 * mm, yy - 2, 12, "solido", INK,
                       nome_fonte="Andika-Bold.ttf")
        # caixinha de marcar
        checkbox(c, x + cols_w - 10 * mm, yy - 2, 5 * mm, HexColor("#B9C0C9"), 1)

    # linhas para escrever as palavras encontradas
    y_esc = M + 26 * mm
    texto(c, M, y_esc + 14 * mm, "ESCREVA AS PALAVRAS QUE ENCONTROU:", 8.5, FONT_B, SOFT)
    for k in range(3):
        linha(c, M, y_esc - k * 9 * mm, W - M, y_esc - k * 9 * mm,
              HexColor("#D3DAE2"), 1)
    rodape(c, pag, total, "Caça-palavras • palavras na horizontal")


def domino(c, pag, total):
    """Dominó de sílabas (peças grandes, 2 por linha)."""
    fundo(c)
    topo = faixa_titulo(c, "DOMINÓ DE SÍLABAS",
                        "Recorte as peças. Emende a sílaba igual ou que forme uma palavra.",
                        PURPLE, PURPLE_L, etiqueta="jogo")
    itens = DOMINO[:]
    rnd = random.Random(5)
    rnd.shuffle(itens)
    pecas = [(itens[i], itens[i + 1]) for i in range(0, len(itens) - 1, 2)][:24]
    larg = W - 2 * M
    cols = 3
    rows = 8
    y0 = topo - 6 * mm
    h = (y0 - M) / rows
    cw = larg / cols
    for i, (a, b) in enumerate(pecas):
        col, row = i % cols, i // cols
        x = M + col * cw + 1 * mm
        y = y0 - (row + 1) * h + 1 * mm
        rrect(c, x, y, cw - 2 * mm, h - 2 * mm, 5, WHITE, PURPLE, 1.1)
        c.setStrokeColor(HexColor("#C9CDD4"))
        c.setLineWidth(0.7)
        c.line(x + 1 * mm, y + (h - 2 * mm) / 2, x + cw - 3 * mm, y + (h - 2 * mm) / 2)
        desenhar_texto(c, a, x + cw / 2 - 2 * mm - medir(a, 13, "Andika-Bold.ttf") / 2,
                       y + h - 10 * mm, 13, "solido", INK, nome_fonte="Andika-Bold.ttf")
        desenhar_texto(c, b, x + cw / 2 - 2 * mm - medir(b, 13, "Andika-Bold.ttf") / 2,
                       y + 5 * mm, 13, "solido", PURPLE, nome_fonte="Andika-Bold.ttf")
    rodape(c, pag, total, "Dominó de sílabas • recorte")


# ------------------------------------------------------------------ extras
def capa_jogos(c, pag, total):
    fundo(c, CREAM)
    c.setFillColor(AMBER)
    c.rect(0, H - 92 * mm, W, 92 * mm, stroke=0, fill=1)
    texto(c, W / 2, H - 34 * mm, "JOGOS E FICHAS", 30, FONT_B, WHITE, "c")
    texto(c, W / 2, H - 44 * mm, "aprender brincando — e sem perceber", 12, FONT, WHITE, "c")
    for i, e in enumerate(["🎲", "🃏", "🔔", "🏁", "✂️"]):
        emoji(c, e, W / 2 + (i - 2) * 26 * mm, H - 70 * mm, 18 * mm, WHITE)

    y = H - 108 * mm
    itens = [
        ("🃏", "Jogo da memória", "figura + palavra (24 cartas)"),
        ("🔔", "Bingo de palavras", "6 cartelas + fichas"),
        ("🏁", "Trilha da leitura", "com dado e peões para recortar"),
        ("🔗", "Ligue a figura à palavra", "3 folhas"),
        ("🔍", "Caça-palavras", "3 níveis"),
        ("🁢", "Dominó de sílabas", "2 folhas de peças"),
        ("🅰️", "Forca de palavras", "para adivinhar letras"),
    ]
    dicas = [
        "Jogue junto e deixe ela ganhar algumas vezes: o jogo é para ler, não para vencer.",
        "Rodadas curtas. Se cansar, pare antes do erro — guarde com vontade de voltar.",
    ]
    box_h = 12 * mm + len(dicas) * 6.4 * mm + 5 * mm
    box_y = M + 13 * mm
    box_topo = box_y + box_h

    passo = (y - (box_topo + 19 * mm)) / 6
    for i, (fig, tit, sub) in enumerate(itens):
        yy = y - i * passo
        rrect(c, M + 8 * mm, yy - 13 * mm, W - 2 * M - 16 * mm, 15 * mm, 7,
              WHITE, HexColor("#E8E1D3"), 1)
        emoji(c, fig, M + 18 * mm, yy - 5.5 * mm, 9 * mm, AMBER)
        texto(c, M + 27 * mm, yy - 5 * mm, tit, 10, FONT_B, INK)
        texto(c, W - M - 14 * mm, yy - 5 * mm, sub, 8, FONT, SOFT, "r")

    rrect(c, M + 8 * mm, box_y, W - 2 * M - 16 * mm, box_h, 9, AMBER_L, None)
    texto(c, M + 16 * mm, box_topo - 8.5 * mm, "ANTES DE JOGAR", 8.5, FONT_B, AMBER)
    for i, t in enumerate(dicas):
        texto(c, M + 16 * mm, box_topo - 16.5 * mm - i * 6.6 * mm, "•  " + t, 8.6,
              FONT, INK)
    rodape(c, pag, total)


def trilha_fichas(c, pag, total):
    """Fichas de sílabas para sortear na trilha (opcional)."""
    fundo(c)
    texto(c, W / 2, H - M - 7 * mm, "FICHAS DA TRILHA", 15, FONT_B, GREEN, "c")
    texto(c, W / 2, H - M - 13 * mm,
          "Recorte e sorteie em vez de usar o dado — ou use para montar palavras.", 9,
          FONT, SOFT, "c")
    from conteudo import DOMINO
    larg = W - 2 * M
    cols = 6
    cw = larg / cols
    ch = 22 * mm
    y0 = H - M - 20 * mm
    for i, s in enumerate(DOMINO[:48]):
        col, row = i % cols, i // cols
        x = M + col * cw
        y = y0 - (row + 1) * ch
        if y < M:
            break
        rrect(c, x + 1 * mm, y + 1 * mm, cw - 2 * mm, ch - 2 * mm, 5, WHITE,
              HexColor("#C9D6C6"), 0.9)
        desenhar_texto(c, s, x + cw / 2 - medir(s, 13, "Andika-Bold.ttf") / 2,
                       y + ch / 2 - 4, 13, "solido", GREEN, nome_fonte="Andika-Bold.ttf")
    rodape(c, pag, total, "Fichas da trilha • recorte")


def caca_2(c, pag, total):
    """Caça-palavras nível 2 (sílabas e palavras com dígrafos)."""
    _caca_generico(c, pag, total,
                   "NÍVEL 2 — SÍLABAS E DÍGRAFOS",
                   [["C", "H", "U", "V", "A", "B", "O", "L"],
                    ["B", "A", "L", "A", "C", "H", "A", "V"],
                    ["M", "A", "L", "H", "A", "D", "A", "D"],
                    ["N", "I", "N", "H", "O", "G", "A", "T"],
                    ["F", "I", "L", "H", "O", "P", "A", "T"],
                    ["G", "A", "L", "H", "A", "S", "O", "L"],
                    ["C", "H", "A", "V", "E", "M", "E", "L"],
                    ["B", "A", "N", "H", "O", "V", "A", "C"]],
                   [("CHUVA", "🌧️"), ("MALHA", "🧶"), ("NINHO", "🪹"),
                    ("FILHO", "👦"), ("GALINHA", "🐔"), ("CHAVE", "🔑")])


def caca_3(c, pag, total):
    _caca_generico(c, pag, total,
                   "NÍVEL 3 — PALAVRAS MAIORES",
                   [["B", "O", "R", "B", "O", "L", "E", "T", "A"],
                    ["C", "A", "S", "A", "D", "O", "C", "E", "G"],
                    ["J", "A", "N", "E", "L", "A", "T", "O", "A"],
                    ["T", "A", "R", "T", "A", "R", "U", "G", "A"],
                    ["S", "A", "P", "A", "T", "O", "L", "U", "A"],
                    ["E", "L", "E", "F", "A", "N", "T", "E", "X"],
                    ["P", "I", "P", "O", "C", "A", "M", "E", "L"],
                    ["B", "A", "N", "A", "N", "A", "G", "A", "T"]],
                   [("BORBOLETA", "🦋"), ("JANELA", "🪟"), ("TARTARUGA", "🐢"),
                    ("SAPATO", "👟"), ("ELEFANTE", "🐘"), ("PIPOCA", "🍿")])


def _caca_generico(c, pag, total, titulo, grade, dicas):
    fundo(c)
    topo = faixa_titulo(c, "CAÇA-PALAVRAS", titulo, CORAL, CORAL_L, etiqueta="jogo")
    larg = W - 2 * M
    linhas, cols = len(grade), max(len(r) for r in grade)
    y0 = topo - 8 * mm
    gh = min(96 * mm, y0 - M - 34 * mm)
    cw = (larg - 10 * mm) / cols
    ch = gh / linhas
    x0 = M + 5 * mm
    for i, row in enumerate(grade):
        for j, ch_ in enumerate(row):
            cx = x0 + j * cw
            cy = y0 - (i + 1) * ch
            rrect(c, cx + 0.4 * mm, cy + 0.4 * mm, cw - 0.8 * mm, ch - 0.8 * mm,
                  2, None, HexColor("#DCE2E9"), 0.6)
            texto(c, cx + cw / 2, cy + ch / 2 - 3.4, ch_, 11, FONT_B, INK, "c")
    yb = y0 - gh - 10 * mm
    texto(c, M, yb, "PALAVRAS PARA ENCONTRAR", 9, FONT_B, CORAL)
    yb -= 8 * mm
    cols_w = larg / 2
    for i, (pal, fig) in enumerate(dicas):
        col, row = i % 2, i // 2
        x = M + col * cols_w
        yy = yb - row * 11 * mm
        emoji(c, fig, x + 6 * mm, yy + 1 * mm, 9 * mm, CORAL)
        desenhar_texto(c, pal, x + 13 * mm, yy - 2, 11, "solido", INK,
                       nome_fonte="Andika-Bold.ttf")
        checkbox(c, x + cols_w - 10 * mm, yy - 2, 5 * mm, HexColor("#B9C0C9"), 1)
    y_esc = M + 22 * mm
    texto(c, M, y_esc + 12 * mm, "ESCREVA AS PALAVRAS QUE ENCONTROU:", 8.5, FONT_B, SOFT)
    for k in range(2):
        linha(c, M, y_esc - k * 9 * mm, W - M, y_esc - k * 9 * mm,
              HexColor("#D3DAE2"), 1)
    rodape(c, pag, total, "Caça-palavras • palavras na horizontal")


def domino_2(c, pag, total):
    fundo(c)
    topo = faixa_titulo(c, "DOMINÓ DE SÍLABAS — PARTE 2",
                        "Junte as peças pelas sílabas iguais.",
                        PURPLE, PURPLE_L, etiqueta="jogo")
    from conteudo import DOMINO
    itens = DOMINO[24:]
    rnd = random.Random(9)
    rnd.shuffle(itens)
    pecas = [(itens[i], itens[i + 1]) for i in range(0, len(itens) - 1, 2)][:24]
    larg = W - 2 * M
    cols, rows = 3, 8
    y0 = topo - 6 * mm
    h = (y0 - M) / rows
    cw = larg / cols
    for i, (a, b) in enumerate(pecas):
        col, row = i % cols, i // cols
        x = M + col * cw + 1 * mm
        y = y0 - (row + 1) * h + 1 * mm
        rrect(c, x, y, cw - 2 * mm, h - 2 * mm, 5, WHITE, PURPLE, 1.1)
        c.setStrokeColor(HexColor("#C9CDD4"))
        c.setLineWidth(0.7)
        c.line(x + 1 * mm, y + (h - 2 * mm) / 2, x + cw - 3 * mm, y + (h - 2 * mm) / 2)
        desenhar_texto(c, a, x + cw / 2 - 2 * mm - medir(a, 13, "Andika-Bold.ttf") / 2,
                       y + h - 10 * mm, 13, "solido", INK, nome_fonte="Andika-Bold.ttf")
        desenhar_texto(c, b, x + cw / 2 - 2 * mm - medir(b, 13, "Andika-Bold.ttf") / 2,
                       y + 5 * mm, 13, "solido", PURPLE, nome_fonte="Andika-Bold.ttf")
    rodape(c, pag, total, "Dominó de sílabas • parte 2 • recorte")


def forca(c, pag, total):
    """Forca de palavras com banco de figuras."""
    fundo(c)
    topo = faixa_titulo(c, "FORCA DAS PALAVRAS",
                        "O adulto sorteia uma figura. A criança chuta letras até completar.",
                        BLUE, BLUE_L, etiqueta="jogo")
    larg = W - 2 * M
    y = topo - 8 * mm
    alt_rod = (y - (M + 46 * mm)) / 3
    for rodada in range(3):
        yy = y - rodada * alt_rod
        h = alt_rod - 5 * mm
        rrect(c, M, yy - h, larg, h, 10, WHITE, LINE, 1)
        texto(c, M + 5 * mm, yy - 8 * mm, f"RODADA {rodada + 1}", 9, FONT_B, BLUE)
        # boneco da forca (com os 6 espaços de erro)
        bx = M + 16 * mm
        by = yy - h + 9 * mm
        topo_forca = by + min(26 * mm, h - 20 * mm)
        linha(c, bx, by, bx + 16 * mm, by, INK, 1.6)          # base
        linha(c, bx + 5 * mm, by, bx + 5 * mm, topo_forca, INK, 1.6)  # poste
        linha(c, bx + 5 * mm, topo_forca, bx + 18 * mm, topo_forca, INK, 1.6)  # viga
        linha(c, bx + 18 * mm, topo_forca, bx + 18 * mm, topo_forca - 4 * mm, INK, 1.2)  # corda
        # espaços das letras
        n = 7
        xw = M + 46 * mm
        tam_casa = (W - M - 6 * mm - xw) / n
        for k in range(n):
            x = xw + k * tam_casa
            linha(c, x, yy - h * 0.52, x + tam_casa * 0.70,
                  yy - h * 0.52, HexColor("#B9C0C9"), 1.6)
        # alfabeto para riscar (quadradinhos: a criança marca o que já chutou)
        aw = (W - M - 6 * mm - xw) / 13
        ah = 8.5 * mm
        for linha_i, letras in enumerate(["ABCDEFGHIJKLM", "NOPQRSTUVWXYZ"]):
            yb = yy - h + 6 * mm + (1 - linha_i) * (ah + 2 * mm)
            for k, L in enumerate(letras):
                xb = xw + k * aw
                rrect(c, xb + 0.4 * mm, yb, aw - 0.8 * mm, ah, 2,
                      None, HexColor("#D3D9E1"), 0.7)
                texto(c, xb + aw / 2, yb + ah / 2 - 3.4, L, 9.2, FONT_B, INK, "c")

    # figuras para sortear
    y2 = M + 38 * mm
    rrect(c, M, M + 6 * mm, larg, y2 - M - 6 * mm, 10, AMBER_L, None)
    texto(c, M + 5 * mm, y2 - 7 * mm, "FIGURAS PARA SORTEAR (recorte ou aponte)", 8.5,
          FONT_B, AMBER)
    for i, (pal, fig) in enumerate(MEMORIA[:10]):
        cx = M + 13 * mm + i * ((larg - 20 * mm) / 10)
        emoji(c, fig, cx, y2 - 17.5 * mm, 10.5 * mm, AMBER)
        texto(c, cx, y2 - 24.5 * mm, pal, 6.8, FONT, SOFT, "c")
    rodape(c, pag, total, "Forca das palavras • jogo")
