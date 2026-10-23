# -*- coding: utf-8 -*-
"""Jogos imprimíveis: memória, bingo, trilha, ligue-ligue, caça-palavras, dominó."""
import random
from reportlab.lib.units import mm

from base import *
from contornos import desenhar_texto, medir
from figuras import emoji, checkbox, bolinhas_progresso
from conteudo import MEMORIA, BINGO_POOL, LIGUE, CACA, TRILHA, DOMINO


def _marcas_de_corte(c):
    """Cantinhos de corte discretos (ver base.marcas_de_corte)."""
    marcas_de_corte(c)


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

    x0 = M
    larg = W - 2 * M
    cols, rows = 4, 3
    gap = 5
    # carta com proporção de carta de baralho (mais larga que alta), centralizada na área
    cw = (larg - gap * (cols - 1)) / cols
    ch = min(cw * 1.45, (topo - M - gap * (rows - 1)) / rows)
    bloco = ch * rows + gap * (rows - 1)
    y0 = topo - (topo - M - bloco) / 2 - bloco

    def desenhar(i, x, y, w, h):
        pal, fig, tipo = cartas[i][2], cartas[i][1], cartas[i][0]
        cor = PALETA[i % 7]
        rrect(c, x, y, w, h, 8, WHITE, cor, 1.4)
        if tipo == "fig":
            emoji(c, fig, x + w / 2, y + h / 2 + 3, min(w, h) * 0.66, cor)
        else:
            tam = 21
            while medir(pal, tam, "Andika-Bold.ttf") > w - 10 and tam > 8:
                tam -= 0.5
            desenhar_texto(c, pal, x + w / 2 - medir(pal, tam, "Andika-Bold.ttf") / 2,
                           y + h / 2 - 6, tam, "solido", INK, nome_fonte="Andika-Bold.ttf")

    _tabuleiro(c, x0, y0, larg, bloco, cols, rows, desenhar, gap)
    _marcas_de_corte(c)
    rodape(c, pag, total, "Jogo da memória • recorte e brinque")


def _pool_bingo():
    """As mesmas palavras nas cartelas e nas fichas de sorteio."""
    itens = MEMORIA + BINGO_POOL
    return list(dict((p, f) for p, f in itens).items())


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
        pool = _pool_bingo()[:]
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
    _marcas_de_corte(c)
    rodape(c, pag, total, "Bingo de palavras • 6 cartelas")


def bingo_fichas(c, pag, total):
    """Fichas para recortar (sorteio do bingo)."""
    fundo(c)
    texto(c, W / 2, H - M - 6 * mm, "FICHAS DO BINGO", 16, FONT_B, PURPLE, "c")
    texto(c, W / 2, H - M - 12 * mm,
          "Recorte, dobre e coloque num saquinho. Sorteie uma por vez e mostre a figura.",
          9.5, FONT, SOFT, "c")
    itens = _pool_bingo()
    cols = 4
    x0, y0 = M, H - M - 20 * mm
    larg = W - 2 * M
    cw = larg / cols
    linhas = (len(itens) + cols - 1) // cols
    ch = min(56 * mm, (y0 - M - 4 * mm) / linhas)
    for i, (pal, fig) in enumerate(itens):
        col, row = i % cols, i // cols
        x = x0 + col * cw
        y = y0 - (row + 1) * ch
        rrect(c, x + 1.2 * mm, y + 1.2 * mm, cw - 2.4 * mm, ch - 2.4 * mm, 7, WHITE,
              HexColor("#D3D9E1"), 0.9)
        emoji(c, fig, x + cw / 2, y + ch * 0.60, min(20 * mm, ch * 0.38), PURPLE)
        tam = 15 if len(pal) <= 6 else 12
        desenhar_texto(c, pal, x + cw / 2 - medir(pal, tam, "Andika-Bold.ttf") / 2,
                       y + ch * 0.20, tam, "solido", INK, nome_fonte="Andika-Bold.ttf")
    _marcas_de_corte(c)
    rodape(c, pag, total, "Fichas do bingo • recorte")


