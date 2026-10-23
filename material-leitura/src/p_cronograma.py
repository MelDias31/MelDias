# -*- coding: utf-8 -*-
"""Cronograma de 4 semanas: o mapa dia a dia do primeiro mês.

Caderno 06. Não traz folha de atividade: diz qual folha usar em cada dia,
em que ordem imprimir e o que observar. Foi escrito para a mãe, não para a
criança.
"""
from base import (W, H, M, mm, INK, SOFT, LINE, WHITE, TEAL, TEAL_L, CORAL,
                  CORAL_L, AMBER, AMBER_L, BLUE, BLUE_L, PURPLE, PURPLE_L,
                  GREEN, GREEN_L, PINK, PINK_L, HexColor, FONT, FONT_B, FONT_I,
                  texto, quebrar, largura, paragrafo, paragrafo_altura, rrect,
                  linha, faixa_titulo, rodape, fundo, numero_passo, pauta)
from figuras import emoji, checkbox
from conteudo import ALFABETO

CINZA = HexColor("#F7F9FB")
TRACO = HexColor("#E4E7EC")
BORDA = HexColor("#B9C0C9")


# --------------------------------------------------------------- utilidades
def _chips(c, x, y, itens, cor, cor_l, larg_max, size=8.2, h=5.4 * mm):
    """Desenha os 'chips' em linha, quebrando quando falta espaço.

    Devolve o y da última linha usada.
    """
    cx, cy = x, y
    for t in itens:
        w = largura(t, size, FONT_B) + 7 * mm
        if cx + w > x + larg_max and cx > x:
            cx, cy = x, cy - (h + 1.3 * mm)
        rrect(c, cx, cy - h + 1.2 * mm, w, h, h / 2, cor_l, None)
        texto(c, cx + w / 2, cy - h / 2 + 0.6 * mm, t, size, FONT_B, cor, "c")
        cx += w + 1.6 * mm
    return cy


def _titulo_bloco(c, x, y, txt, cor):
    texto(c, x, y, txt, 9.4, FONT_B, cor)


def _lista(c, itens, x, y, larg, cor, size=8.9, cor_marca=None):
    """Lista com bolinha; devolve o y depois do último item."""
    cor_marca = cor_marca or cor
    for t in itens:
        c.setFillColor(cor_marca)
        c.circle(x + 1.2 * mm, y + 1.0 * mm, 1.0 * mm, stroke=0, fill=1)
        linhas = quebrar(t, larg - 6 * mm, size, FONT)
        for j, ln in enumerate(linhas):
            texto(c, x + 5 * mm, y - j * 4.1 * mm, ln, size, FONT, INK)
        y -= len(linhas) * 4.1 * mm + 2.2 * mm
    return y


def _caixa_lista(c, x, y, larg, alt, titulo, itens, cor, cor_l, size=8.9):
    rrect(c, x, y - alt, larg, alt, 9, cor_l, None)
    _titulo_bloco(c, x + 5 * mm, y - 7.4 * mm, titulo, cor)
    _lista(c, itens, x + 6 * mm, y - 15.4 * mm, larg - 10 * mm, cor, size)


def _altura_lista(itens, larg, size=8.9):
    return sum(len(quebrar(t, larg, size, FONT)) * 4.1 + 2.2 for t in itens) * mm


