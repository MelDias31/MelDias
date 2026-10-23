# -*- coding: utf-8 -*-
"""Cartilha do alfabeto: uma letra por folha A4 (colorir + traçar + achar)."""
import random
from reportlab.lib.units import mm

from base import *
from base import largura
from letras import DEFS, desenhar_letra, desenhar_glifo
from contornos import desenhar_texto, medir
from figuras import emoji, emoji_quadro, checkbox
from conteudo import ALFABETO, ORDEM, DICA_LETRA


def capa(c, pag=1, total=1, **kw):
    fundo(c, CREAM)
    # faixa superior
    c.setFillColor(TEAL)
    c.rect(0, H - 86 * mm, W, 86 * mm, stroke=0, fill=1)
    coruja(c, W / 2, H - 38 * mm, 20 * mm, AMBER, AMBER_L, WHITE, CORAL, INK)
    texto(c, W / 2, H - 64 * mm, "MEU ALFABETO", 38, FONT_B, WHITE, "c")
    texto(c, W / 2, H - 75 * mm, "colorir • traçar • encontrar", 13, FONT, TEAL_L, "c")

    y = H - 96 * mm
    texto(c, W / 2, y, "26 letras para brincar de aprender", 16, FONT_B, INK, "c")
    paragrafo(c, M + 16 * mm, y - 9 * mm, W - 2 * M - 32 * mm,
              "Uma folha por letra. Sem pressa, sem nota, sem comparação. Pinte a letra "
              "grande, siga as setas, cubra os pontinhos e encontre a letra escondida. "
              "Se cansar, pare — a próxima vez também conta.",
              10.5, FONT, SOFT, align="c")

    # nome
    y2 = y - 54 * mm
    rrect(c, M + 12 * mm, y2, W - 2 * M - 24 * mm, 30 * mm, 10, WHITE, LINE, 1)
    texto(c, M + 20 * mm, y2 + 20 * mm, "NOME:", 10.5, FONT_B, INK)
    linha(c, M + 34 * mm, y2 + 18 * mm, W - M - 20 * mm, y2 + 18 * mm, LINE, 1.2)
    texto(c, M + 20 * mm, y2 + 9 * mm, "QUEM VAI USAR ESTE CADERNO:", 9, FONT_B, SOFT)
    linha(c, M + 84 * mm, y2 + 7 * mm, W - M - 20 * mm, y2 + 7 * mm, LINE, 0.9)

    # 3 missões
    y3 = y2 - 10 * mm
    rrect(c, M + 12 * mm, y3 - 22 * mm, W - 2 * M - 24 * mm, 22 * mm, 10, TEAL_L, None)
    texto(c, M + 20 * mm, y3 - 7 * mm, "CADA LETRA TEM 3 MISSÕES", 9, FONT_B, TEAL)
    for i, (fig, txt) in enumerate([("✏️", "traçar"), ("🎨", "colorir"), ("🔍", "achar")]):
        emoji(c, fig, M + 24 * mm + i * 30 * mm, y3 - 16 * mm, 8 * mm, TEAL)
        texto(c, M + 30 * mm + i * 30 * mm, y3 - 17.5 * mm, txt, 9, FONT, INK)

    # alfabeto
    y4 = y3 - 30 * mm
    rrect(c, M + 12 * mm, y4 - 26 * mm, W - 2 * M - 24 * mm, 26 * mm, 10, WHITE, LINE, 1)
    texto(c, W / 2, y4 - 9 * mm, "COMECE PELA PRIMEIRA LETRA DO NOME DELA", 9,
          FONT_B, TEAL, "c")
    tam = 15
    larg_total = largura(ORDEM, tam, FONT_B) + 25 * 1.0
    px = W / 2 - larg_total / 2
    for i, L in enumerate(ORDEM):
        c.setFont(FONT_B, tam)
        c.setFillColor(PALETA[i % 7])
        c.drawString(px, y4 - 20 * mm, L)
        px += largura(L, tam, FONT_B) + 1.0

    # dica final
    y5 = y4 - 36 * mm
    rrect(c, M + 12 * mm, y5 - 18 * mm, W - 2 * M - 24 * mm, 18 * mm, 8, AMBER_L, None)
    texto(c, M + 20 * mm, y5 - 7 * mm, "IMPRIMA SÓ A FOLHA DO DIA.", 8.5, FONT_B, AMBER)
    texto(c, M + 20 * mm, y5 - 13 * mm,
          "Muitas folhas na mesa = distração. Uma folha por vez funciona melhor.", 8,
          FONT, INK)

    rodape(c, pag, total)


