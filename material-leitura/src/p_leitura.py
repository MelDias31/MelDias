# -*- coding: utf-8 -*-
"""Leitura guiada, frases, pequenos textos e escrita."""
from reportlab.lib.units import mm

from base import *
from contornos import desenhar_texto, medir
from figuras import emoji, checkbox, bolinhas_progresso
from conteudo import FRASES


def cartao_frase(c, texto_frase, fig, x, y, w, h, cor_idx=0, tamanho=16,
                 mostrar_figura=True, linha_escrita=False):
    cor, cor_l = PALETA[cor_idx % 7], PALETA_L[cor_idx % 7]
    rrect(c, x, y, w, h, 12, WHITE, cor, 1.4)
    xa = x + 5 * mm
    if mostrar_figura and fig:
        emoji(c, fig, x + 15 * mm, y + h - 17 * mm, 19 * mm, cor)
        xa = x + 28 * mm
    # sílabas coloridas alternando
    linhas = texto_frase.split("\n")
    yy = y + h - 11 * mm
    for ln in linhas:
        px = xa
        for i, palavra in enumerate(ln.split(" ")):
            if not palavra:
                continue
            partes = _dividir_silabas(palavra)
            for j, (ped, tipo) in enumerate(partes):
                cor_p = cor if j % 2 == 0 else INK
                if palavra in ("É", "E") or len(palavra) <= 2:
                    cor_p = SOFT
                px += desenhar_texto(c, ped, px, yy, tamanho, "solido", cor_p,
                                     nome_fonte="Andika-Bold.ttf")
            px += tamanho * 0.30
        yy -= tamanho * 1.45
    if linha_escrita:
        yy -= 2 * mm
        for i in range(2):
            linha(c, xa, yy - 3 * mm, x + w - 5 * mm, yy - 3 * mm,
                  HexColor("#D3DAE2"), 1.1)
            yy -= 9 * mm


VOGAIS = "AEIOUÁÉÍÓÚÂÊÔÃÕ"
_DIGRAFOS = ("CH", "LH", "NH", "QU", "GU")
_DITONGOS = ("AI", "EI", "OI", "AU", "EU", "IU", "OU", "UI", "ÃE", "ÃO", "ÕE",
             "AI", "ÃO", "ÕE", "ÃE", "ÃO", "UI", "IU")


def _dividir_silabas(palavra):
    """Divisão silábica aproximada, suficiente para colorir os pedaços."""
    import re
    m = re.match(r"^(.*?)([.,!?;:]*)$", palavra)
    nucleo, pont = m.group(1), m.group(2)
    if not nucleo:
        return [palavra]
    p = nucleo.upper()
    n = len(p)
    eh_v = [c in VOGAIS for c in p]
    # em QU/GU o U não é núcleo (qu-e-ro, gu-i-a)
    for idx in range(1, n - 1):
        if p[idx] == "U" and p[idx - 1] in "QG" and eh_v[idx + 1]:
            eh_v[idx] = False
    for idx in range(1, n - 1):
        if p[idx] == "U" and p[idx - 1] in "Q" and p[idx + 1] in "AI" and not eh_v[idx]:
            pass

    # sílabas por posição de corte
    cortes = []
    i = 0
    while i < n:
        if not eh_v[i]:
            i += 1
            continue
        # fim do núcleo vocálico (ditongo conta como um núcleo)
        j = i
        while j + 1 < n and eh_v[j + 1] and (p[j:j + 2] in _DITONGOS):
            j += 1
        # próximos consoantes
        k = j + 1
        while k < n and not eh_v[k]:
            k += 1
        cons = p[j + 1:k]
        if k < n:  # existe próxima vogal
            if len(cons) == 0:
                corte = k
            elif len(cons) == 1:
                corte = k - 1
            else:
                par = cons[:2]
                if par in ("CH", "LH", "NH", "QU", "GU"):
                    corte = j + 1
                elif par[1] in "LR" and par not in ("RR",):
                    corte = j + 1
                elif par in ("SC", "SÇ", "XC") and p[k] in "EIÉÍ":
                    corte = j + 1
                else:
                    corte = k - len(cons) + 1
            cortes.append(corte)
        i = k
    pedacos, ant = [], 0
    for c in cortes:
        if c > ant:
            pedacos.append(nucleo[ant:c])
            ant = c
    pedacos.append(nucleo[ant:])
    pedacos = [x for x in pedacos if x]
    if pont:
        pedacos[-1] += pont
    return pedacos or [palavra]