# ------------------------------------------------------------------- dados
SEMANAS = [
    dict(
        letras=["A", "E"], cor=TEAL, cor_l=TEAL_L,
        sub="As duas primeiras vogais. Cinco dias curtos e dois dias leves.",
        imprimir=["01 p. 3", "01 p. 29", "01 p. 4", "01 p. 30", "01 p. 58"],
        dias=[
            ("SEG", "Letra A — colorir e traçar",
             "Comece pelo ponto verde e siga a ordem 1, 2, 3 dos traços.", "01 p. 3"),
            ("TER", "Letra A — caça-letra e minúscula",
             "Ache o A entre as parecidas; depois cubra o a pontilhado.", "01 p. 3 e 29"),
            ("QUA", "Letra E — colorir e traçar",
             "O E é uma reta com três braços. Faça um braço por vez.", "01 p. 4"),
            ("QUI", "Letra E — caça-letra e minúscula",
             "Compare o E grande com o e pequeno: mesmo som, outro desenho.", "01 p. 4 e 30"),
            ("SEX", "Jogo: bingo de letras",
             "Use só as cinco vogais. Ela canta e você marca; depois troca.", "01 p. 58"),
            ("SÁB", "Revisão leve: mural do alfabeto",
             "Dois minutos apontando: “acha o A”, “acha o E”.", "01 p. 56 e 57"),
            ("DOM", "Descanso",
             "Nenhuma folha hoje. Descanso também faz parte do método.", "—"),
        ],
        observar=[
            "Ela olhou a folha e começou sem você mandar?",
            "Acertou o traço do A na terceira tentativa, sem ajuda?",
            "Achou o A ou o E em outra palavra (nome, placa, embalagem)?",
        ],
        travar=[
            "Confunde A com E? Cante “A de abelha, E de elefante” e aponte os dois.",
            "Cansa em 5 minutos? Faça só a letra grande e pare. Amanhã recomeça dela.",
            "Ainda não reconhece as duas? Repita a semana inteira. Repetir é o método.",
        ],
    ),
    dict(
        letras=["I", "O"], cor=BLUE, cor_l=BLUE_L,
        sub="Fechando as vogais. O jogo da semana usa figura e palavra.",
        imprimir=["01 p. 5", "01 p. 31", "01 p. 6", "01 p. 32", "04 p. 3 e 4"],
        dias=[
            ("SEG", "Letra I — colorir e traçar",
             "O I é uma reta com chapéu e pé. Desça devagar, sem tirar o lápis.", "01 p. 5"),
            ("TER", "Letra I — caça-letra e minúscula",
             "O i pequeno é a reta com um pinguinho em cima.", "01 p. 5 e 31"),
            ("QUA", "Letra O — colorir e traçar",
             "O O começa no topo, roda e fecha. Redondo, sem ponta.", "01 p. 6"),
            ("QUI", "Letra O — caça-letra e minúscula",
             "Cuidado: o O não é o número 0. Mostre os dois lado a lado.", "01 p. 6 e 32"),
            ("SEX", "Jogo: memória figura + palavra",
             "Você lê a palavra em voz alta. Ela pode achar pela figura: está certo.", "04 p. 3 e 4"),
            ("SÁB", "Caça de vogais em revista",
             "Achar A, E, I, O em embalagem ou revista e colar num cartaz.", "revista"),
            ("DOM", "Descanso",
             "Nenhuma folha hoje. Se ela pedir, pode jogar o bingo de novo.", "—"),
        ],
        observar=[
            "Ela já nomeia A, E, I e O sem você falar primeiro?",
            "Escolhe a carta certa no jogo da memória, mesmo sem ler?",
            "Percebeu que o O e o número 0 são diferentes?",
        ],
        travar=[
            "Mistura I e O? Deixe só uma folha na mesa. Letra a mais é distração.",
            "O jogo é difícil? Use 6 pares (3 figuras e 3 palavras), não os 12.",
            "Se A e E ainda não estão firmes, repita a semana 1 antes de seguir.",
        ],
    ),
    dict(
        letras=["U", "M"], cor=PURPLE, cor_l=PURPLE_L,
        sub="A última vogal e a primeira consoante. Aqui começa a juntar letras.",
        imprimir=["01 p. 7", "01 p. 33", "01 p. 8", "01 p. 34", "02 p. 9",
                  "02 p. 26", "04 p. 9"],
        dias=[
            ("SEG", "Letra U — colorir e traçar",
             "O U é um copo sem tampa. Desça, curve e suba.", "01 p. 7"),
            ("TER", "Letra U — caça-letra e minúscula",
             "O u pequeno é o mesmo desenho, menor.", "01 p. 7 e 33"),
            ("QUA", "Letra M + família do M",
             "MA ME MI MO MU: junte o M com cada vogal, devagar, falando junto.", "01 p. 8 · 02 p. 9"),
            ("QUI", "Letra M minúscula",
             "Cubra o m pontilhado e copie MA ME MI MO MU uma vez.", "01 p. 34 · 02 p. 9"),
            ("SEX", "Jogo: ligue a figura à palavra",
             "Ela pode ligar pela primeira letra. Leia a palavra junto.", "04 p. 9"),
            ("SÁB", "Escada das palavras",
             "Só as palavras de 2 sílabas, com o dedo embaixo. Uma vez cada.", "02 p. 26"),
            ("DOM", "Descanso",
             "Nenhuma folha hoje. Semana que vem entram o P e o B.", "—"),
        ],
        observar=[
            "Ela leu MA, ME, MI sozinha, sem você soprar o som?",
            "Juntou M + A com o dedo: toca no M, toca no A, desliza?",
            "Reconheceu uma palavra do jogo (MALA, MOLA, MAMÃE)?",
        ],
        travar=[
            "Se o M ainda não colou, fique 3 dias só na letra grande. Sem pressa.",
            "Não consegue juntar M + A? Faça com o dedo antes do lápis, 5 vezes.",
            "Chorou na escada das palavras? Volte ao jogo e deixe a leitura para depois.",
        ],
    ),
    dict(
        letras=["P", "B"], cor=AMBER, cor_l=AMBER_L,
        sub="Duas letras que se parecem de perto. A semana fecha com as primeiras frases.",
        imprimir=["01 p. 9", "01 p. 35", "01 p. 10", "01 p. 36", "02 p. 11",
                  "02 p. 2", "03 p. 2", "04 p. 12", "05 p. 8"],
        dias=[
            ("SEG", "Letra P + família do P",
             "PA PE PI PO PU. O P tem a barriga em cima e a perna descendo.", "01 p. 9 · 02 p. 11"),
            ("TER", "Letra P minúscula",
             "A perna do p passa da linha. Cubra e escreva três vezes.", "01 p. 35"),
            ("QUA", "Letra B + família do B",
             "BA BE BI BO BU. O B tem duas barrigas: uma em cima, outra embaixo.", "01 p. 10 · 02 p. 2"),
            ("QUI", "Letra B minúscula",
             "Cubra o b e copie BA BE BI BO BU. Depois compare b com d.", "01 p. 36 · 02 p. 2"),
            ("SEX", "As primeiras frases + caça-palavras",
             "Leia junto, uma linha por vez. Depois ache as palavras escondidas.", "03 p. 2 · 04 p. 12"),
            ("SÁB", "Revisão e certificado",
             "Se ela chegou até aqui, entregue o certificado. Elogie o esforço.", "05 p. 8"),
            ("DOM", "Descanso",
             "Um mês de trabalho. Olhe o mapa das letras e comemore com ela.", "01 p. 59"),
        ],
        observar=[
            "Ela diferencia P de B ao escrever, sem você avisar?",
            "Leu BÁ, BÉ ou “O BOI” sozinha na página de frases?",
            "Achou as palavras no caça-palavras sem desistir?",
        ],
        travar=[
            "Troca p e b? Volte a “Letras que se parecem” (01 p. 55) e faça a brincadeira do espelho.",
            "A frase é longa demais? Cubra o resto da folha e deixe só uma linha.",
            "Se B ainda não está firme, faça a semana 4 de novo só com o B antes do D.",
        ],
    ),
]