def _trilha_tab(c, x, y, w, h):
    n = len(TRILHA)
    cols = 6
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

    # faixa de CHEGADA ocupando o resto da última linha
    i = n - 1
    row = i // cols
    col = i % cols
    if row % 2 == 1:
        col = cols - 1 - col
    bx = x + (col + 1) * (cw + gap)
    bw = x + w - bx
    cy = y + h - (row + 1) * ch - row * gap
    if bw > 14 * mm:
        rrect(c, bx, cy, bw, ch, 6, GREEN_L, GREEN, 1.4)
        estrela(c, bx + bw - 12 * mm, cy + ch / 2, min(ch * 0.34, 7 * mm), GREEN)
        texto(c, bx + 5 * mm, cy + ch / 2 - 3.2, "CHEGADA", 10, FONT_B, GREEN)
    return cw, ch


def trilha(c, pag, total):
    fundo(c)
    topo = faixa_titulo(c, "TRILHA DA LEITURA",
                        "Jogue com um dado. Leia a sílaba da casa em voz alta.",
                        GREEN, GREEN_L, etiqueta="jogo")
    larg = W - 2 * M
    y = topo - 6 * mm

    # tabuleiro (26 casas + chegada, em 6 colunas)
    alt = 100 * mm
    rrect(c, M, y - alt, larg, alt, 10, WHITE, LINE, 1)
    _trilha_tab(c, M + 4 * mm, y - alt + 4 * mm, larg - 8 * mm, alt - 8 * mm)

    # regras (altura medida pelo texto)
    regras = [
        "Cada jogador escolhe uma tampinha para andar na trilha.",
        "Jogue o dado e ande o número de casas.",
        "Leia a sílaba em voz alta. Se acertar, fica na casa; se errar, o adulto lê e a criança repete.",
        "Casa verde (estrela): avance 1 casa. Casa laranja (seta): volte 1 casa. Casa amarela (dado): jogue de novo.",
        "Ganham todos que chegam ao fim. Não precisa ter só um vencedor.",
    ]
    blocos = [quebrar(r, larg - 26 * mm, 9.2, FONT) for r in regras]
    h_regras = 13 * mm + sum(len(b) * 4.3 * mm + 2.6 * mm for b in blocos) + 3 * mm
    y2 = y - alt - 6 * mm
    rrect(c, M, y2 - h_regras, larg, h_regras, 10, HexColor("#F7F9FB"), LINE, 1)
    texto(c, M + 6 * mm, y2 - 8 * mm, "COMO JOGAR", 10, FONT_B, GREEN)
    yy = y2 - 16 * mm
    for i, linhas in enumerate(blocos):
        numero_passo(c, M + 9 * mm, yy + 2.2 * mm, i + 1, 4.4, WHITE, GREEN, 6.8)
        for j, ln in enumerate(linhas):
            texto(c, M + 15 * mm, yy - j * 4.3 * mm, ln, 9.2, FONT, INK)
        yy -= (len(linhas) * 4.3 + 2.6) * mm

    # dado e peões para recortar
    y_d = y2 - h_regras - 6 * mm
    _dado_e_peoes(c, M, M + 6 * mm, larg, y_d - M - 6 * mm)
    rodape(c, pag, total, "Trilha da leitura • use tampinhas, feijões ou os peões desta folha")


