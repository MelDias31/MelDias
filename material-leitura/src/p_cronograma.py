# -*- coding: utf-8 -*-
"""Cronograma do alfabeto: 13 semanas, duas letras por semana.

Caderno 06. Não traz folha de atividade: diz qual folha usar em cada dia,
em que ordem imprimir e o que observar. Foi escrito para a mãe, não para
a criança.
"""
from base import (W, H, M, mm, INK, SOFT, LINE, WHITE, TEAL, TEAL_L, CORAL,
                  CORAL_L, AMBER, AMBER_L, BLUE, BLUE_L, PURPLE, PURPLE_L,
                  GREEN, GREEN_L, PINK, PINK_L, HexColor, FONT, FONT_B, FONT_I,
                  texto, quebrar, largura, paragrafo, rrect,
                  linha, faixa_titulo, rodape, fundo, numero_passo)
from figuras import emoji, checkbox
from conteudo import ALFABETO

CINZA = HexColor("#F7F9FB")
TRACO = HexColor("#E4E7EC")
BORDA = HexColor("#B9C0C9")


# --------------------------------------------------------------- utilidades
def _chips(c, x, y, itens, cor, cor_l, larg_max, size=8.0, h=5.2 * mm):
    """Desenha os 'chips' em linha, quebrando quando falta espaço."""
    cx, cy = x, y
    for t in itens:
        w = largura(t, size, FONT_B) + 6.4 * mm
        if cx + w > x + larg_max and cx > x:
            cx, cy = x, cy - (h + 1.2 * mm)
        rrect(c, cx, cy - h + 1.2 * mm, w, h, h / 2, cor_l, None)
        texto(c, cx + w / 2, cy - h / 2 + 0.6 * mm, t, size, FONT_B, cor, "c")
        cx += w + 1.4 * mm
    return cy


def _lista(c, itens, x, y, larg, cor, size=8.9):
    for t in itens:
        c.setFillColor(cor)
        c.circle(x + 1.2 * mm, y + 1.0 * mm, 1.0 * mm, stroke=0, fill=1)
        linhas = quebrar(t, larg - 6 * mm, size, FONT)
        for j, ln in enumerate(linhas):
            texto(c, x + 5 * mm, y - j * 4.1 * mm, ln, size, FONT, INK)
        y -= len(linhas) * 4.1 * mm + 2.2 * mm
    return y


def _caixa_lista(c, x, y, larg, alt, titulo, itens, cor, cor_l, size=8.9):
    rrect(c, x, y - alt, larg, alt, 9, cor_l, None)
    texto(c, x + 5 * mm, y - 7.4 * mm, titulo, 9.2, FONT_B, cor)
    _lista(c, itens, x + 6 * mm, y - 15.4 * mm, larg - 10 * mm, cor, size)


def _altura_lista(itens, larg, size=8.9):
    return sum(len(quebrar(t, larg, size, FONT)) * 4.1 + 2.2 for t in itens) * mm