PROXIMAS = [("D", "02 p. 4"), ("T", "02 p. 14"), ("L", "02 p. 8"), ("C", "02 p. 3"),
            ("S", "02 p. 13"), ("R", "02 p. 12"), ("N", "02 p. 10"), ("F", "02 p. 5"),
            ("V", "02 p. 15"), ("G", "02 p. 6"), ("J", "02 p. 7"), ("Z", "02 p. 16"),
            ("X", "—"), ("Q", "—"), ("H", "—"), ("K", "—"), ("W", "—"), ("Y", "—")]

FIXOS = [
    ("01 p. 1 e 2", "Capa e “Como usar este caderno”", "antes de começar"),
    ("05 p. 1 a 6", "Guia do adulto, rotina, quadro e registro", "antes de começar"),
    ("05 p. 7", "Cartões de pausa e elogio (recortar)", "semana 1"),
    ("01 p. 55", "Letras que se parecem (ler antes)", "semana 1"),
    ("01 p. 56 e 57", "Mural do alfabeto (parede)", "semana 1"),
    ("01 p. 59", "Mapa das 26 letras (parede)", "semana 1"),
    ("01 p. 58", "Bingo de letras (recortar)", "semana 1"),
    ("04 p. 3 e 4", "Jogo da memória (recortar)", "semana 2"),
    ("05 p. 8", "Certificado de leitura", "semana 4"),
]

NOMES = {
    "01 p. 1 e 2": "Capa e instruções do caderno do alfabeto",
    "05 p. 1 a 6": "Guia do adulto, rotina, quadro e registro",
    "05 p. 7": "Cartões de pausa e elogio",
    "01 p. 55": "Letras que se parecem",
    "01 p. 56 e 57": "Mural do alfabeto (2 partes)",
    "01 p. 59": "Mapa das 26 letras",
    "01 p. 58": "Bingo de letras",
    "04 p. 3 e 4": "Jogo da memória (2 partes)",
    "01 p. 3": "Letra A — colorir, traçar e caçar",
    "01 p. 29": "Letra A — maiúscula e minúscula",
    "01 p. 4": "Letra E — colorir, traçar e caçar",
    "01 p. 30": "Letra E — maiúscula e minúscula",
    "01 p. 5": "Letra I — colorir, traçar e caçar",
    "01 p. 31": "Letra I — maiúscula e minúscula",
    "01 p. 6": "Letra O — colorir, traçar e caçar",
    "01 p. 32": "Letra O — maiúscula e minúscula",
    "01 p. 7": "Letra U — colorir, traçar e caçar",
    "01 p. 33": "Letra U — maiúscula e minúscula",
    "01 p. 8": "Letra M — colorir, traçar e caçar",
    "01 p. 34": "Letra M — maiúscula e minúscula",
    "02 p. 9": "Família do M (MA ME MI MO MU)",
    "02 p. 26": "Escada das palavras",
    "04 p. 9": "Ligue a figura à palavra 1",
    "01 p. 9": "Letra P — colorir, traçar e caçar",
    "01 p. 35": "Letra P — maiúscula e minúscula",
    "01 p. 10": "Letra B — colorir, traçar e caçar",
    "01 p. 36": "Letra B — maiúscula e minúscula",
    "02 p. 11": "Família do P (PA PE PI PO PU)",
    "02 p. 2": "Família do B (BA BE BI BO BU)",
    "03 p. 2": "Leia a frase — nível 1",
    "04 p. 12": "Caça-palavras 1",
    "05 p. 8": "Certificado de leitura",
}