def leitura_frases(c, pag, total, item):
    titulo, frases = item
    idx = [t for t, _ in FRASES].index(titulo)
    cor, cor_l = PALETA[idx % 7], PALETA_L[idx % 7]
    fundo(c)
    topo = faixa_titulo(c, "LEIA A FRASE", titulo, cor, cor_l,
                        etiqueta="leitura guiada")
    larg = W - 2 * M

    rodape_txt = 22 * mm
    y = topo - 5 * mm
    limite = M + rodape_txt + 4 * mm
    itens = frases[:4]
    alt = min(46 * mm, (y - limite) / len(itens) - 4 * mm)
    for i, (frase, simples, fig) in enumerate(itens):
        h = alt
        rrect(c, M, y - h, larg, h, 12, WHITE, cor, 1.4)
        xa = M + 6 * mm
        if fig:
            emoji(c, fig, M + 15 * mm, y - 17 * mm, 19 * mm, cor)
            xa = M + 28 * mm
        # sílabas coloridas
        yy = y - 12 * mm
        for ln in frase.split("\n"):
            px = xa
            for palavra in ln.split(" "):
                if not palavra:
                    continue
                for j, sil in enumerate(_dividir_silabas(palavra)):
                    cor_p = cor if j % 2 == 0 else INK
                    if len(palavra) <= 2:
                        cor_p = SOFT
                    px += desenhar_texto(c, sil, px, yy, 18, "solido", cor_p,
                                         nome_fonte="Andika-Bold.ttf")
                px += 5
            yy -= 20
        # linhas de treino
        yy = y - h + 20 * mm
        for k in range(2):
            linha(c, xa, yy, M + larg - 6 * mm, yy, HexColor("#D3DAE2"), 1.1)
            yy -= 9 * mm
        texto(c, M + larg - 6 * mm, y - h + 4 * mm, "leia 2 vezes e marque:", 7.5,
              FONT, SOFT, "r")
        for k in range(2):
            checkbox(c, M + larg - 18 * mm + k * 8 * mm, y - h + 7 * mm, 6 * mm,
                     HexColor("#B9C0C9"), 1)
        y -= h + 4 * mm

    # rodapé instrução
    rrect(c, M, M + 3 * mm, larg, 17 * mm, 8, AMBER_L, None)
    texto(c, M + 5 * mm, M + 13 * mm, "COMO LER:", 8.5, FONT_B, AMBER)
    paragrafo(c, M + 26 * mm, M + 13 * mm, larg - 31 * mm,
              "Aponte cada sílaba com o dedo e leia devagar. Depois leia junto com a "
              "criança e, por último, deixe ela ler sozinha. Adivinhar pelo desenho "
              "também vale — faz parte do caminho.", 8.5, FONT, INK)
    rodape(c, pag, total)


def leitura_textos(c, pag, total):
    """Textos curtos com figuras de apoio (para quem já lê palavras)."""
    fundo(c)
    topo = faixa_titulo(c, "PRIMEIRAS HISTÓRIAS", "Leia junto. Uma linha por vez.",
                        GREEN, GREEN_L, etiqueta="leitura")
    textos = [
        ("O GATO DE BOTAS", "🐱", [
            "O gato subiu na mesa.",
            "Ele viu o peixe no prato.",
            "O gato pulou e o prato caiu.",
            "A menina riu muito.",
        ]),
        ("A BOLA AZUL", "⚽", [
            "Ana tem uma bola azul.",
            "Ela joga a bola para o pai.",
            "O pai chuta a bola longe.",
            "A bola caiu no jardim.",
        ]),
        ("O PATO NO LAGO", "🦆", [
            "O pato nada no lago.",
            "Ele vê um peixe pequeno.",
            "O peixe foge bem rápido.",
            "O pato mergulha de novo.",
        ]),
    ]
    y = topo - 4 * mm
    for titulo, fig, linhas in textos:
        h = 62 * mm
        rrect(c, M, y - h, W - 2 * M, h, 10, WHITE, GREEN, 1.2)
        emoji(c, fig, M + 12 * mm, y - 9 * mm, 12 * mm, GREEN)
        texto(c, M + 21 * mm, y - 9 * mm, titulo, 12.5, FONT_B, GREEN)
        yy = y - 22 * mm
        for i, ln in enumerate(linhas):
            desenhar_texto(c, ln, M + 8 * mm, yy, 12.5, "solido", INK)
            checkbox(c, W - M - 11 * mm, yy - 1 * mm, 5.5 * mm,
                     HexColor("#B9C0C9"), 1)
            yy -= 9.2 * mm
        texto(c, W - M - 25 * mm, y - h + 4 * mm, "marque cada linha lida", 7.5,
              FONT, SOFT, "r")
        y -= h + 4 * mm
    rodape(c, pag, total)