def _dado_e_peoes(c, x, y, w, h):
    """Dado (planificação em cruz) e 4 peões para recortar."""
    rrect(c, x, y, w, h, 10, WHITE, LINE, 1)
    texto(c, x + 5 * mm, y + h - 7 * mm, "RECORTE AQUI: DADO E PEÕES", 9, FONT_B, GREEN)

    lado = min(10 * mm, (h - 17 * mm) / 4)
    ox = x + 12 * mm
    oy = y + 6 * mm
    faces = {(1, 0): 2, (0, 1): 1, (1, 1): 6, (2, 1): 4, (1, 2): 3, (1, 3): 5}
    pos = {1: [(0.5, 0.5)], 2: [(0.25, 0.75), (0.75, 0.25)],
           3: [(0.25, 0.75), (0.5, 0.5), (0.75, 0.25)],
           4: [(0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75)],
           5: [(0.25, 0.25), (0.75, 0.25), (0.5, 0.5), (0.25, 0.75), (0.75, 0.75)],
           6: [(0.25, 0.2), (0.75, 0.2), (0.25, 0.5), (0.75, 0.5), (0.25, 0.8), (0.75, 0.8)]}
    for (col, row), n in faces.items():
        fx = ox + col * lado
        fy = oy + (3 - row) * lado
        rrect(c, fx, fy, lado, lado, 1.5, WHITE, INK, 1)
        for (px, py) in pos[n]:
            c.setFillColor(INK)
            c.circle(fx + px * lado, fy + py * lado, lado * 0.075, stroke=0, fill=1)

    # dobras (tracejado cinza sobre as arestas internas)
    c.saveState()
    c.setStrokeColor(HexColor("#9AA3AF"))
    c.setLineWidth(0.7)
    c.setDash(3, 3)
    dobras = [((ox + lado, oy + 3 * lado), (ox + 2 * lado, oy + 3 * lado)),
              ((ox + lado, oy + 2 * lado), (ox + 2 * lado, oy + 2 * lado)),
              ((ox + lado, oy + 1 * lado), (ox + 2 * lado, oy + 1 * lado)),
              ((ox + lado, oy + 2 * lado), (ox + lado, oy + 3 * lado)),
              ((ox + 2 * lado, oy + 2 * lado), (ox + 2 * lado, oy + 3 * lado))]
    for (x1, y1), (x2, y2) in dobras:
        c.line(x1, y1, x2, y2)
    c.restoreState()

    texto(c, ox + lado * 1.5, oy - 4 * mm,
          "dobre nas linhas • cole nas abas", 7.5, FONT, SOFT, "c")

    # peões
    px0 = x + 68 * mm
    for i in range(4):
        cx = px0 + i * 27 * mm
        cy = y + h / 2 + 3 * mm
        c.setFillColor(PALETA[i])
        c.circle(cx, cy, 8.5 * mm, stroke=0, fill=1)
        c.setFillColor(WHITE)
        c.circle(cx, cy, 4.5 * mm, stroke=0, fill=1)
        texto(c, cx, cy - 2.5, str(i + 1), 8, FONT_B, PALETA[i], "c")
        texto(c, cx, cy - 12.5 * mm, "Jogador %d" % (i + 1), 8, FONT, SOFT, "c")


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
    texto(c, M + 5 * mm, yf - 8 * mm, "VALE MAIS DE UMA TENTATIVA", 9.5, FONT_B, AMBER)
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
    gh = min(112 * mm, y0 - M - 92 * mm)
    cw = (larg - 10 * mm) / cols
    ch = gh / linhas
    x0 = M + 5 * mm
    for i, row in enumerate(grade):
        for j, ch_ in enumerate(row):
            cx = x0 + j * cw
            cy = y0 - (i + 1) * ch
            rrect(c, cx + 0.4 * mm, cy + 0.4 * mm, cw - 0.8 * mm, ch - 0.8 * mm,
                  2, None, HexColor("#DCE2E9"), 0.6)
            texto(c, cx + cw / 2, cy + ch / 2 - ch * 0.20, ch_, min(15, ch * 0.46),
                  FONT_B, INK, "c")
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

    # espaço para copiar as palavras encontradas
    n_lin_dicas = (len(dicas) + 1) // 2
    y_d = yb - n_lin_dicas * 12 * mm - 4 * mm
    rrect(c, M, y_d - 13 * mm, larg, 13 * mm, 8, CORAL_L, None)
    texto(c, M + 5 * mm, y_d - 8.5 * mm,
          "Todas estão na horizontal. Passe o dedo da esquerda para a direita, linha por linha.",
          9.5, FONT, INK)

    y_esc = y_d - 22 * mm
    texto(c, M, y_esc, "ESCREVA AS PALAVRAS QUE ENCONTROU:", 9.5, FONT_B, SOFT)
    y_esc -= 8 * mm
    n_lin = max(2, int((y_esc - (M + 6 * mm)) / (9 * mm)))
    for k in range(n_lin):
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
    _marcas_de_corte(c)
    rodape(c, pag, total, "Dominó de sílabas • recorte")