def _grupos():
    """Lista de impressão sem repetir folha. Devolve grupos e nº de itens."""
    vistos = set()
    total = 0
    grupos = []
    primeiros = []
    for arq, desc, quando in FIXOS:
        primeiros.append((arq, desc, quando))
        vistos.add(arq)
        total += 1
    grupos.append(("UMA VEZ SÓ — ANTES DE COMEÇAR", primeiros, BLUE, BLUE_L))
    for i, s in enumerate(SEMANAS):
        itens = []
        for t in s["imprimir"]:
            if t == "revista":
                itens.append(("revista", "Revista ou embalagem velha (não imprimir)",
                              f"semana {i + 1}"))
                continue
            if t in vistos:
                continue
            vistos.add(t)
            total += 1
            itens.append((t, NOMES.get(t, ""), f"semana {i + 1}"))
        grupos.append((f"SEMANA {i + 1} — LETRAS {' e '.join(s['letras'])}",
                       itens, s["cor"], s["cor_l"]))
    return grupos, total


TOTAL_FOLHAS = _grupos()[1]


# -------------------------------------------------------------------- capa
def capa(c, pag, total):
    fundo(c)
    topo = faixa_titulo(c, "CRONOGRAMA DE 4 SEMANAS",
                        "O primeiro mês, dia por dia: o que fazer e o que imprimir.",
                        TEAL, TEAL_L, etiqueta="comece por aqui")
    larg = W - 2 * M
    y = topo - 5 * mm

    rrect(c, M, y - 22 * mm, larg, 22 * mm, 10, CINZA, LINE, 1)
    paragrafo(c, M + 6 * mm, y - 8 * mm, larg - 12 * mm,
              "Este caderno é o mapa do primeiro mês. Aqui não tem folha para a criança: "
              "tem a ordem certa das folhas e o que fazer em cada dia. As atividades estão "
              "nos cadernos 01 a 04 — a lista da página 2 diz tudo o que imprimir.",
              9.4, FONT, INK, 4.4 * mm)
    y -= 26 * mm

    # as quatro semanas
    texto(c, M, y, "AS QUATRO SEMANAS", 10, FONT_B, TEAL)
    y -= 4 * mm
    alt = 31 * mm
    cw = (larg - 3 * 4 * mm) / 4
    for i, s in enumerate(SEMANAS):
        x = M + i * (cw + 4 * mm)
        rrect(c, x, y - alt, cw, alt, 9, s["cor_l"], None)
        texto(c, x + cw / 2, y - 7 * mm, f"SEMANA {i + 1}", 8.2, FONT_B, s["cor"], "c")
        texto(c, x + cw / 2, y - 17 * mm, f"{s['letras'][0]} e {s['letras'][1]}",
              19, FONT_B, s["cor"], "c")
        _, f1, _ = ALFABETO[s["letras"][0]]
        _, f2, _ = ALFABETO[s["letras"][1]]
        emoji(c, f1, x + 10 * mm, y - 24.6 * mm, 5.8 * mm, s["cor"])
        emoji(c, f2, x + cw - 10 * mm, y - 24.6 * mm, 5.8 * mm, s["cor"])
        texto(c, x + cw / 2, y - 25.8 * mm, "e", 8, FONT, SOFT, "c")
        texto(c, x + cw / 2, y - 29.4 * mm,
              ("vogais" if i < 2 else ("1ª consoante" if i == 2 else "1ªs frases")),
              7.6, FONT, SOFT, "c")
    y -= alt + 7.4 * mm

    # três regras
    rrect(c, M, y - 29 * mm, larg, 29 * mm, 10, AMBER_L, None)
    texto(c, M + 6 * mm, y - 8 * mm, "AS TRÊS REGRAS QUE NÃO MUDAM", 9.4, FONT_B, AMBER)
    regras = [
        ("10 MINUTOS", "Cronometre e pare no fim, mesmo se estiver indo bem."),
        ("UMA FOLHA", "Só a do dia na mesa. O resto fica guardado."),
        ("REPETIR", "Letra que não colou volta na semana seguinte."),
    ]
    cwr = (larg - 12 * mm) / 3
    for i, (t, d) in enumerate(regras):
        x = M + 6 * mm + i * cwr
        numero_passo(c, x + 3.4 * mm, y - 16 * mm, i + 1, r=3.3 * mm, fundo=AMBER, size=8.2)
        texto(c, x + 9 * mm, y - 15.1 * mm, t, 8.6, FONT_B, INK)
        for j, ln in enumerate(quebrar(d, cwr - 11 * mm, 8.4, FONT)):
            texto(c, x + 9 * mm, y - 20 * mm - j * 3.9 * mm, ln, 8.4, FONT, SOFT)
    y -= 33.4 * mm

    # como usar
    texto(c, M, y, "COMO USAR ESTE CADERNO", 9.8, FONT_B, BLUE)
    y -= 4.6 * mm
    passos = [
        ("1", "Imprima a lista da página 2, toda de uma vez.",
         f"São {TOTAL_FOLHAS} itens. Sai mais barato que imprimir todo dia — e não falta "
         "nada no meio da semana."),
        ("2", "Corte os jogos e monte a caixa.",
         "Bingo, memória e cartões de pausa ficam num saquinho, longe das folhas."),
        ("3", "Marque cada dia na tabela da semana.",
         "O quadradinho no fim da linha é para ela pintar. Dia pintado é dia feito."),
    ]
    for n, t, d in passos:
        linhas = quebrar(d, larg - 26 * mm, 9.0, FONT)
        alt_lin = 12.8 * mm + (len(linhas) - 1) * 4.0 * mm + 2.4 * mm
        rrect(c, M, y - alt_lin, larg, alt_lin, 8, WHITE, LINE, 1)
        numero_passo(c, M + 8 * mm, y - 7.4 * mm, n, r=3.6 * mm, fundo=BLUE, size=8.6)
        texto(c, M + 16 * mm, y - 6.5 * mm, t, 9.4, FONT_B, INK)
        for j, ln in enumerate(linhas):
            texto(c, M + 16 * mm, y - 11.4 * mm - j * 4.0 * mm, ln, 8.9, FONT, SOFT)
        y -= alt_lin + 2.6 * mm
    y -= 3.6 * mm

    # o que tem em cada arquivo
    texto(c, M, y, "O QUE TEM EM CADA ARQUIVO", 9.8, FONT_B, PURPLE)
    y -= 5.4 * mm
    arquivos = [
        ("01", "Meu alfabeto", "59 p.", "as 26 letras, maiúscula e minúscula"),
        ("02", "Sílabas e palavras", "28 p.", "famílias silábicas e leitura"),
        ("03", "Leitura e escrita", "15 p.", "frases, histórias e ditado"),
        ("04", "Jogos e fichas", "17 p.", "memória, bingo, trilha, caça"),
        ("05", "Guia do adulto", "8 p.", "rotina, quadro e certificado"),
        ("06", "Este cronograma", f"{total} p.", "o mapa dia a dia"),
    ]
    for cod, nome, pags, o_que in arquivos:
        rrect(c, M, y - 4.8 * mm, 10 * mm, 4.8 * mm, 2.2, PURPLE_L, None)
        texto(c, M + 4.6 * mm, y - 3.4 * mm, cod, 7.2, FONT_B, PURPLE, "c")
        texto(c, M + 13 * mm, y - 3.4 * mm, nome, 8.6, FONT_B, INK)
        texto(c, M + 62 * mm, y - 3.4 * mm, pags, 8.2, FONT_B, PURPLE)
        texto(c, M + 75 * mm, y - 3.4 * mm, o_que, 8.4, FONT, SOFT)
        y -= 5.9 * mm
    y -= 1.6 * mm

    para = ("Não dobre a dose nem pule etapa: repita a mesma semana. Uma letra consolidada "
            "vale mais que 26 letras vistas. Se ela faltou um dia, siga do ponto onde parou.")
    linhas = quebrar(para, larg - 12 * mm, 8.8, FONT)
    h = 12.6 * mm + (len(linhas) - 1) * 4.1 * mm + 3.6 * mm
    rrect(c, M, y - h, larg, h, 9, TEAL_L, None)
    texto(c, M + 6 * mm, y - 7.0 * mm, "SE A SEMANA DER ERRADO", 9.0, FONT_B, TEAL)
    paragrafo(c, M + 6 * mm, y - 12.8 * mm, larg - 12 * mm, para, 8.8, FONT, INK, 4.1 * mm)
    rodape(c, pag, total, "Cronograma • como usar")