def _grade_letras(c, x, y, w, h, alvo, linhas=4, colunas=8, semente=1):
    """Grade de letras com a letra-alvo escondida (busca visual)."""
    rnd = random.Random(semente + ord(alvo))
    parecidas = {"B": "BDPR", "D": "DBPQ", "P": "PBQO", "Q": "QPOG",
                 "M": "MNW", "N": "NMH", "E": "EFL", "F": "FEL",
                 "C": "COG", "G": "GCQ", "U": "UVW", "V": "VUW",
                 "I": "ILJ", "L": "LIJ", "S": "SZC", "Z": "ZSN",
                 "A": "AVH", "O": "OQD", "T": "TIF", "J": "JIL",
                 "K": "KXR", "R": "RPB", "H": "HNM", "W": "WMN",
                 "X": "XKY", "Y": "YVX"}
    distratores = parecidas.get(alvo, "AEIOU")
    cw, ch = w / colunas, h / linhas
    for i in range(linhas):
        for j in range(colunas):
            cx = x + cw * j + cw / 2
            cy = y + h - ch * i - ch / 2
            if rnd.random() < 0.30:
                letra, cor = alvo, INK
            else:
                letra, cor = rnd.choice(distratores), SOFT
            tamanho = min(cw, ch) * 0.52
            c.setFont(FONT_B, tamanho)
            c.setFillColor(cor)
            c.drawCentredString(cx, cy - tamanho * 0.35, letra)
    # moldura
    rrect(c, x, y, w, h, 8, None, LINE, 1)