# ------------------------------------------------------------------ extras
def instrucoes_jogos(c, pag, total):
    """Página de instruções do caderno de jogos (o material pede: capa + instrução de uso)."""
    fundo(c)
    topo = faixa_titulo(c, "COMO USAR OS JOGOS",
                        "Para o adulto: 3 minutos lendo, meses brincando.",
                        AMBER, AMBER_L, etiqueta="leia primeiro")
    larg = W - 2 * M

    # ---- passos de preparo
    passos = [
        ("1", "IMPRIMA", "Cartas e fichas ficam melhores em papel mais grosso (120 g ou cartolina)."),
        ("2", "RECORTE NOS CANTINHOS", "As cruzinhas dos cantos mostram onde cortar. Corte reto, sem ponta."),
        ("3", "GUARDE EM ENVELOPES", "Um envelope por jogo. Jogo perdido não volta; envelope mantém tudo junto."),
        ("4", "ESCOLHA UM POR VEZ", "Um jogo por dia. Guarde antes de cansar: na próxima vez ela quer voltar."),
    ]
    y = topo - 6 * mm
    for num, tit, txt in passos:
        h = 18 * mm
        rrect(c, M, y - h, larg, h, 9, WHITE, LINE, 1)
        numero_passo(c, M + 9 * mm, y - h / 2, num, 5.6, WHITE, AMBER, 9)
        texto(c, M + 18 * mm, y - 7 * mm, tit, 9.8, FONT_B, INK)
        for j, ln in enumerate(quebrar(txt, larg - 26 * mm, 9, FONT)):
            texto(c, M + 18 * mm, y - 12.4 * mm - j * 4.2 * mm, ln, 9, FONT, SOFT)
        y -= h + 3 * mm

    # ---- ordem dos jogos
    y -= 2 * mm
    texto(c, M, y - 2 * mm, "ORDEM SUGERIDA — DO MAIS FÁCIL AO MAIS DIFÍCIL", 9.5, FONT_B, AMBER)
    y -= 8 * mm
    jogos = [
        ("🃏", "Memória", "figura + palavra", "reconhecer a palavra inteira"),
        ("🔗", "Ligue a figura à palavra", "passe o dedo", "juntar som e escrita"),
        ("🔔", "Bingo", "6 cartelas", "achar a palavra no meio de outras"),
        ("🔍", "Caça-palavras", "3 níveis", "olhar letra por letra"),
        ("🁢", "Dominó de sílabas", "2 folhas", "montar palavras por sílaba"),
        ("🏁", "Trilha da leitura", "dado e peões", "ler rápido, sem travar"),
        ("✏️", "Forca", "3 rodadas", "lembrar das letras sem apoio"),
    ]
    passo = (y - (M + 46 * mm)) / len(jogos)
    for i, (fig, tit, sub, objetivo) in enumerate(jogos):
        yy = y - i * passo
        h = min(passo - 2.4 * mm, 15 * mm)
        rrect(c, M, yy - h, larg, h, 7, WHITE, HexColor("#E8E1D3"), 1)
        emoji(c, fig, M + 8 * mm, yy - h / 2, 8 * mm, AMBER)
        texto(c, M + 17 * mm, yy - h / 2 - 3.4, tit, 10, FONT_B, INK)
        texto(c, M + 72 * mm, yy - h / 2 - 3, sub, 9, FONT, SOFT)
        texto(c, W - M - 5 * mm, yy - h / 2 - 3, objetivo, 9, FONT, INK, "r")

    # ---- caixa final: o que fazer quando erra
    yb = M + 4 * mm
    hb = 40 * mm
    rrect(c, M, yb, larg, hb, 10, GREEN_L, None)
    texto(c, M + 6 * mm, yb + hb - 9 * mm, "QUANDO ELA ERRA", 9.5, FONT_B, GREEN)
    dicas = [
        "Não corrija tudo de uma vez: escolha 1 coisa por rodada.",
        "Leia junto, devagar, e peça só que ela repita a parte certa.",
        "Se errar duas vezes seguidas, pare o jogo e volte amanhã — erro repetido vira desânimo.",
        "Ganhar não é o objetivo. O objetivo é ler. Deixe ela ganhar algumas vezes.",
    ]
    for i, t in enumerate(dicas):
        for j, ln in enumerate(quebrar(t, larg - 16 * mm, 9, FONT)):
            texto(c, M + 6 * mm, yb + hb - 17 * mm - i * 6.4 * mm - j * 4.2 * mm,
                  ("•  " if j == 0 else "   ") + ln, 9, FONT, INK)
    marcas_de_corte(c)
    rodape(c, pag, total)


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
    texto(c, M + 16 * mm, box_topo - 8.5 * mm, "ANTES DE JOGAR", 9, FONT_B, AMBER)
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
    _marcas_de_corte(c)
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
                    ["G", "A", "L", "I", "N", "H", "A", "S"],
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