# ---------------------------------------------------------- lista de impressão
def lista_impressao(c, pag, total):
    fundo(c)
    topo = faixa_titulo(c, "LISTA DE IMPRESSÃO",
                        "Marque o quadradinho depois de imprimir. Depois é só seguir o dia.",
                        BLUE, BLUE_L, etiqueta="imprimir")
    larg = W - 2 * M
    y = topo - 4 * mm

    x_arq = M + 11 * mm
    x_desc = M + 40 * mm
    x_quando = W - M - 4 * mm
    grupos, n_itens = _grupos()

    # distribui as linhas pelo espaço disponível (lista cheia ocupa a página)
    n_lin = sum(len(itens) for _, itens, _, _ in grupos)
    h_topo = 6.8 * mm * len(grupos) + 1.2 * mm * len(grupos)
    disponivel = y - (M + 52 * mm) - h_topo
    h_lin = max(4.6 * mm, min(7.0 * mm, disponivel / max(n_lin, 1)))

    for titulo, itens, cor, cor_l in grupos:
        rrect(c, M, y - 5.0 * mm, larg, 5.0 * mm, 3, cor_l, None)
        texto(c, M + 3 * mm, y - 3.5 * mm, titulo, 7.8, FONT_B, cor)
        y -= 6.8 * mm
        for arq, desc, quando in itens:
            cy = y - h_lin / 2
            checkbox(c, M + 0.5 * mm, cy - 1.6 * mm, 3.2 * mm, BORDA, 1)
            texto(c, x_arq, cy - 2.9, arq, 8.2, FONT_B, INK)
            texto(c, x_desc, cy - 2.9, desc, 8.2, FONT, INK)
            texto(c, x_quando, cy - 2.9, quando, 7.6, FONT, SOFT, "r")
            y -= h_lin
        y -= 1.2 * mm

    y -= 4.0 * mm
    linha(c, M, y + 2 * mm, W - M, y + 2 * mm, TRACO, 0.8)
    texto(c, M, y - 3.6 * mm, f"TOTAL: {n_itens} itens — cerca de 40 páginas A4", 8.4,
          FONT_B, BLUE)
    texto(c, W - M, y - 3.6 * mm, "dá para imprimir tudo em 1 hora", 7.6, FONT_I, SOFT, "r")
    y -= 9 * mm

    rrect(c, M, y - 16 * mm, larg, 16 * mm, 8, CINZA, LINE, 1)
    paragrafo(c, M + 6 * mm, y - 7 * mm, larg - 12 * mm,
              "Imprima em preto e branco. Frente e verso só quando a folha for de traço. "
              "Papel comum (75 g) serve. Guarde o que não vai usar na semana num envelope: "
              "folha à vista vira distração.", 8.8, FONT, INK, 4.1 * mm)
    rodape(c, pag, total, "Cronograma • lista de impressão")