def escrita(c, pag, total):
    """Folha pautada grande para treinar palavras ditadas."""
    fundo(c)
    topo = faixa_titulo(c, "FOLHA DE ESCRITA", "Use esta folha para o ditado das palavras.",
                        BLUE, BLUE_L, etiqueta="escrita")
    y = topo - 8 * mm
    alt = 22 * mm
    n = int((y - (M + 6 * mm)) / (alt + 4 * mm))
    for i in range(n):
        pauta(c, M, y - alt, W - 2 * M, alt, HexColor("#D5DCE5"))
        texto(c, M - 3 * mm, y - alt - 2 * mm, "", 8, FONT, SOFT)
        y -= alt + 4 * mm
    rodape(c, pag, total)


def ditado_figuras(c, pag, total):
    """Figura + quadro para escrever a palavra (ditar pelo desenho)."""
    from conteudo import NIVEIS_PALAVRAS
    fundo(c)
    topo = faixa_titulo(c, "DITADO DE FIGURAS", "Olhe o desenho e escreva a palavra.",
                        CORAL, CORAL_L, etiqueta="escrita")
    itens = [p for _, lista in NIVEIS_PALAVRAS for p in lista][:12]
    larg = W - 2 * M
    cols = 3
    cw = larg / cols
    ch = (topo - (M + 8 * mm)) / 4
    for i, (pal, fig) in enumerate(itens):
        col, row = i % cols, i // cols
        x = M + col * cw
        y = topo - row * ch
        rrect(c, x + 1.5 * mm, y - ch + 2 * mm, cw - 3 * mm, ch - 4 * mm, 8,
              WHITE, HexColor("#DDE3EA"), 1)
        emoji(c, fig, x + cw / 2, y - 18 * mm, 17 * mm, CORAL)
        # pauta para a palavra
        pauta(c, x + 6 * mm, y - ch + 12 * mm, cw - 12 * mm, 10 * mm,
              HexColor("#DCE2E9"))
    rodape(c, pag, total)


# ------------------------------------------------------------------ extras
def capa(c, pag, total):
    fundo(c, CREAM)
    c.setFillColor(PURPLE)
    c.rect(0, H - 88 * mm, W, 88 * mm, stroke=0, fill=1)
    texto(c, W / 2, H - 30 * mm, "LEITURA E ESCRITA", 30, FONT_B, WHITE, "c")
    texto(c, W / 2, H - 40 * mm, "da sílaba à frase, sem pressa", 12, FONT, PURPLE_L, "c")
    for i, e in enumerate(["🦆", "🐟", "🌙"]):
        emoji(c, e, W / 2 + (i - 1) * 28 * mm, H - 62 * mm, 20 * mm, WHITE)

    y = H - 100 * mm
    texto(c, W / 2, y, "CINCO NÍVEIS DE LEITURA", 13, FONT_B, INK, "c")
    texto(c, W / 2, y - 7 * mm,
          "Comece no nível 1. Só avance quando o nível atual estiver fácil.", 9.5,
          FONT, SOFT, "c")
    niveis = [
        ("1", "Sílabas soltas", "BA, BE, BI...", TEAL),
        ("2", "Palavras de 2 sílabas", "GATO, BOLA, CASA", CORAL),
        ("3", "Frase curta", "O GATO É PRETO.", BLUE),
        ("4", "Frase com ação", "O MENINO PULA.", PURPLE),
        ("5", "Duas frases", "O GATO SOBE. ELE QUER O PEIXE.", AMBER),
    ]
    yy = y - 18 * mm
    for num, tit, ex, cor in niveis:
        rrect(c, M + 12 * mm, yy - 16 * mm, W - 2 * M - 24 * mm, 16 * mm, 8,
              WHITE, HexColor("#E3DDEB"), 1)
        numero_passo(c, M + 22 * mm, yy - 8 * mm, num, 5.0, WHITE, cor, 8)
        texto(c, M + 31 * mm, yy - 6.6 * mm, tit, 10.5, FONT_B, INK)
        texto(c, W - M - 18 * mm, yy - 6.6 * mm, ex, 8.5, FONT, SOFT, "r")
        yy -= 21 * mm

    # como usar
    yb = yy + 21 * mm - 16 * mm - 7 * mm
    rrect(c, M + 12 * mm, M + 12 * mm, W - 2 * M - 24 * mm, yb - M - 12 * mm, 9,
          AMBER_L, None)
    texto(c, M + 20 * mm, yb - 9 * mm, "ANTES DE COMEÇAR", 8.5, FONT_B, AMBER)
    for i, t in enumerate([
            "Leia junto, apontando cada sílaba com o dedo.",
            "Deixe ela adivinhar pelo desenho: faz parte do caminho.",
            "Elogie o esforço, não o acerto.",
            "Termine sempre antes do cansaço."]):
        texto(c, M + 20 * mm, yb - 18.5 * mm - i * 6.4 * mm, "•  " + t, 8.8, FONT, INK)
    rodape(c, pag, total)