def folha_letra(c, pag, total, letra):
    palavra, fig, cor_idx = ALFABETO[letra]
    cor = PALETA[cor_idx]
    cor_l = PALETA_L[cor_idx]
    fundo(c)

    topo = faixa_titulo(c, f"LETRA {letra}",
                        f"{palavra.capitalize()}  —  {DICA_LETRA[letra].split('. ', 1)[1]}",
                        cor, cor_l, etiqueta=f"{ORDEM.index(letra) + 1} de 26")

    # ------------------------------------------------ zona 1: letra grande + figura
    z1_top = topo - 4 * mm
    z1_h = 84 * mm
    z1_y = z1_top - z1_h

    bx, bw = M, 86 * mm
    rrect(c, bx, z1_y, bw, z1_h, 12, WHITE, LINE, 1.1)
    larg = DEFS[letra][0]
    alt = 58 * mm
    escala = alt / 100.0
    lx = bx + (bw - larg * escala) / 2
    ly = z1_y + 10 * mm
    desenhar_letra(c, letra, lx, ly, alt, "cheio", HexColor("#E8EEF4"),
                   mostrar_numeros=False, mostrar_seta=False, mostrar_inicio=False)
    desenhar_letra(c, letra, lx, ly, alt, "solido", INK, largura_linha=1.5,
                   mostrar_numeros=False, mostrar_seta=False, mostrar_inicio=False)
    for i, stroke in enumerate(DEFS[letra][1]):
        px, py = lx + stroke[0][0] * escala, ly + stroke[0][1] * escala
        _num(c, px, py, i + 1, 7.0, cor)
    texto(c, bx + bw / 2, z1_y + 4.5 * mm, "pinte por dentro • siga os números",
          8.2, FONT, SOFT, "c")

    # figura + palavra + minúscula
    fx = bx + bw + 4 * mm
    fw = W - M - fx
    rrect(c, fx, z1_y, fw, z1_h, 12, cor_l, None)
    emoji(c, fig, fx + fw / 2, z1_y + z1_h - 27 * mm, 31 * mm, cor)
    _palavra_destaque(c, palavra, fx, z1_y + 26 * mm, fw, cor, tam_base=19)
    # fita com a minúscula
    c.setFillColor(WHITE)
    c.roundRect(fx + fw / 2 - 17 * mm, z1_y + 7 * mm, 34 * mm, 13 * mm, 6,
                stroke=0, fill=1)
    c.setFont(FONT_B, 30)
    c.setFillColor(cor)
    c.drawCentredString(fx + fw / 2 - 4 * mm, z1_y + 9 * mm, letra.lower())
    texto(c, fx + fw / 2 + 8 * mm, z1_y + 11.5 * mm, "minúscula", 7.5, FONT, SOFT, "c")

    # ------------------------------------------------ zona 2: traçado
    z2_top = z1_y - 4 * mm
    z2_h = 86 * mm
    z2_y = z2_top - z2_h
    rrect(c, M, z2_y, W - 2 * M, z2_h, 12, WHITE, LINE, 1.1)
    texto(c, M + 5 * mm, z2_top - 7.5 * mm, "TRACEDO", 9, FONT_B, cor)
    linha(c, M + 30 * mm, z2_top - 8 * mm, W - M - 5 * mm, z2_top - 8 * mm, LINE, 0.8)

    linhas = [
        ("1", "Siga as setas", "guia", True, letra),
        ("2", "Cubra o tracejado", "guia", False, letra),
        ("3", "Cubra os pontinhos", "pontilhado", False, letra),
        ("4", "A minúscula", "min", False, letra.lower()),
    ]
    alt_l = 11 * mm
    x_lab = M + 5 * mm
    x_esc = M + 36 * mm
    larg_esc = W - M - 5 * mm - x_esc
    for k, (num, rotulo, modo, com_num, alvo) in enumerate(linhas):
        ry = z2_top - 24 * mm - k * 18 * mm        # linha de base da escrita
        _num(c, x_lab + 2 * mm, ry + alt_l * 0.55, num, 7.0, cor, fundo=cor_l,
             texto_cor=cor)
        texto(c, x_lab + 6.5 * mm, ry + alt_l * 0.75 - 3.2 * mm, rotulo, 7.8, FONT, INK)
        pauta(c, x_esc, ry, larg_esc, alt_l, HexColor("#DCE2E9"))
        px = x_esc + 2 * mm
        espac = 17 * mm if modo != "min" else 15 * mm
        primeira = True
        while px + 12 * mm < x_esc + larg_esc:
            if modo == "min":
                desenhar_texto(c, alvo, px, ry, alt_l * 1.02, "guia", SOFT,
                               lw=1.4)
            else:
                desenhar_letra(c, alvo, px, ry, alt_l, modo, SOFT,
                               largura_linha=1.4, mostrar_numeros=com_num and primeira,
                               mostrar_seta=com_num and primeira,
                               mostrar_inicio=not com_num, cor_numero=cor)
            px += espac
            primeira = False

    # ------------------------------------------------ zona 3: caça-letra
    z3_top = z2_y - 4 * mm
    z3_y = M + 3 * mm
    z3_h = z3_top - z3_y
    rrect(c, M, z3_y, W - 2 * M, z3_h, 12, cor_l, None)
    texto(c, M + 5 * mm, z3_top - 7.5 * mm,
          f"5. Ache e circule todas as letras {letra}", 9.5, FONT_B, INK)
    texto(c, W - M - 5 * mm, z3_top - 7.5 * mm, "quantas você achou?", 8, FONT, SOFT, "r")
    rrect(c, M + 62 * mm, z3_top - 9.6 * mm, 12 * mm, 6.0 * mm, 2, WHITE,
          HexColor("#9AA3AF"), 1)
    _grade_letras(c, M + 5 * mm, z3_y + 3 * mm, W - 2 * M - 10 * mm,
                  z3_h - 15 * mm, letra, 3, 9, semente=17)
    rodape(c, pag, total)


def _num(c, cx, cy, n, tam, cor, fundo=WHITE, texto_cor=None):
    r = tam * 0.95
    c.setFillColor(fundo)
    c.setStrokeColor(cor)
    c.setLineWidth(1.3)
    c.circle(cx, cy, r, stroke=1, fill=1)
    texto(c, cx, cy - tam * 0.34, str(n), tam, FONT_B, texto_cor or cor, "c")