# ------------------------------------------------------------------- semana
def semana(c, pag, total, n):
    s = SEMANAS[n]
    fundo(c)
    letras = " e ".join(s["letras"])
    topo = faixa_titulo(c, f"SEMANA {n + 1} — LETRAS {letras}",
                        s["sub"], s["cor"], s["cor_l"], etiqueta=f"semana {n + 1} de 4")
    larg = W - 2 * M
    y = topo - 4 * mm

    # o que imprimir
    texto(c, M, y, "IMPRIMIR:", 9.0, FONT_B, s["cor"])
    y = _chips(c, M + 21 * mm, y + 0.8 * mm, s["imprimir"], s["cor"], s["cor_l"],
               larg - 21 * mm) - 5.6 * mm

    # tabela dos dias
    h_cab = 6.2 * mm
    rrect(c, M, y - h_cab, larg, h_cab, 4, s["cor_l"], None)
    texto(c, M + 3 * mm, y - 4.2 * mm, "DIA", 7.6, FONT_B, s["cor"])
    texto(c, M + 20 * mm, y - 4.2 * mm, "O QUE FAZER (10 MINUTOS)", 7.6, FONT_B, s["cor"])
    texto(c, W - M - 12 * mm, y - 4.2 * mm, "FOLHA", 7.6, FONT_B, s["cor"], "r")
    y -= h_cab
    h_lin = 12.2 * mm
    for i, (dia, tarefa, dica, folha) in enumerate(s["dias"]):
        dom = dia == "DOM"
        if i % 2 == 0:
            c.setFillColor(HexColor("#FBFCFD"))
            c.rect(M, y - h_lin, larg, h_lin, stroke=0, fill=1)
        texto(c, M + 3 * mm, y - 6.4 * mm, dia, 8.4, FONT_B, SOFT if dom else s["cor"])
        texto(c, M + 20 * mm, y - 6.0 * mm, tarefa, 9.4, FONT_B, SOFT if dom else INK)
        paragrafo(c, M + 20 * mm, y - 10.2 * mm, larg - 58 * mm, dica, 8.5, FONT, SOFT,
                  3.8 * mm)
        if folha != "—":
            texto(c, W - M - 12 * mm, y - 6.0 * mm, folha, 8.4, FONT_B, s["cor"], "r")
        checkbox(c, W - M - 6.6 * mm, y - 7.0 * mm, 3.4 * mm, BORDA, 1)
        linha(c, M, y - h_lin, W - M, y - h_lin, HexColor("#EDF0F4"), 0.8)
        y -= h_lin
    y -= 4.6 * mm

    # observar / travar
    cw = (larg - 5 * mm) / 2
    alt = 7.4 * mm + _altura_lista(s["observar"], cw - 10 * mm) + 5.0 * mm
    alt2 = 7.4 * mm + _altura_lista(s["travar"], cw - 10 * mm) + 5.0 * mm
    alt = max(alt, alt2)
    _caixa_lista(c, M, y, cw, alt, "O QUE OBSERVAR (E NÃO COBRAR)", s["observar"],
                 GREEN, GREEN_L)
    _caixa_lista(c, M + cw + 5 * mm, y, cw, alt, "SE ELA TRAVAR", s["travar"],
                 CORAL, CORAL_L)
    y -= alt + 5 * mm

    # palavras da semana
    h = 33 * mm
    rrect(c, M, y - h, larg, h, 10, AMBER_L, None)
    texto(c, M + 6 * mm, y - 8 * mm, "AS PALAVRAS DESTA SEMANA", 8.8, FONT_B, AMBER)
    texto(c, M + 6 * mm, y - 14 * mm,
          "Aponte a figura, diga a palavra e só depois mostre a letra inicial.",
          8.6, FONT, INK)
    n_letras = len(s["letras"])
    cwl = (larg - 12 * mm) / n_letras
    for i, L in enumerate(s["letras"]):
        palavra, fig, _ = ALFABETO[L]
        cx = M + 6 * mm + i * cwl
        emoji(c, fig, cx + 10 * mm, y - 30 * mm, 11 * mm, AMBER)
        texto(c, cx + 21 * mm, y - 27 * mm, L, 19, FONT_B, AMBER)
        texto(c, cx + 32 * mm, y - 26.4 * mm, "de", 8.4, FONT, SOFT)
        texto(c, cx + 32 * mm, y - 31.4 * mm, palavra.upper(), 9.6, FONT_B, INK)
    y -= h + 5.5 * mm

    # anotações
    h2 = y - (M + 8 * mm)
    if h2 > 20 * mm:
        rrect(c, M, M + 8 * mm, larg, h2, 9, CINZA, LINE, 1)
        texto(c, M + 6 * mm, y - 8 * mm, "ANOTE AQUI — PARA VOCÊ, NÃO PARA ELA", 8.6,
              FONT_B, BLUE)
        texto(c, M + 6 * mm, y - 14 * mm,
              "O que funcionou, o que travou e por onde recomeçar amanhã.", 8.4, FONT, SOFT)
        ini = y - 20 * mm
        fim = M + 12 * mm
        n_lin = max(int(round((ini - fim) / (9.0 * mm))) + 1, 2)
        passo = (ini - fim) / (n_lin - 1)
        for k in range(n_lin):
            yy = ini - k * passo
            linha(c, M + 6 * mm, yy, W - M - 6 * mm, yy, HexColor("#DDE3EA"), 0.8)
    rodape(c, pag, total, f"Cronograma • semana {n + 1} de 4")