# ------------------------------------------------------------------- dados
SEMANAS = [
    dict(
        letras=["A", "E"], cor=TEAL, cor_l=TEAL_L,
        sub="As duas primeiras vogais. Cinco dias curtos e dois dias leves.",
        imprimir=["01 p. 3 e 4", "01 p. 29 e 30", "01 p. 58"],
        lista="01 p. 3, 4, 29 e 30 · 01 p. 58",
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
        imprimir=["01 p. 5 e 6", "01 p. 31 e 32", "04 p. 3 e 4"],
        lista="01 p. 5, 6, 31 e 32 · 04 p. 3 e 4",
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
        imprimir=["01 p. 7 e 8", "01 p. 33 e 34", "02 p. 9", "02 p. 26", "04 p. 9"],
        lista="01 p. 7, 8, 33 e 34 · 02 p. 9 e 26 · 04 p. 9",
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
        imprimir=["01 p. 9 e 10", "01 p. 35 e 36", "02 p. 2 e 11", "03 p. 2", "04 p. 12"],
        lista="01 p. 9, 10, 35 e 36 · 02 p. 2 e 11 · 03 p. 2 · 04 p. 12",
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
            ("SÁB", "Revisão e primeiro certificado",
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
    dict(
        letras=["D", "T"], cor=GREEN, cor_l=GREEN_L,
        sub="Duas letras de traço simples. O D abre caminho para o nome dela.",
        imprimir=["01 p. 11 e 12", "01 p. 37 e 38", "02 p. 4 e 14", "04 p. 10"],
        lista="01 p. 11, 12, 37 e 38 · 02 p. 4 e 14 · 04 p. 10",
        dias=[
            ("SEG", "Letra D + família do D",
             "A barriga do D começa no topo e encosta na reta. DA DE DI DO DU.", "01 p. 11 · 02 p. 4"),
            ("TER", "Letra D minúscula",
             "O d pequeno tem a barriga para a esquerda, não para a direita.", "01 p. 37"),
            ("QUA", "Letra T + família do T",
             "O T é um chapéu em cima de uma reta. TA TE TI TO TU.", "01 p. 12 · 02 p. 14"),
            ("QUI", "Letra T minúscula",
             "O t pequeno tem o travessão no alto, não no pé.", "01 p. 38"),
            ("SEX", "Jogo: ligue a figura à palavra 2",
             "Ela liga pela primeira letra. Leia a palavra inteira junto.", "04 p. 10"),
            ("SÁB", "Caça de D e T em revista",
             "Achar as duas letras em embalagem, placa ou livro e apontar.", "revista"),
            ("DOM", "Descanso",
             "Nenhuma folha hoje. Se ela pedir, jogue o ligue de novo.", "—"),
        ],
        observar=[
            "Escreveu o D sem virar um O com risquinho?",
            "Leu DA, DE, DI sem você falar a sílaba antes?",
            "Reconheceu o D ou o T no nome dela?",
        ],
        travar=[
            "Confunde D com B? Faça a brincadeira do espelho (01 p. 55) antes da folha.",
            "A barriga do D sai torta? Desenhe a barriga no ar com o dedo, 5 vezes.",
            "Cansa nas sílabas? Faça só a linha do DA e deixe o resto para amanhã.",
        ],
    ),
    dict(
        letras=["L", "C"], cor=PINK, cor_l=PINK_L,
        sub="Duas letras que aparecem em tudo que ela vê na rua.",
        imprimir=["01 p. 13 e 14", "01 p. 39 e 40", "02 p. 3 e 8", "02 p. 26", "04 p. 12"],
        lista="01 p. 13, 14, 39 e 40 · 02 p. 3, 8 e 26 · 04 p. 12",
        dias=[
            ("SEG", "Letra L + família do L",
             "O L desce reto e faz o pé para a direita, sem levantar. LA LE LI LO LU.", "01 p. 13 · 02 p. 8"),
            ("TER", "Letra L minúscula",
             "O l pequeno é só uma reta alta, sem pé.", "01 p. 39"),
            ("QUA", "Letra C + família do C",
             "O C é uma meia-lua aberta para a direita. CA CO CU.", "01 p. 14 · 02 p. 3"),
            ("QUI", "Letra C minúscula",
             "Com E e I o C muda de som: CE, CI. Mostre CASA e CEBOLA.", "01 p. 40 · 02 p. 3"),
            ("SEX", "Jogo: caça-palavras 1",
             "Palavras na horizontal. Aponte a primeira letra e leia junto.", "04 p. 12"),
            ("SÁB", "Escada das palavras",
             "Pule as palavras com letras que ela ainda não viu. Sem pressa.", "02 p. 26"),
            ("DOM", "Descanso",
             "Nenhuma folha hoje. Semana que vem: S e R.", "—"),
        ],
        observar=[
            "O C saiu redondo ou virou um L torto?",
            "Percebeu que CE e CI têm som diferente de CA?",
            "Leu LU, LA ou LUA sozinha?",
        ],
        travar=[
            "Confunde L com I? Mostre o pé do L: o I não tem pé.",
            "O C fecha demais? Faça o C no ar, bem grande, antes do lápis.",
            "As palavras da escada assustam? Fique nos cartões de figura do caderno 04.",
        ],
    ),
    dict(
        letras=["S", "R"], cor=TEAL, cor_l=TEAL_L,
        sub="O S escorrega e o R tem perna. Duas letras que trocam de lugar nas palavras.",
        imprimir=["01 p. 15 e 16", "01 p. 41 e 42", "02 p. 12 e 13", "02 p. 28",
                  "04 p. 15 e 16"],
        lista="01 p. 15, 16, 41 e 42 · 02 p. 12, 13 e 28 · 04 p. 15 e 16",
        dias=[
            ("SEG", "Letra S + família do S",
             "O S é uma cobrinha: sobe, desce e volta. SA SE SI SO SU.", "01 p. 15 · 02 p. 13"),
            ("TER", "Letra S minúscula",
             "O s pequeno é a mesma cobrinha, só menor. Cubra e copie.", "01 p. 41"),
            ("QUA", "Letra R + família do R",
             "O R é o P com uma perna solta. RA RE RI RO RU.", "01 p. 16 · 02 p. 12"),
            ("QUI", "Letra R minúscula",
             "O r pequeno é curto. O RR do meio é forte: CARRO, PORTA.", "01 p. 42 · 02 p. 12"),
            ("SEX", "Jogo: dominó de sílabas",
             "Emende pela sílaba igual. Diga a sílaba em voz alta ao emendar.", "04 p. 15 e 16"),
            ("SÁB", "Revisão: leitura rápida",
             "Só a primeira coluna. Marque o tempo e tente de novo na semana seguinte.", "02 p. 28"),
            ("DOM", "Descanso",
             "Nenhuma folha hoje. Semana que vem: N e F.", "—"),
        ],
        observar=[
            "Diferencia o S do R ao escrever?",
            "Lê SA, SE, SO sem trocar a ordem das letras?",
            "Achou o S de sapo e o R de rato em outras palavras?",
        ],
        travar=[
            "Troca S com Z? Deixe o Z para depois: agora é só o S com som de S.",
            "O R do meio sai fraco? Diga a palavra exagerando: “ca-RR-o”.",
            "O dominó cansou? Use só 8 peças na mesa e guarde o resto.",
        ],
    ),
    dict(
        letras=["N", "F"], cor=CORAL, cor_l=CORAL_L,
        sub="A ponte do N e os braços do F: duas letras boas para ganhar confiança.",
        imprimir=["01 p. 17 e 18", "01 p. 43 e 44", "02 p. 5 e 10", "03 p. 2", "04 p. 11"],
        lista="01 p. 17, 18, 43 e 44 · 02 p. 5 e 10 · 03 p. 2 · 04 p. 11",
        dias=[
            ("SEG", "Letra N + família do N",
             "Duas retas com uma ponte no meio. NA NE NI NO NU.", "01 p. 17 · 02 p. 10"),
            ("TER", "Letra N minúscula",
             "O n pequeno é uma perna com a curva do m. Compare m e n.", "01 p. 43 · 02 p. 10"),
            ("QUA", "Letra F + família do F",
             "O F é uma reta com dois braços. FA FE FI FO FU.", "01 p. 18 · 02 p. 5"),
            ("QUI", "Letra F minúscula",
             "O f pequeno é o único que desce e sobe. Faça devagar.", "01 p. 44 · 02 p. 5"),
            ("SEX", "Jogo: ligue a figura à palavra 3",
             "Agora com palavras mais longas. Leia junto e deixe ela escolher.", "04 p. 11"),
            ("SÁB", "Leia a frase — nível 1",
             "Só sílabas. Uma linha por vez, com o dedo embaixo.", "03 p. 2"),
            ("DOM", "Descanso",
             "Nenhuma folha hoje. Metade do alfabeto já foi.", "—"),
        ],
        observar=[
            "Confunde M com N ao escrever? (é a troca mais comum aqui)",
            "Leu NA, NE ou o nome dela sem ajuda?",
            "Começou a ler sozinha alguma palavra da casa?",
        ],
        travar=[
            "Troca m e n? Mostre que o m tem duas pernas e o n só uma.",
            "O F sai com os braços tortos? Faça dois traços separados e depois junte.",
            "A frase nível 1 é muita coisa? Leia você e deixe ela apontar a palavra.",
        ],
    ),
    dict(
        letras=["V", "G"], cor=BLUE, cor_l=BLUE_L,
        sub="O V desce e o G ganha um degrau. As últimas letras de som previsível.",
        imprimir=["01 p. 19 e 20", "01 p. 45 e 46", "02 p. 6 e 15", "03 p. 3",
                  "04 p. 5 e 6"],
        lista="01 p. 19, 20, 45 e 46 · 02 p. 6 e 15 · 03 p. 3 · 04 p. 5 e 6",
        dias=[
            ("SEG", "Letra V + família do V",
             "O V é um vale fundo: desce e sobe. VA VE VI VO VU.", "01 p. 19 · 02 p. 15"),
            ("TER", "Letra V minúscula",
             "O v pequeno é o mesmo vale, menor. Cubra e copie.", "01 p. 45"),
            ("QUA", "Letra G + família do G",
             "O G é o C que ganhou um degrau. GA GO GU.", "01 p. 20 · 02 p. 6"),
            ("QUI", "Letra G minúscula",
             "O g pequeno desce abaixo da linha. Com E e I: GE, GI.", "01 p. 46 · 02 p. 6"),
            ("SEX", "Jogo: bingo de palavras",
             "Ela lê a cartela com você. Quem completa primeiro ganha a rodada.", "04 p. 5 e 6"),
            ("SÁB", "Leia a frase — nível 2",
             "Palavras de 2 sílabas, com artigo. Uma linha por vez.", "03 p. 3"),
            ("DOM", "Descanso",
             "Nenhuma folha hoje. Faltam 4 semanas para o fim do alfabeto.", "—"),
        ],
        observar=[
            "Distingue V de U ao escrever?",
            "Leu GA, GO ou GATO sozinha?",
            "Acertou alguma palavra do bingo sem você apontar?",
        ],
        travar=[
            "Troca V com U? Mostre o bico do V: ele não fecha em cima.",
            "O G sai como C? Faça o degrau separado e depois encaixe no C.",
            "O bingo é muita leitura? Jogue com uma cartela só, a dela.",
        ],
    ),
    dict(
        letras=["J", "Z"], cor=PURPLE, cor_l=PURPLE_L,
        sub="Duas letras de traço solto. O J desce e o Z corta.",
        imprimir=["01 p. 21 e 22", "01 p. 47 e 48", "02 p. 7 e 16", "03 p. 4",
                  "04 p. 13"],
        lista="01 p. 21, 22, 47 e 48 · 02 p. 7 e 16 · 03 p. 4 · 04 p. 13",
        dias=[
            ("SEG", "Letra J + família do J",
             "O J desce e faz a curva para a esquerda. JA JE JI JO JU.", "01 p. 21 · 02 p. 7"),
            ("TER", "Letra J minúscula",
             "O j pequeno tem pingo e desce abaixo da linha.", "01 p. 47"),
            ("QUA", "Letra Z + família do Z",
             "O Z é um raio: corta em cima e embaixo. ZA ZE ZI ZO ZU.", "01 p. 22 · 02 p. 16"),
            ("QUI", "Letra Z minúscula",
             "O z pequeno é o mesmo raio. Compare com o S: ZABELÊ x SAPO.", "01 p. 48"),
            ("SEX", "Jogo: caça-palavras 2",
             "Nível 2, com sílabas e dígrafos. Procure com ela, não por ela.", "04 p. 13"),
            ("SÁB", "Leia a frase — nível 3",
             "Frases com artigo e cor. Leia junto e mostre a cor escrita.", "03 p. 4"),
            ("DOM", "Descanso",
             "Nenhuma folha hoje. Faltam 3 semanas.", "—"),
        ],
        observar=[
            "Escreve o J sem virar um I com gancho no pé?",
            "Diferencia Z de S na leitura?",
            "Leu uma frase inteira do nível 3?",
        ],
        travar=[
            "Troca J com G? Diga “J de jacaré, G de gato” e aponte os dois.",
            "O Z sai como 2? Mostre que o Z tem quina, o 2 tem curva.",
            "O caça nível 2 é difícil? Volte ao nível 1 (04 p. 12) e faça só uma linha.",
        ],
    ),
    dict(
        letras=["X", "Q"], cor=AMBER, cor_l=AMBER_L,
        sub="As duas letras com mais jeitinhos. Ensine com a palavra do dia a dia.",
        imprimir=["01 p. 23 e 24", "01 p. 49 e 50", "01 p. 55", "03 p. 5", "04 p. 17"],
        lista="01 p. 23, 24, 49, 50 e 55 · 03 p. 5 · 04 p. 17",
        dias=[
            ("SEG", "Letra X — colorir e traçar",
             "O X é um cruzar de duas retas. XÍCARA, XÍCARA, XÍCARA.", "01 p. 23"),
            ("TER", "Letra X minúscula",
             "O x pequeno é o mesmo cruzado, menor. Some no meio das palavras.", "01 p. 49"),
            ("QUA", "Letra Q — colorir e traçar",
             "O Q é o O com um rabinho. QUEIJO começa com Q.", "01 p. 24"),
            ("QUI", "Letra Q minúscula e letras parecidas",
             "O q tem a barriga em cima e o rabinho embaixo. Compare p e q.", "01 p. 50 e 55"),
            ("SEX", "Jogo: forca das palavras",
             "O adulto sorteia a figura. Ela chuta letras até completar.", "04 p. 17"),
            ("SÁB", "Leia a frase — nível 4",
             "Frases com ação. Uma linha por vez, sem cobrar velocidade.", "03 p. 5"),
            ("DOM", "Descanso",
             "Nenhuma folha hoje. Faltam 2 semanas.", "—"),
        ],
        observar=[
            "Confunde p com q? (é a troca esperada nesta semana)",
            "Lembra que o Q precisa do U para soar? (QUEIJO, QUATRO)",
            "Leu uma frase com ação sem gaguejar demais?",
        ],
        travar=[
            "Troca p e q? Faça o espelho na frente dela: vire a folha e mostre.",
            "O Q sai como O? Diga “o Q tem rabinho, o O é redondo e fechado”.",
            "A forca frustra? Jogue com a figura à vista e só 3 letras por vez.",
        ],
    ),
    dict(
        letras=["H", "K"], cor=GREEN, cor_l=GREEN_L,
        sub="Letras que quase não aparecem sozinhas. Ensine com o nome dela e com a rua.",
        imprimir=["01 p. 25 e 26", "01 p. 51 e 52", "03 p. 7", "04 p. 14"],
        lista="01 p. 25, 26, 51 e 52 · 03 p. 7 · 04 p. 14",
        dias=[
            ("SEG", "Letra H — colorir e traçar",
             "O H são duas retas com uma ponte no meio. Não tem som sozinho.", "01 p. 25"),
            ("TER", "Letra H minúscula",
             "O h pequeno é a reta com a curva do n. H de HELICÓPTERO.", "01 p. 51"),
            ("QUA", "Letra K — colorir e traçar",
             "O K tem uma reta e dois braços abertos. KIWI, KOMBU, KAYAK.", "01 p. 26"),
            ("QUI", "Letra K minúscula",
             "O k pequeno é igual, menor. O K aparece em poucas palavras.", "01 p. 52"),
            ("SEX", "Jogo: caça-palavras 3",
             "Nível 3, palavras maiores. Procurem juntas, uma palavra por vez.", "04 p. 14"),
            ("SÁB", "Primeiras histórias",
             "Leia junto e deixe ela apontar as palavras que já conhece.", "03 p. 7"),
            ("DOM", "Descanso",
             "Nenhuma folha hoje. Falta 1 semana!", "—"),
        ],
        observar=[
            "Entendeu que o H é mudo no começo (HORA, HOJE)?",
            "Reconhece o K em alguma palavra da vida dela?",
            "Acompanhou a história com o dedo?",
        ],
        travar=[
            "O H não faz sentido para ela? Diga: “é uma letra decorativa, como um enfeite”.",
            "Nunca viu K? Use o nome de alguém conhecido ou uma marca da cozinha.",
            "A história é longa? Leia só o título e a primeira linha.",
        ],
    ),
    dict(
        letras=["W", "Y"], cor=PINK, cor_l=PINK_L,
        sub="As duas últimas. A semana termina com história, trilha e certificado.",
        imprimir=["01 p. 27 e 28", "01 p. 53 e 54", "03 p. 8", "04 p. 7 e 8",
                  "05 p. 8"],
        lista="01 p. 27, 28, 53 e 54 · 03 p. 8 · 04 p. 7 e 8 · 05 p. 8",
        dias=[
            ("SEG", "Letra W — colorir e traçar",
             "O W são dois V juntos. WAFFLE, WAFER, KIWI.", "01 p. 27"),
            ("TER", "Letra W minúscula",
             "O w pequeno é o mesmo desenho, menor. Quase só em nome próprio.", "01 p. 53"),
            ("QUA", "Letra Y — colorir e traçar",
             "O Y é um V com uma perna embaixo. YOGA, YOGURTE.", "01 p. 28"),
            ("QUI", "Letra Y minúscula",
             "O y pequeno desce abaixo da linha, com rabo. Última letra!", "01 p. 54"),
            ("SEX", "Jogo: trilha da leitura",
             "Ela joga o dado, anda e lê a casa. Pode ler com você junto.", "04 p. 7 e 8"),
            ("SÁB", "Mais histórias + certificado",
             "Leia a história e entregue o certificado do alfabeto completo.", "03 p. 8 · 05 p. 8"),
            ("DOM", "Festa",
             "Pinte o mapa das 26 letras e comemore: ela conhece o alfabeto.", "01 p. 59"),
        ],
        observar=[
            "Reconhece as 26 letras, mesmo que ainda confunda duas?",
            "Lê palavras curtas sozinha?",
            "Pede para ler em vez de fugir da tarefa?",
        ],
        travar=[
            "Ainda troca letras? Volte às parecidas (01 p. 55) e repita a semana certa.",
            "Não quer parar? Ótimo: siga para as sílabas complexas (02 p. 17 a 25).",
            "Chegou ao fim sem ler palavras? Repita as semanas 9 a 13 antes de avançar.",
        ],
    ),
]

FIXOS = [
    ("01 p. 1 e 2", "Capa e “Como usar este caderno”", "antes de começar"),
    ("05 p. 1 a 6", "Guia do adulto, rotina, quadro e registro", "antes de começar"),
    ("05 p. 7", "Cartões de pausa e elogio (recortar)", "semana 1"),
    ("01 p. 55", "Letras que se parecem (ler antes)", "semana 1"),
    ("01 p. 56 e 57", "Mural do alfabeto (parede)", "semana 1"),
    ("01 p. 59", "Mapa das 26 letras (parede)", "semana 1"),
    ("01 p. 58", "Bingo de letras (recortar)", "semana 1"),
    ("04 p. 3 e 4", "Jogo da memória (recortar)", "semana 2"),
    ("05 p. 8", "Certificado de leitura", "semana 13"),
]

COMPLEXAS = [("CH", "02 p. 17"), ("LH", "02 p. 18"), ("NH", "02 p. 19"),
             ("R / RR", "02 p. 20"), ("S / SS", "02 p. 21"), ("ÃO / ÃE", "02 p. 22"),
             ("CE / CI", "02 p. 23"), ("GE / GI", "02 p. 24"), ("QU / GU", "02 p. 25")]


# -------------------------------------------------------------------- capa
def capa(c, pag, total):
    fundo(c)
    topo = faixa_titulo(c, "CRONOGRAMA DO ALFABETO",
                        "13 semanas, duas letras por semana: o que fazer em cada dia.",
                        TEAL, TEAL_L, etiqueta="comece por aqui")
    larg = W - 2 * M
    y = topo - 5 * mm

    rrect(c, M, y - 22 * mm, larg, 22 * mm, 10, CINZA, LINE, 1)
    paragrafo(c, M + 6 * mm, y - 8 * mm, larg - 12 * mm,
              "Este caderno é o mapa do alfabeto inteiro. Aqui não tem folha para a criança: "
              "tem a ordem certa das folhas e o que fazer em cada dia. As atividades estão nos "
              "cadernos 01 a 04 — a lista da página 2 diz o que imprimir e quando.",
              9.4, FONT, INK, 4.4 * mm)
    y -= 26 * mm

    # as 13 semanas
    texto(c, M, y, "AS 13 SEMANAS", 9.8, FONT_B, TEAL)
    texto(c, W - M, y, "2 letras por semana · 5 dias de folha + 1 jogo + 1 descanso",
          7.8, FONT_I, SOFT, "r")
    y -= 5.6 * mm
    cols = 7
    cw = (larg - 6 * (cols - 1) * mm) / cols
    for i, s in enumerate(SEMANAS):
        col, row = i % cols, i // cols
        x = M + col * (cw + 6 * mm)
        yy = y - 12.6 * mm - row * 14.4 * mm
        rrect(c, x, yy, cw, 12.6 * mm, 6, s["cor_l"], None)
        texto(c, x + cw / 2, yy + 8.6 * mm, f"SEMANA {i + 1}", 6.6, FONT_B, s["cor"], "c")
        texto(c, x + cw / 2, yy + 3.6 * mm, f"{s['letras'][0]}  {s['letras'][1]}",
              12.5, FONT_B, s["cor"], "c")
    y -= 12.6 * mm + 14.4 * mm + 3 * mm

    # três regras
    rrect(c, M, y - 27 * mm, larg, 27 * mm, 10, AMBER_L, None)
    texto(c, M + 6 * mm, y - 7.6 * mm, "AS TRÊS REGRAS QUE NÃO MUDAM", 9.4, FONT_B, AMBER)
    regras = [
        ("10 MINUTOS", "Cronometre e pare no fim, mesmo se estiver indo bem."),
        ("UMA FOLHA", "Só a do dia na mesa. O resto fica guardado."),
        ("REPETIR", "Letra que não colou volta na semana seguinte."),
    ]
    cwr = (larg - 12 * mm) / 3
    for i, (t, d) in enumerate(regras):
        x = M + 6 * mm + i * cwr
        numero_passo(c, x + 3.4 * mm, y - 15.4 * mm, i + 1, r=3.3 * mm, fundo=AMBER, size=8.2)
        texto(c, x + 9 * mm, y - 14.5 * mm, t, 8.6, FONT_B, INK)
        for j, ln in enumerate(quebrar(d, cwr - 11 * mm, 8.3, FONT)):
            texto(c, x + 9 * mm, y - 19.4 * mm - j * 3.8 * mm, ln, 8.3, FONT, SOFT)
    y -= 31 * mm

    # como usar
    texto(c, M, y, "COMO USAR ESTE CADERNO", 9.8, FONT_B, BLUE)
    y -= 4.8 * mm
    passos = [
        ("1", "Imprima a semana 1 e monte a caixa.",
         "Capa e instruções, folhas do A e do E e o bingo. O resto fica guardado."),
        ("2", "Cada sexta-feira, imprima a semana seguinte.",
         "Uma linha da lista da página 2. São 4 a 6 folhas por semana."),
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
    y -= 3.2 * mm

    # o que tem em cada arquivo
    texto(c, M, y, "O QUE TEM EM CADA ARQUIVO", 9.8, FONT_B, PURPLE)
    y -= 5.2 * mm
    arquivos = [
        ("01", "Meu alfabeto", "59 p.", "as 26 letras, maiúscula e minúscula"),
        ("02", "Sílabas e palavras", "28 p.", "famílias silábicas e leitura"),
        ("03", "Leitura e escrita", "15 p.", "frases, histórias e ditado"),
        ("04", "Jogos e fichas", "17 p.", "memória, bingo, trilha, caça"),
        ("05", "Guia do adulto", "8 p.", "rotina, quadro e certificado"),
        ("06", "Este cronograma", f"{total} p.", "o dia a dia das 13 semanas"),
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
                        "Imprima uma linha por semana, quando chegar nela. Não precisa imprimir tudo.",
                        BLUE, BLUE_L, etiqueta="imprimir")
    larg = W - 2 * M
    y = topo - 4 * mm

    # bloco fixo
    rrect(c, M, y - 5.0 * mm, larg, 5.0 * mm, 3, BLUE_L, None)
    texto(c, M + 3 * mm, y - 3.5 * mm, "UMA VEZ SÓ — ANTES DE COMEÇAR", 7.8, FONT_B, BLUE)
    y -= 8.2 * mm
    x_arq, x_desc, x_quando = M + 11 * mm, M + 40 * mm, W - M - 2 * mm
    for arq, desc, quando in FIXOS:
        checkbox(c, M + 0.5 * mm, y - 1.5 * mm, 3.1 * mm, BORDA, 1)
        texto(c, x_arq, y, arq, 8.0, FONT_B, INK)
        texto(c, x_desc, y, desc, 8.0, FONT, INK)
        texto(c, x_quando, y, quando, 7.5, FONT, SOFT, "r")
        y -= 4.55 * mm
    y -= 2.4 * mm

    # semana a semana
    rrect(c, M, y - 5.0 * mm, larg, 5.0 * mm, 3, TEAL_L, None)
    texto(c, M + 3 * mm, y - 3.5 * mm, "SEMANA A SEMANA — IMPRIMA QUANDO CHEGAR", 7.8,
          FONT_B, TEAL)
    y -= 7.0 * mm
    x_sem = M + 0.5 * mm
    x_pag = M + 32 * mm
    for i, s in enumerate(SEMANAS):
        if i % 2 == 0:
            c.setFillColor(HexColor("#FBFCFD"))
            c.rect(M, y - 4.4 * mm, larg, 5.4 * mm, stroke=0, fill=1)
        texto(c, x_sem, y, f"SEM {i + 1}", 6.8, FONT_B, s["cor"])
        texto(c, x_sem + 11 * mm, y, f"{s['letras'][0]}  {s['letras'][1]}", 8.4, FONT_B, INK)
        texto(c, x_pag, y, s["lista"], 7.9, FONT, INK)
        y -= 5.35 * mm
    y -= 2.8 * mm

    linha(c, M, y + 1.6 * mm, W - M, y + 1.6 * mm, TRACO, 0.8)
    texto(c, M, y - 3.4 * mm,
          "Ao todo: 13 semanas · 2 letras por semana · cerca de 6 folhas novas por semana",
          8.2, FONT_B, BLUE)
    texto(c, W - M, y - 3.4 * mm, "dá para imprimir a semana em 5 minutos", 7.5,
          FONT_I, SOFT, "r")
    y -= 9.4 * mm

    dicas = [
        "Imprima em preto e branco: as folhas foram desenhadas para continuar legíveis.",
        "Frente e verso só nas folhas de traço. Jogos e certificados, em folha solta.",
        "Papel comum (75 g) serve. Para os jogos, cole em cartolina antes de recortar.",
        "O que ainda não vai usar fica num envelope fechado: folha à vista vira distração.",
    ]
    hbox = 7.2 * mm + _altura_lista(dicas, larg - 20 * mm, 8.6) + 5.2 * mm
    rrect(c, M, y - hbox, larg, hbox, 9, CINZA, LINE, 1)
    texto(c, M + 6 * mm, y - 7.4 * mm, "COMO ECONOMIZAR PAPEL E DINHEIRO", 9.0, FONT_B, BLUE)
    _lista(c, dicas, M + 6 * mm, y - 15.4 * mm, larg - 10 * mm, BLUE, size=8.6)
    y -= hbox + 6 * mm

    # fechamento: o que fazer antes de começar
    prep = [
        ("1", "Recorte os jogos da semana 1",
         "Bingo de letras (01 p. 58): recorte, dobre e guarde num saquinho."),
        ("2", "Cole na parede",
         "Mural (01 p. 56 e 57), mapa das letras (01 p. 59) e quadro de conquistas (05 p. 5)."),
        ("3", "Leia duas páginas do guia",
         "“Como ajudar” e “o que atrapalha” (05 p. 3). Leva 5 minutos."),
    ]
    hprep = 8.0 * mm + sum(4.6 * mm + len(quebrar(d, larg - 26 * mm, 8.5, FONT)) * 3.9 * mm + 2.4 * mm
                           for _, _, d in prep)
    rrect(c, M, y - hprep, larg, hprep, 9, AMBER_L, None)
    texto(c, M + 6 * mm, y - 8 * mm, "ANTES DA PRIMEIRA FOLHA (10 MINUTOS)", 9.0, FONT_B, AMBER)
    yy = y - 13.4 * mm
    for n, t, d in prep:
        numero_passo(c, M + 7.4 * mm, yy - 1.2 * mm, n, r=3.2 * mm, fundo=AMBER, size=7.8)
        texto(c, M + 14 * mm, yy, t, 8.8, FONT_B, INK)
        linhas = quebrar(d, larg - 26 * mm, 8.5, FONT)
        for j, ln in enumerate(linhas):
            texto(c, M + 14 * mm, yy - 4.2 * mm - j * 3.9 * mm, ln, 8.5, FONT, SOFT)
        yy -= 4.6 * mm + len(linhas) * 3.9 * mm + 2.4 * mm
    rodape(c, pag, total, "Cronograma • lista de impressão")


# ------------------------------------------------------------------- semana
def semana(c, pag, total, n):
    s = SEMANAS[n]
    fundo(c)
    letras = " e ".join(s["letras"])
    topo = faixa_titulo(c, f"SEMANA {n + 1} — LETRAS {letras}",
                        s["sub"], s["cor"], s["cor_l"], etiqueta=f"semana {n + 1} de 13")
    larg = W - 2 * M
    y = topo - 4 * mm

    texto(c, M, y, "IMPRIMIR:", 8.8, FONT_B, s["cor"])
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
    alt = 7.4 * mm + max(_altura_lista(s["observar"], cw - 10 * mm),
                         _altura_lista(s["travar"], cw - 10 * mm)) + 5.0 * mm
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
        emoji(c, fig, cx + 10 * mm, y - 25.6 * mm, 10.4 * mm, AMBER)
        texto(c, cx + 20 * mm, y - 23 * mm, L, 18, FONT_B, AMBER)
        texto(c, cx + 30 * mm, y - 22.4 * mm, "de", 8.2, FONT, SOFT)
        texto(c, cx + 30 * mm, y - 27 * mm, palavra.upper(), 9.4, FONT_B, INK)
    y -= h + 5.5 * mm

    # anotações
    h2 = y - (M + 8 * mm)
    if h2 > 18 * mm:
        rrect(c, M, M + 8 * mm, larg, h2, 9, CINZA, LINE, 1)
        texto(c, M + 6 * mm, y - 8 * mm, "ANOTE AQUI — PARA VOCÊ, NÃO PARA ELA", 8.6,
              FONT_B, BLUE)
        texto(c, M + 6 * mm, y - 13.6 * mm,
              "O que funcionou, o que travou e por onde recomeçar amanhã.", 8.4, FONT, SOFT)
        ini = y - 19.4 * mm
        fim = M + 11 * mm
        n_lin = max(int(round((ini - fim) / (8.6 * mm))) + 1, 2)
        passo = (ini - fim) / (n_lin - 1)
        for k in range(n_lin):
            yy = ini - k * passo
            linha(c, M + 6 * mm, yy, W - M - 6 * mm, yy, HexColor("#DDE3EA"), 0.8)
    rodape(c, pag, total, f"Cronograma • semana {n + 1} de 13")


# -------------------------------------------------------------------- depois
def depois(c, pag, total):
    fundo(c)
    topo = faixa_titulo(c, "DEPOIS DAS 13 SEMANAS",
                        "Alfabeto completo. Agora a leitura ganha velocidade.",
                        PURPLE, PURPLE_L, etiqueta="continue")
    larg = W - 2 * M
    y = topo - 5 * mm

    rrect(c, M, y - 19 * mm, larg, 19 * mm, 10, CINZA, LINE, 1)
    paragrafo(c, M + 6 * mm, y - 7.4 * mm, larg - 12 * mm,
              "Ela conhece as 26 letras — mas conhecer não é ler. A fase seguinte é juntar "
              "letras em blocos maiores e ganhar velocidade. É o mesmo esquema: 10 minutos, "
              "uma folha por vez, jogo na sexta.",
              9.2, FONT, INK, 4.5 * mm)
    y -= 25 * mm

    # fase 2: complexas
    texto(c, M, y, "FASE 2 — SÍLABAS QUE PRECISAM DE ATENÇÃO", 9.4, FONT_B, PURPLE)
    texto(c, W - M, y, "uma por semana, 9 semanas", 7.8, FONT_I, SOFT, "r")
    y -= 5.2 * mm
    cols = 3
    cw = (larg - 2 * 4 * mm) / cols
    for i, (nome, pg) in enumerate(COMPLEXAS):
        col, row = i % cols, i // cols
        x = M + col * (cw + 4 * mm)
        yy = y - 11.6 * mm - row * 13.6 * mm
        rrect(c, x, yy, cw, 11.6 * mm, 6, PURPLE_L, None)
        texto(c, x + cw / 2, yy + 7.8 * mm, nome, 10.2, FONT_B, PURPLE, "c")
        texto(c, x + cw / 2, yy + 3.4 * mm, pg, 8.0, FONT, SOFT, "c")
    y -= 11.6 * mm + 2 * 13.6 * mm + 9 * mm

    # fase 3: ler de verdade
    texto(c, M, y, "FASE 3 — LER DE VERDADE", 9.4, FONT_B, PURPLE)
    y -= 5.0 * mm
    cards = [
        ("PALAVRAS MAIORES", "02 p. 27", "Quando as curtas já estão fáceis."),
        ("LEITURA RÁPIDA", "02 p. 28", "Cronometrar vira jogo: 3 tentativas e melhora."),
        ("HISTÓRIAS", "03 p. 7 e 8", "Uma linha por vez, apontando com o dedo."),
        ("ESCREVER", "03 p. 9 a 14", "Ditado de figuras e folhas de escrita."),
    ]
    cw2 = (larg - 4 * mm) / 2
    for i, (t, pg, d) in enumerate(cards):
        col, row = i % 2, i // 2
        x = M + col * (cw2 + 4 * mm)
        yy = y - 17 * mm - row * 19 * mm
        rrect(c, x, yy, cw2, 17 * mm, 8, WHITE, LINE, 1)
        texto(c, x + 4.5 * mm, yy + 11.4 * mm, t, 8.6, FONT_B, PURPLE)
        texto(c, x + cw2 - 4.5 * mm, yy + 11.4 * mm, pg, 8.2, FONT_B, PURPLE, "r")
        for j, ln in enumerate(quebrar(d, cw2 - 9 * mm, 8.4, FONT)):
            texto(c, x + 4.5 * mm, yy + 6.6 * mm - j * 3.8 * mm, ln, 8.4, FONT, SOFT)
    y -= 17 * mm + 19 * mm + 3 * mm

    # sinais de alerta
    sinais0 = ("Se, depois de um ano de trabalho, ela ainda troca letras de forma insistente, "
               "não lê palavras curtas ou chora diante da tarefa, leve o material e três folhas "
               "feitas a um fonoaudiólogo, neuropediatra ou psicopedagogo. Este kit é apoio "
               "pedagógico e não substitui avaliação.")
    hsin = 12.6 * mm + (len(quebrar(sinais0, larg - 12 * mm, 8.6, FONT)) - 1) * 4.0 * mm + 3.4 * mm
    rrect(c, M, y - hsin, larg, hsin, 9, CORAL_L, None)
    texto(c, M + 6 * mm, y - 7.6 * mm, "QUANDO PARAR E PROCURAR AVALIAÇÃO", 9.0, FONT_B, CORAL)
    paragrafo(c, M + 6 * mm, y - 12.8 * mm, larg - 12 * mm, sinais0, 8.6, FONT, INK, 4.0 * mm)
    y -= hsin + 8 * mm

    # rotina que continua
    texto(c, M, y, "A ROTINA QUE CONTINUA IGUAL", 9.4, FONT_B, PURPLE)
    y -= 5.6 * mm
    rotina = [
        ("SEG a QUI", "uma folha nova por dia", "10 minutos, sem cobrar capricho"),
        ("SEX", "um jogo do caderno 04", "memória, bingo, trilha ou forca"),
        ("SÁB", "leitura livre", "ela escolhe o que ler — bula, gibi, receita"),
        ("DOM", "descanso", "nenhuma tarefa, de propósito"),
    ]
    rowh = 9.6 * mm
    for i, (quando, o_que, obs) in enumerate(rotina):
        yy = y - rowh * (i + 1)
        if i % 2 == 0:
            c.setFillColor(HexColor("#FBFCFD"))
            c.rect(M, yy, larg, rowh, stroke=0, fill=1)
        texto(c, M + 3 * mm, yy + 3.4 * mm, quando, 8.2, FONT_B, PURPLE)
        texto(c, M + 34 * mm, yy + 3.4 * mm, o_que, 8.8, FONT_B, INK)
        texto(c, M + 96 * mm, yy + 3.4 * mm, obs, 8.4, FONT, SOFT)
        linha(c, M, yy, W - M, yy, HexColor("#EDF0F4"), 0.8)
    y -= rowh * len(rotina) + 6 * mm

    # marco final
    yy = max(y - 22 * mm, M + 12 * mm)
    rrect(c, M, yy, larg, y - yy, 9, TEAL_L, None)
    texto(c, M + 6 * mm, y - 8 * mm, "MARCO: 13 SEMANAS", 9.0, FONT_B, TEAL)
    para2 = ("Se ela chegou até aqui, conhece as 26 letras. Isso não é pouco: é o alicerce. "
             "A partir de agora, o ganho vem da repetição em textos de verdade — e não de "
             "mais folhas de traço.")
    paragrafo(c, M + 6 * mm, y - 14.4 * mm, larg - 12 * mm, para2, 8.8, FONT, INK, 4.1 * mm)
    rodape(c, pag, total, "Cronograma • depois das 13 semanas")