def _garantir_palavras(grade, dicas):
    """Toda palavra da lista precisa existir na grade (na horizontal)."""
    linhas = ["".join(r) for r in grade]
    faltando = [p for p, _ in dicas if not any(p in l for l in linhas)]
    if faltando:
        raise ValueError("caça-palavras sem a palavra: " + ", ".join(faltando))


def _caca_generico(c, pag, total, titulo, grade, dicas):
    _garantir_palavras(grade, dicas)
    fundo(c)
    topo = faixa_titulo(c, "CAÇA-PALAVRAS", titulo, CORAL, CORAL_L, etiqueta="jogo")
    larg = W - 2 * M
    linhas, cols = len(grade), max(len(r) for r in grade)
    y0 = topo - 8 * mm
    gh = min(112 * mm, y0 - M - 60 * mm)
    cw = (larg - 10 * mm) / cols
    ch = gh / linhas
    x0 = M + 5 * mm
    for i, row in enumerate(grade):
        for j, ch_ in enumerate(row):
            cx = x0 + j * cw
            cy = y0 - (i + 1) * ch
            rrect(c, cx + 0.4 * mm, cy + 0.4 * mm, cw - 0.8 * mm, ch - 0.8 * mm,
                  2, None, HexColor("#DCE2E9"), 0.6)
            texto(c, cx + cw / 2, cy + ch / 2 - ch * 0.20, ch_, min(14, ch * 0.44),
                  FONT_B, INK, "c")
    yb = y0 - gh - 10 * mm
    texto(c, M, yb, "PALAVRAS PARA ENCONTRAR", 9.5, FONT_B, CORAL)
    yb -= 9 * mm
    cols_w = larg / 2
    for i, (pal, fig) in enumerate(dicas):
        col, row = i % 2, i // 2
        x = M + col * cols_w
        yy = yb - row * 13 * mm
        emoji(c, fig, x + 6 * mm, yy + 1 * mm, 10 * mm, CORAL)
        desenhar_texto(c, pal, x + 14 * mm, yy - 2, 12.5, "solido", INK,
                       nome_fonte="Andika-Bold.ttf")
        checkbox(c, x + cols_w - 10 * mm, yy - 2, 5.5 * mm, HexColor("#B9C0C9"), 1)

    # dica de busca
    n_lin_dicas = (len(dicas) + 1) // 2
    y_d = yb - n_lin_dicas * 13 * mm - 2 * mm
    rrect(c, M, y_d - 13 * mm, larg, 13 * mm, 8, CORAL_L, None)
    texto(c, M + 5 * mm, y_d - 8.5 * mm,
          "Todas estão na horizontal. Passe o dedo da esquerda para a direita, linha por linha.",
          9.5, FONT, INK)

    # espaço para copiar as palavras encontradas (aproveita o resto da folha)
    y_esc = y_d - 22 * mm
    texto(c, M, y_esc, "ESCREVA AS PALAVRAS QUE ENCONTROU:", 9.5, FONT_B, SOFT)
    y_esc -= 8 * mm
    n_lin = max(2, int((y_esc - (M + 6 * mm)) / (9 * mm)))
    for k in range(n_lin):
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
    _marcas_de_corte(c)
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
    texto(c, M + 5 * mm, y2 - 7 * mm, "FIGURAS PARA SORTEAR (recorte ou aponte)", 9,
          FONT_B, AMBER)
    for i, (pal, fig) in enumerate(MEMORIA[:10]):
        cx = M + 13 * mm + i * ((larg - 20 * mm) / 10)
        emoji(c, fig, cx, y2 - 17.5 * mm, 10.5 * mm, AMBER)
        texto(c, cx, y2 - 24.5 * mm, pal, 6.8, FONT, SOFT, "c")
    rodape(c, pag, total, "Forca das palavras • jogo")