# -------------------------------------------------------------------- depois
def depois(c, pag, total):
    fundo(c)
    topo = faixa_titulo(c, "DEPOIS DA QUARTA SEMANA",
                        "O mesmo esquema continua até a última letra do alfabeto.",
                        PURPLE, PURPLE_L, etiqueta="continue")
    larg = W - 2 * M
    y = topo - 5 * mm

    rrect(c, M, y - 18 * mm, larg, 18 * mm, 10, CINZA, LINE, 1)
    paragrafo(c, M + 6 * mm, y - 7 * mm, larg - 12 * mm,
              "A quinta semana repete a estrutura da semana 4: uma letra por dia, 10 minutos, "
              "o jogo na sexta. Troque apenas a letra — o resto do plano é igual.",
              9.2, FONT, INK, 4.6 * mm)
    y -= 24 * mm

    # ordem completa
    texto(c, M, y, "A ORDEM DAS LETRAS (A MESMA DO CADERNO 01)", 9.6, FONT_B, PURPLE)
    texto(c, W - M, y, "coloridas = já trabalhadas", 7.8, FONT_I, SOFT, "r")
    y -= 5.4 * mm
    letras = "A E I O U M P B D T L C S R N F V G J Z X Q H K W Y".split()
    feitas = {"A", "E", "I", "O", "U", "M", "P", "B"}
    cw = (larg - 6 * mm) / 13
    for i, L in enumerate(letras):
        col, row = i % 13, i // 13
        x = M + 3 * mm + col * cw
        yy = y - 10 * mm - row * 13.4 * mm
        ok = L in feitas
        rrect(c, x, yy, cw - 1.8 * mm, 11 * mm, 5,
              PURPLE_L if ok else WHITE, None if ok else LINE, 0.9)
        texto(c, x + (cw - 1.8 * mm) / 2, yy + 3.8 * mm, L, 12, FONT_B,
              PURPLE if ok else SOFT, "c")
    y -= 10 * mm + 13.4 * mm + 8 * mm

    # próximas letras + páginas
    texto(c, M, y, "ONDE ESTÁ CADA LETRA NO CADERNO 02", 9.6, FONT_B, PURPLE)
    y -= 5.0 * mm
    paragrafo(c, M, y, larg - 2 * mm,
              "Cada consoante tem uma página de família silábica. O X, o Q, o H, o K, o W e o Y "
              "não têm página própria: ensine cada um com uma palavra do dia a dia.",
              8.6, FONT, SOFT, 4.0 * mm)
    y -= 13.6 * mm
    cols = 6
    cwp = larg / cols
    for i, (L, pg) in enumerate(PROXIMAS):
        col, row = i % cols, i // cols
        x = M + col * cwp
        yy = y - row * 7.8 * mm
        texto(c, x + 2 * mm, yy, L, 10, FONT_B, PURPLE)
        texto(c, x + 9 * mm, yy, pg, 8.8, FONT, INK if pg != "—" else SOFT)
    y -= 3 * 7.8 * mm + 10 * mm

    # quando avançar / repetir
    cw2 = (larg - 5 * mm) / 2
    av = ["Ela reconhece a letra em 3 lugares diferentes (folha, mural, livro).",
          "Acerta sem dica, dois dias seguidos.",
          "Consegue juntar a letra com as vogais sem ajuda."]
    rp = ["Ela ainda confunde a letra com outra parecida.",
          "Chora, foge da tarefa ou diz que não sabe.",
          "Passaram duas semanas e ela não reconhece a letra na rua."]
    alt = 7.4 * mm + max(_altura_lista(av, cw2 - 10 * mm, 8.7),
                         _altura_lista(rp, cw2 - 10 * mm, 8.7)) + 5 * mm
    _caixa_lista(c, M, y, cw2, alt, "AVANCE QUANDO", av, GREEN, GREEN_L, size=8.7)
    _caixa_lista(c, M + cw2 + 5 * mm, y, cw2, alt, "REPITA A SEMANA QUANDO", rp,
                 CORAL, CORAL_L, size=8.7)
    y -= alt + 6.5 * mm

    para = ("Preencha o registro de progresso (05 p. 6), pinte o mapa das letras (01 p. 59) "
            "e mostre para ela o quanto andou. Progresso que se vê anima — e criança animada "
            "aprende mais rápido.")
    linhas = quebrar(para, larg - 12 * mm, 8.8, FONT)
    y -= 2 * mm
    h = 13.6 * mm + (len(linhas) - 1) * 4.1 * mm + 4.4 * mm
    rrect(c, M, y - h, larg, h, 9, AMBER_L, None)
    texto(c, M + 6 * mm, y - 7.6 * mm, "A CADA 4 SEMANAS, PARE E OLHE PARA TRÁS", 9.0,
          FONT_B, AMBER)
    paragrafo(c, M + 6 * mm, y - 13.6 * mm, larg - 12 * mm, para, 8.8, FONT, INK, 4.1 * mm)
    y -= h + 9 * mm

    # retomada: as 18 letras que faltam, em semanas
    texto(c, M, y, "AS SEMANAS QUE FALTAM", 9.6, FONT_B, PURPLE)
    y -= 5.4 * mm
    faltam = [("5ª", "D e T"), ("6ª", "L e C"), ("7ª", "S e R"), ("8ª", "N e F"),
              ("9ª", "V e G"), ("10ª", "J e Z"), ("11ª", "X e Q"), ("12ª", "H e K"),
              ("13ª", "W e Y")]
    cwt = (larg - 8 * 2 * mm) / 5
    for i, (sem, par) in enumerate(faltam):
        col, row = i % 5, i // 5
        x = M + col * (cwt + 2 * mm)
        yy = y - 11 * mm - row * 15.4 * mm
        rrect(c, x, yy, cwt, 12.8 * mm, 6, PURPLE_L, None)
        texto(c, x + cwt / 2, yy + 8.2 * mm, f"{sem} SEMANA", 7.0, FONT_B, PURPLE, "c")
        texto(c, x + cwt / 2, yy + 3.4 * mm, par, 10, FONT_B, INK, "c")
    y -= 11 * mm + 12.8 * mm + 8 * mm

    paragrafo(c, M, y, larg,
              "Com 1 letra nova por semana no ritmo do guia, o alfabeto todo leva cerca de "
              "4 meses. Se ela engatar, dá para emendar duas letras por semana.",
              9.0, FONT_I, SOFT, 4.2 * mm)
    rodape(c, pag, total, "Cronograma • depois da 4ª semana")