def textos_2(c, pag, total):
    fundo(c)
    topo = faixa_titulo(c, "MAIS HISTÓRIAS", "Leia uma linha por vez, apontando com o dedo.",
                        GREEN, GREEN_L, etiqueta="leitura")
    textos = [
        ("O DADO DA SORTE", "🎲", [
            "Bia achou um dado na rua.",
            "Ela jogou o dado no chão.",
            "Saiu o número seis!",
            "Bia pulou de alegria.",
        ]),
        ("A FLOR DO QUINTAL", "🌸", [
            "No quintal nasceu uma flor.",
            "Ela é rosa e cheira bem.",
            "A abelha veio visitar.",
            "A flor ficou feliz.",
        ]),
        ("O CACHORRO SOLTO", "🐶", [
            "O cachorro fugiu do portão.",
            "Ele correu atrás do gato.",
            "O gato subiu na árvore.",
            "O cachorro ficou latindo.",
        ]),
    ]
    y = topo - 4 * mm
    for titulo, fig, linhas in textos:
        h = 62 * mm
        rrect(c, M, y - h, W - 2 * M, h, 10, WHITE, GREEN, 1.2)
        emoji(c, fig, M + 12 * mm, y - 9 * mm, 12 * mm, GREEN)
        texto(c, M + 21 * mm, y - 9 * mm, titulo, 12.5, FONT_B, GREEN)
        yy = y - 22 * mm
        for i, ln in enumerate(linhas):
            desenhar_texto(c, ln, M + 8 * mm, yy, 12.5, "solido", INK)
            checkbox(c, W - M - 11 * mm, yy - 1 * mm, 5.5 * mm,
                     HexColor("#B9C0C9"), 1)
            yy -= 9.2 * mm
        texto(c, W - M - 25 * mm, y - h + 4 * mm, "marque cada linha lida", 7.5,
              FONT, SOFT, "r")
        y -= h + 4 * mm
    rodape(c, pag, total)


def ditado_figuras_2(c, pag, total):
    from conteudo import NIVEIS_PALAVRAS
    fundo(c)
    topo = faixa_titulo(c, "DITADO DE FIGURAS 2", "Olhe o desenho e escreva a palavra.",
                        CORAL, CORAL_L, etiqueta="escrita")
    itens = [p for _, lista in NIVEIS_PALAVRAS for p in lista]
    itens = itens[12:24] if len(itens) > 24 else itens[8:20]
    larg = W - 2 * M
    cols = 3
    cw = larg / cols
    ch = (topo - (M + 8 * mm)) / 4
    for i, (pal, fig) in enumerate(itens[:12]):
        col, row = i % cols, i // cols
        x = M + col * cw
        y = topo - row * ch
        rrect(c, x + 1.5 * mm, y - ch + 2 * mm, cw - 3 * mm, ch - 4 * mm, 8,
              WHITE, HexColor("#DDE3EA"), 1)
        emoji(c, fig, x + cw / 2, y - 18 * mm, 17 * mm, CORAL)
        pauta(c, x + 6 * mm, y - ch + 12 * mm, cw - 12 * mm, 10 * mm,
              HexColor("#DCE2E9"))
    rodape(c, pag, total)