def _palavra_destaque(c, palavra, x, y, w, cor, tam_base=17):
    letras = list(palavra)
    tam = tam_base
    while medir(palavra, tam, "Andika-Bold.ttf", espaco_extra=0.6) > w - 10 * mm and tam > 9:
        tam -= 0.5
    largs = [medir(ch, tam, "Andika-Bold.ttf", espaco_extra=0.6) for ch in letras]
    px0 = x + (w - sum(largs)) / 2
    for i, ch in enumerate(letras):
        alvo = (i == 0)
        desenhar_texto(c, ch, px0, y, tam, "solido", cor if alvo else INK,
                       nome_fonte="Andika-Bold.ttf", espaco_extra=0.6)
        if alvo:
            linha(c, px0 + 0.5, y - 2.2, px0 + largs[i] - 1.5, y - 2.2, cor, 2)
        px0 += largs[i]


def _contar_na_grade(letra):
    return 8


def folha_letra_minuscula(c, pag, total, letra):
    """Versão focada em minúsculas: para depois do domínio das maiúsculas."""
    letra = letra.upper()
    palavra, fig, cor_idx = ALFABETO[letra]
    cor = PALETA[cor_idx]
    cor_l = PALETA_L[cor_idx]
    fundo(c)
    topo = faixa_titulo(c, f"{letra}  {letra.lower()}",
                        f"{palavra.capitalize()} — maiúscula e minúscula",
                        cor, cor_l, etiqueta=f"{ORDEM.index(letra) + 1} de 26")
    larg = W - 2 * M

    # ---------------- bloco superior: as duas formas lado a lado
    y1 = topo - 5 * mm
    h1 = 62 * mm
    rrect(c, M, y1 - h1, larg, h1, 12, WHITE, LINE, 1.1)
    alt = 34 * mm
    base = y1 - h1 + 18 * mm
    # maiúscula
    texto(c, M + 30 * mm, y1 - 8 * mm, "MAIÚSCULA", 8.5, FONT_B, cor, "c")
    desenhar_letra(c, letra, M + 30 * mm - DEFS[letra][0] * alt / 100 / 2, base, alt,
                   "solido", INK, largura_linha=1.6, mostrar_numeros=False,
                   mostrar_seta=False, mostrar_inicio=False)
    # minúscula (traço cheio + pontilhado ao lado)
    texto(c, M + larg * 0.44, y1 - 8 * mm, "minúscula", 8.5, FONT_B, cor, "c")
    desenhar_texto(c, letra.lower(), M + larg * 0.44 - medir(letra.lower(), alt * 0.8) / 2,
                   base, alt * 0.8, "solido", cor, nome_fonte="Andika-Bold.ttf")
    texto(c, M + larg * 0.72, y1 - 8 * mm, "minúscula pontilhada", 8, FONT_B, SOFT, "c")
    desenhar_texto(c, letra.lower(), M + larg * 0.72 - medir(letra.lower(), alt * 0.8) / 2,
                   base, alt * 0.8, "pontilhado", SOFT, nome_fonte="Andika-Bold.ttf")
    emoji(c, fig, W - M - 14 * mm, y1 - h1 / 2, 15 * mm, cor)
    # pauta de referência
    linha(c, M + 6 * mm, base - 2 * mm, W - M - 26 * mm, base - 2 * mm,
          HexColor("#D5DCE5"), 0.8)

    # ---------------- treino
    y = y1 - h1 - 6 * mm
    texto(c, M, y, "TREINE AS DUAS FORMAS", 9, FONT_B, cor)
    y -= 6 * mm
    n = 9
    h_lin = (y - (M + 6 * mm)) / n
    alt_l = h_lin - 6.5 * mm
    for k in range(n):
        base_l = y - (k + 1) * h_lin + 4 * mm
        pauta(c, M + 34 * mm, base_l - 1 * mm, larg - 38 * mm, alt_l + 1 * mm,
              HexColor("#D5DCE5"))
        # modelos à esquerda: maiúscula e minúscula
        desenhar_letra(c, letra, M + 2 * mm, base_l, alt_l, "guia" if k % 2 == 0 else "pontilhado",
                       SOFT, largura_linha=1.1, mostrar_numeros=False,
                       mostrar_seta=False, mostrar_inicio=False)
        desenhar_texto(c, letra.lower(), M + 16 * mm, base_l, alt_l * 0.80,
                       "guia" if k % 2 == 0 else "pontilhado", SOFT)
        # repetições pontilhadas para cobrir, distribuídas na linha
        # (nas últimas linhas elas somem aos poucos: a criança passa a escrever sozinha)
        n_rep = 99 if k < 5 else (2 if k < 7 else 0)
        xx = M + 40 * mm
        j = 0
        while xx < W - M - 16 * mm and j < n_rep:
            desenhar_letra(c, letra, xx, base_l, alt_l, "pontilhado", SOFT,
                           largura_linha=1.2, mostrar_numeros=False,
                           mostrar_seta=False, mostrar_inicio=False)
            desenhar_texto(c, letra.lower(), xx + 11.5 * mm, base_l, alt_l * 0.72,
                           "pontilhado", SOFT)
            xx += 31 * mm
            j += 1
    rodape(c, pag, total)


    rodape(c, pag, total)