def escrita(c, pag, total, indice=0):
    fundo(c)
    titulos = ["FOLHA DE ESCRITA — PALAVRAS", "FOLHA DE ESCRITA — SÍLABAS",
               "FOLHA DE ESCRITA — FRASES", "FOLHA DE ESCRITA — MEU NOME"]
    subt = ["Copie as palavras do quadro e depois escreva as que o adulto ditar.",
            "Treine as sílabas da semana: copie e depois escreva de memória.",
            "Copie as frases e depois escreva a que o adulto ditar.",
            "Escreva seu nome, do começo ao fim, e depois o nome de quem você ama."]
    topo = faixa_titulo(c, titulos[indice], subt[indice], BLUE, BLUE_L, etiqueta="escrita")

    larg = W - 2 * M
    y = topo - 7 * mm

    # faixa de apoio: o que copiar
    banco = {
        0: ["BOLA", "CASA", "GATO", "PATO", "LUA", "MALA", "UVA", "DADO"],
        1: ["BA", "BE", "BI", "BO", "BU", "CA", "CO", "CU"],
        2: ["O GATO É PRETO.", "A BOLA É AZUL.", "O SOL É AMARELO."],
        3: ["", "", ""],
    }[indice]
    if indice == 3:
        # caixa do nome para completar
        rrect(c, M, y - 26 * mm, larg, 26 * mm, 10, BLUE_L, None)
        texto(c, M + 6 * mm, y - 9 * mm, "MEU NOME COMPLETO É:", 9, FONT_B, BLUE)
        linha(c, M + 6 * mm, y - 17 * mm, W - M - 6 * mm, y - 17 * mm,
              HexColor("#9AA3AF"), 1.2)
        texto(c, M + 6 * mm, y - 23 * mm,
              "Escreva com letra grande. Depois conte quantas letras tem seu nome.", 8,
              FONT, SOFT)
        y -= 31 * mm
    else:
        h = 16 * mm if indice != 2 else 18 * mm
        rrect(c, M, y - h, larg, h, 8, BLUE_L, None)
        texto(c, M + 5 * mm, y - 6 * mm, "COPIE DAQUI:", 7.5, FONT_B, BLUE)
        xx = M + 32 * mm
        yy = y - 11 * mm
        for item in banco:
            if indice == 2:
                texto(c, M + 5 * mm, yy, item, 9, FONT_B, INK)
                yy -= 4.6 * mm
            else:
                w = largura(item, 11, FONT_B) + 7 * mm
                if xx + w > W - M - 5 * mm:
                    xx = M + 32 * mm
                    yy -= 6 * mm
                texto(c, xx, yy, item, 11, FONT_B, INK)
                xx += w
        y -= h + 4 * mm

    # linhas de escrita
    n = 7 if indice != 3 else 6
    passo = (y - (M + 10 * mm)) / n
    alt_l = min(21 * mm, passo - 6 * mm)
    for i in range(n):
        base = y - (i + 1) * passo + (passo - alt_l) / 2
        pauta(c, M, base, larg, alt_l, HexColor("#D5DCE5"))
    if indice == 3:
        texto(c, M, M + 6 * mm,
              "Dica: escreva o nome com letras grandes e coloridas e cole na parede do quarto.",
              7.6, FONT_I, SOFT)
    rodape(c, pag, total)


def autoavaliacao(c, pag, total):
    fundo(c)
    topo = faixa_titulo(c, "COMO EU ME SENTI HOJE?", "Para a criança marcar com um X ou pintar.",
                        AMBER, AMBER_L, etiqueta="socioemocional")
    larg = W - 2 * M
    y = topo - 12 * mm
    linhas = ["Foi fácil?", "Foi divertido?", "Quero repetir?", "Precisei de ajuda?"]
    emojis = ["😀", "🙂", "😐", "😟"]

    nota = ("Perguntar como ela se sentiu é parte do método. Criança com TDAH costuma "
            "associar tarefa a fracasso; se ela marcar carinha triste, mude o formato "
            "amanhã (mais jogo, menos folha) e reduza o tempo. O objetivo é manter o "
            "vínculo — sem vínculo não há aprendizagem.")
    linhas_nota = quebrar(nota, larg - 12 * mm, 8.8, FONT)
    caixa_h = 10 * mm + len(linhas_nota) * 4.8 * mm + 5 * mm
    caixa_y = M + 8 * mm
    caixa_topo = caixa_y + caixa_h

    passo = (y - (caixa_topo + 8 * mm)) / 4
    h = passo - 6 * mm
    for i, pergunta in enumerate(linhas):
        yy = y - i * passo
        rrect(c, M, yy - h, larg, h, 9, WHITE, LINE, 1)
        texto(c, M + 6 * mm, yy - h / 2 - 4, pergunta, 11.5, FONT_B, INK)
        for j, e in enumerate(emojis):
            cx = W - M - 14 * mm - (3 - j) * 17 * mm
            emoji(c, e, cx, yy - h / 2 + 1 * mm, 10 * mm, SOFT)
            checkbox(c, cx - 2.5 * mm, yy - h + 5 * mm, 5 * mm, HexColor("#B9C0C9"), 1)

    rrect(c, M, caixa_y, larg, caixa_h, 10, PINK_L, None)
    texto(c, M + 6 * mm, caixa_topo - 8 * mm, "PARA O ADULTO", 9, FONT_B, PINK)
    for k, ln in enumerate(linhas_nota):
        texto(c, M + 6 * mm, caixa_topo - 15 * mm - k * 4.8 * mm, ln, 8.8, FONT, INK)
    rodape(c, pag, total)