# ------------------------------------------------------------------ extras
def instrucoes(c, pag, total):
    fundo(c)
    topo = faixa_titulo(c, "COMO USAR ESTE CADERNO",
                        "Para o adulto: leia uma vez e comece hoje mesmo.",
                        TEAL, TEAL_L, etiqueta="leia primeiro")
    larg = W - 2 * M
    y = topo - 6 * mm

    # 4 passos
    passos = [
        ("1", "UMA FOLHA POR VEZ", "Imprima só a folha da letra do dia. Folha cheia na mesa = distração."),
        ("2", "10 MINUTOS", "Comece pela caixa grande, siga a ordem 1, 2, 3 dos traços e pare quando ela cansar."),
        ("3", "PINTE, TRACE, PROCURE", "As três atividades da folha trabalham a mesma letra de formas diferentes."),
        ("4", "VOLTE SEMPRE", "Repetir a mesma letra em dias diferentes é melhor que fazer muitas letras no mesmo dia."),
    ]
    for i, (num, tit, txt) in enumerate(passos):
        h = 21 * mm
        rrect(c, M, y - h, larg, h, 9, WHITE, LINE, 1)
        numero_passo(c, M + 9 * mm, y - h / 2, num, 6, WHITE, TEAL, 9)
        texto(c, M + 18 * mm, y - 8 * mm, tit, 9.8, FONT_B, INK)
        for j, ln in enumerate(quebrar(txt, larg - 24 * mm, 8.6, FONT)):
            texto(c, M + 18 * mm, y - 13.5 * mm - j * 4.1 * mm, ln, 8.6, FONT, SOFT)
        y -= h + 3 * mm

    # anatomia da folha
    y -= 1 * mm
    texto(c, M, y - 3 * mm, "O QUE TEM EM CADA FOLHA", 9.5, FONT_B, TEAL)
    y -= 9 * mm
    itens = [
        ("🐝", "LETRA GRANDE", "Para colorir por dentro, seguindo os números de 1 a 3. O número mostra onde começar."),
        ("⚽", "FIGURA + PALAVRA", "A imagem dá o som da letra. A palavra aparece com a letra inicial destacada."),
        ("✏️", "TRÊS LINHAS DE TRAÇADO", "Siga as setas, cubra o tracejado e depois cubra os pontinhos. A minúscula vem por último."),
        ("🔍", "CAÇA-LETRA", "Encontrar a letra entre parecidas treina o olho a diferenciar b/d, p/q, m/n."),
    ]
    for fig, tit, txt in itens:
        h = 17 * mm
        rrect(c, M, y - h, larg, h, 8, PALETA_L[0], None)
        emoji(c, fig, M + 9 * mm, y - h / 2, 10 * mm, TEAL)
        texto(c, M + 18 * mm, y - 7 * mm, tit, 9, FONT_B, INK)
        for j, ln in enumerate(quebrar(txt, larg - 24 * mm, 8.4, FONT)):
            texto(c, M + 18 * mm, y - 12 * mm - j * 4 * mm, ln, 8.4, FONT, SOFT)
        y -= h + 3 * mm

    # ordem recomendada
    y -= 2 * mm
    rrect(c, M, M + 4 * mm, larg, y - M - 4 * mm, 10, AMBER_L, None)
    texto(c, M + 5 * mm, y - 8 * mm, "ORDEM RECOMENDADA DAS LETRAS", 9, FONT_B, AMBER)
    paragrafo(c, M + 5 * mm, y - 14 * mm, larg - 10 * mm,
              "Não comece pelo alfabeto em ordem. Comece pelo nome dela e pelas letras "
              "que ela já reconhece. Depois siga: A, E, I, O, U (vogais), M, P, B, D, T, "
              "L, C, S, R, N, F, V, G, J, Z, X, Q, H, K, W, Y.", 8.8, FONT, INK)
    paragrafo(c, M + 5 * mm, y - 27 * mm, larg - 10 * mm,
              "Se ela tem TDAH, faça 1 letra por dia, no máximo 3 por semana. Uma letra "
              "bem consolidada vale mais que 26 letras vistas.", 8.8, FONT, INK)
    rodape(c, pag, total)


def parecidas(c, pag, total):
    """Página de letras que se confundem (b/d/p/q, m/n, u/v)."""
    fundo(c)
    topo = faixa_titulo(c, "LETRAS QUE SE PARECEM",
                        "Truques para o olho não se enganar",
                        PINK, PINK_L, etiqueta="atenção visual")
    larg = W - 2 * M
    y = topo - 6 * mm

    grupos = [
        ("B e D", ["b", "d"], "O pauzinho do B fica atrás da barriga; o do D fica na frente.",
         "🛏️", "Use a cama: “b” é a cabeceira, “d” é o pé."),
        ("P e Q", ["p", "q"], "O rabinho do P desce reto; o do Q vira para a direita.",
         "🍳", "P de panela: barriga em cima, cabo embaixo."),
        ("M e N", ["m", "n"], "O M tem dois montes; o N tem um monte e uma perna.",
         "⛰️", "M de montanha (dois picos)."),
        ("U e V", ["u", "v"], "O U é fundo e redondo; o V é pontudo.",
         "🥤", "U de copo, V de vale."),
    ]
    for nome, letras, truque, fig, dica in grupos:
        h = 34 * mm
        rrect(c, M, y - h, larg, h, 10, WHITE, LINE, 1)
        c.setFillColor(PINK)
        c.roundRect(M, y - h, 4, h, 2, stroke=0, fill=1)
        texto(c, M + 7 * mm, y - 7.5 * mm, nome, 10, FONT_B, PINK)
        # as duas letras grandes
        for i, l in enumerate(letras):
            cx = M + 15 * mm + i * 20 * mm
            c.setFont(FONT_B, 30)
            c.setFillColor(INK)
            c.drawCentredString(cx, y - h + 9 * mm, l)
            texto(c, cx, y - h + 4 * mm, "minúscula", 6.2, FONT, SOFT, "c")
        # figura
        emoji(c, fig, M + 52 * mm, y - h / 2 - 1 * mm, 11 * mm, PINK)
        # texto
        tx = M + 62 * mm
        for j, ln in enumerate(quebrar(truque, W - M - tx - 4 * mm, 8.4, FONT)):
            texto(c, tx, y - 11 * mm - j * 4.2 * mm, ln, 8.4, FONT, INK)
        texto(c, tx, y - h + 12 * mm, dica, 8.2, FONT_I, SOFT)
        # treino: 6 repetições
        for k in range(6):
            desenhar_texto(c, letras[k % 2], tx + k * 9 * mm, y - h + 4 * mm, 12,
                           "guia", SOFT)
        y -= h + 3 * mm

    # brincadeira
    rrect(c, M, M + 4 * mm, larg, y - M - 4 * mm, 10, AMBER_L, None)
    texto(c, M + 5 * mm, y - 8 * mm, "BRINCADEIRA DO ESPELHO", 9, FONT_B, AMBER)
    paragrafo(c, M + 5 * mm, y - 14 * mm, larg - 10 * mm,
              "Escreva b, d, p e q em cartõezinhos. Mostre um por vez por 3 segundos e "
              "peça o nome da letra. Repita 5 vezes, 3 vezes por semana. Cronometrar "
              "transforma o treino em jogo.", 8.6, FONT, INK)
    # mini treino para apontar
    yy = y - 34 * mm
    texto(c, M + 5 * mm, yy + 6 * mm, "APONTE E DIGA O NOME:", 8, FONT_B, SOFT)
    seq = "b d q p b p d q"
    for k, l in enumerate(seq.split()):
        cx = M + 14 * mm + k * 22 * mm
        c.setFont(FONT_B, 22)
        c.setFillColor(INK)
        c.drawCentredString(cx, yy - 8 * mm, l)
        linha(c, cx - 6 * mm, yy - 12 * mm, cx + 6 * mm, yy - 12 * mm,
              HexColor("#D6C7A8"), 0.8)
    rodape(c, pag, total)


def _mural(c, letras, titulo, cor):
    fundo(c)
    topo = faixa_titulo(c, titulo, "Recorte, cole na parede e aponte todos os dias.",
                        cor, PALETA_L[PALETA.index(cor)], etiqueta="mural")
    larg = W - 2 * M
    cols, rows = 3, 5
    cw = (larg - 4 * mm) / cols
    ch = (topo - M - 6 * mm) / rows
    for i, L in enumerate(letras):
        col, row = i % cols, i // cols
        x = M + col * (cw + 2 * mm)
        y = topo - 3 * mm - (row + 1) * ch
        palavra, fig, idx = ALFABETO[L]
        c_cor, c_l = PALETA[idx], PALETA_L[idx]
        h = ch - 3 * mm
        rrect(c, x, y, cw, h, 9, WHITE, c_cor, 1.6)
        # faixa superior com a palavra
        c.setFillColor(c_l)
        c.roundRect(x + 1.2 * mm, y + h - 7.2 * mm, cw - 2.4 * mm, 6 * mm, 4,
                    stroke=0, fill=1)
        texto(c, x + cw / 2, y + h - 5.4 * mm, palavra, 8, FONT_B, c_cor, "c")
        # letra grande solida + guia sobreposta
        alt = h - 20 * mm
        lx = x + 7 * mm
        ly = y + 7 * mm
        desenhar_letra(c, L, lx, ly, alt, "solido", c_cor, largura_linha=1.2,
                       mostrar_numeros=False, mostrar_seta=False, mostrar_inicio=False)
        # figura à direita
        emoji(c, fig, x + cw - 13 * mm, y + h / 2 - 1 * mm, 15 * mm, c_cor)
        # minúscula
        c.setFont(FONT_B, 15)
        c.setFillColor(SOFT)
        c.drawString(x + 4 * mm, y + 3 * mm, L.lower())
        texto(c, x + 12 * mm, y + 3.4 * mm, "minúscula", 6.2, FONT, SOFT)


def alfabeto_mural(c, pag, total):
    _mural(c, ORDEM[:15], "MURAL DO ALFABETO — PARTE 1", TEAL)
    rodape(c, pag, total)


def alfabeto_mural_2(c, pag, total):
    _mural(c, ORDEM[15:], "MURAL DO ALFABETO — PARTE 2", BLUE)
    rodape(c, pag, total)


def bingo_letras(c, pag, total):
    """Cartelas de bingo de letras (6 por folha)."""
    import random as _r
    fundo(c)
    texto(c, W / 2, H - M - 6 * mm, "BINGO DE LETRAS", 16, FONT_B, TEAL, "c")
    texto(c, W / 2, H - M - 12 * mm,
          "Recorte as cartelas. Cante as letras e a criança marca as que tiver.", 9,
          FONT, SOFT, "c")
    rnd = _r.Random(11)
    larg = W - 2 * M
    alt = H - 2 * M - 42 * mm
    cw = (larg - 6 * mm) / 2
    ch = (alt - 2 * 6 * mm) / 3
    for k in range(6):
        col, row = k % 2, k // 2
        x = M + col * (cw + 6 * mm)
        y = H - M - 20 * mm - (row + 1) * ch - row * 6 * mm
        rrect(c, x, y, cw, ch, 8, WHITE, TEAL, 1.3)
        texto(c, x + cw / 2, y + ch - 6 * mm, f"CARTELA {k + 1}", 8.5, FONT_B, TEAL, "c")
        escolhas = rnd.sample(ORDEM, 12)
        c2 = cw / 4
        h2 = (ch - 12 * mm) / 3
        for i, L in enumerate(escolhas):
            cc, rr = i % 4, i // 4
            bx = x + cc * c2
            by = y + 3 * mm + (2 - rr) * h2
            rrect(c, bx + 0.6 * mm, by + 0.6 * mm, c2 - 1.2 * mm, h2 - 1.2 * mm,
                  3, None, HexColor("#D3D9E1"), 0.8)
            texto(c, bx + c2 / 2, by + h2 / 2 - 5, L, 18, FONT_B, INK, "c")
    texto(c, W / 2, M + 6 * mm,
          "Fichas para cantar: escreva as letras em pedacinhos de papel ou use o alfabeto móvel.",
          8.5, FONT_I, SOFT, "c")
    rodape(c, pag, total)


def quadro_progresso(c, pag, total):
    """Mapa das 26 letras com duas colunas de checagem."""
    fundo(c)
    topo = faixa_titulo(c, "MAPA DAS 26 LETRAS",
                        "Pinte quando reconhece sem ajuda. Depois, quando já escreve sozinha.",
                        TEAL, TEAL_L, etiqueta="progresso")
    larg = W - 2 * M
    # legenda
    y = topo - 8 * mm
    texto(c, M, y, "COMO MARCAR:", 8.5, FONT_B, TEAL)
    xx = M + 27 * mm
    rrect(c, xx, y - 3.2 * mm, 6.5 * mm, 6 * mm, 1.5, WHITE, GREEN, 0.9)
    texto(c, xx + 2 * mm, y - 1.4 * mm, "lê", 5.6, FONT, GREEN, "c")
    texto(c, xx + 8.5 * mm, y, "= já reconhece e nomeia a letra", 7.8, FONT, INK)
    xx += 68 * mm
    rrect(c, xx, y - 3.2 * mm, 9 * mm, 6 * mm, 1.5, WHITE, BLUE, 0.9)
    texto(c, xx + 4.5 * mm, y - 1.4 * mm, "escr.", 5.4, FONT, BLUE, "c")
    texto(c, xx + 11 * mm, y, "= já escreve sozinha", 7.8, FONT, INK)

    y -= 9 * mm
    cols = 7
    cw = larg / cols
    ch = 32 * mm
    for i, L in enumerate(ORDEM):
        col, row = i % cols, i // cols
        x = M + col * cw
        yy = y - row * ch
        c_cor = PALETA[i % 7]
        rrect(c, x + 1 * mm, yy - ch + 3 * mm, cw - 2 * mm, ch - 5 * mm, 6,
              WHITE, c_cor, 1.1)
        texto(c, x + cw / 2, yy - 14 * mm, L, 24, FONT_B, c_cor, "c")
        texto(c, x + cw / 2, yy - 20 * mm, L.lower(), 12, FONT_B, SOFT, "c")
        # duas caixinhas: lê / escreve
        for k, (leg, cor) in enumerate((("lê", GREEN), ("escr.", BLUE))):
            bx = x + 4 * mm + k * (cw - 8 * mm) / 2
            rrect(c, bx, yy - ch + 6.4 * mm, (cw - 8 * mm) / 2 - 1.4 * mm, 5.4 * mm,
                  2, WHITE, HexColor("#C9CDD4"), 0.7)
            texto(c, bx + ((cw - 8 * mm) / 2 - 1.4 * mm) / 2, yy - ch + 8 * mm,
                  leg, 6, FONT, SOFT, "c")
    y2 = y - 4 * ch - 2 * mm
    h = max(28 * mm, y2 - M - 4 * mm)
    rrect(c, M, M + 4 * mm, larg, h, 10, AMBER_L, None)
    texto(c, M + 5 * mm, y2 - 8 * mm, "COMEMORE CADA LINHA COMPLETA", 9, FONT_B, AMBER)
    paragrafo(c, M + 5 * mm, y2 - 14 * mm, larg - 10 * mm,
              "Não espere as 26 letras para comemorar. Cada coluna completa já merece um "
              "elogio grande: “Você já conhece 7 letras!”. Para a criança com TDAH, o "
              "progresso visível é o que sustenta a vontade de continuar.", 8.6, FONT, INK)
    # quadro de quantas letras
    yy = y2 - 30 * mm
    texto(c, M + 5 * mm, yy, "QUANTAS LETRAS EU JÁ SEI?", 8.5, FONT_B, AMBER)
    for k in range(4):
        cx = M + 12 * mm + k * 34 * mm
        rrect(c, cx, yy - 12 * mm, 26 * mm, 9 * mm, 3, WHITE, HexColor("#D9C7A2"), 0.9)
        texto(c, cx + 6 * mm, yy - 9.4 * mm, "letras", 7, FONT, SOFT)
    rodape(c, pag, total)


