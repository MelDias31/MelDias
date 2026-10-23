# -*- coding: utf-8 -*-
"""Material para o adulto: guia, rotina, quadro de recompensas, registro, certificado."""
from reportlab.lib.units import mm

from base import *
from contornos import desenhar_texto, medir
from figuras import emoji, checkbox, bolinhas_progresso
from letras import desenhar_letra
from conteudo import ORDEM, ALFABETO


def capa_kit(c, pag, total):
    fundo(c, CREAM)
    c.setFillColor(TEAL)
    c.rect(0, H - 108 * mm, W, 108 * mm, stroke=0, fill=1)
    coruja(c, W / 2, H - 52 * mm, 24 * mm, AMBER, AMBER_L, WHITE, CORAL, INK)
    texto(c, W / 2, H - 84 * mm, "KIT LER SEM PRESSA", 32, FONT_B, WHITE, "c")
    texto(c, W / 2, H - 94 * mm, "alfabetização para crianças com TDAH",
          13, FONT, TEAL_L, "c")
    texto(c, W / 2, H - 102 * mm, "6 a 8 anos • 1 folha por vez • 10 minutos por dia",
          10, FONT, TEAL_L, "c")

    y = H - 126 * mm
    itens = [
        ("🐝", "26 folhas de letras", "colorir, traçar e achar"),
        ("🅱️", "15 famílias silábicas", "BA BE BI BO BU..."),
        ("🐱", "leitura em 5 níveis", "da sílaba à frase"),
        ("🎲", "8 jogos imprimíveis", "memória, bingo, trilha"),
        ("📋", "guia do adulto", "rotina, elogio, registro"),
        ("🏆", "certificado", "para comemorar cada etapa"),
    ]
    for i, (fig, tit, sub) in enumerate(itens):
        col, row = i % 2, i // 2
        x = M + col * ((W - 2 * M) / 2)
        yy = y - row * 22 * mm
        rrect(c, x + 2 * mm, yy - 16 * mm, (W - 2 * M) / 2 - 5 * mm, 18 * mm, 8,
              WHITE, HexColor("#E6E1D5"), 1)
        emoji(c, fig, x + 11 * mm, yy - 7 * mm, 11 * mm, TEAL)
        texto(c, x + 20 * mm, yy - 4 * mm, tit, 10, FONT_B, INK)
        texto(c, x + 20 * mm, yy - 11 * mm, sub, 8, FONT, SOFT)

    y2 = M + 26 * mm
    rrect(c, M, y2, W - 2 * M, 22 * mm, 8, AMBER_L, None)
    paragrafo(c, M + 6 * mm, y2 + 14 * mm, W - 2 * M - 12 * mm,
              "Este material não substitui acompanhamento médico, fonoaudiológico ou "
              "psicopedagógico. Ele é um apoio para o dia a dia em casa e na escola.",
              9, FONT, INK)
    rodape(c, pag, total, "Kit Ler sem Pressa • material de apoio • uso livre em casa e na escola")


def guia_tdah(c, pag, total):
    fundo(c)
    topo = faixa_titulo(c, "COMO AJUDAR UMA CRIANÇA COM TDAH A LER",
                        "O que funciona na prática — e o que atrapalha",
                        BLUE, BLUE_L, etiqueta="guia")
    larg = W - 2 * M
    col_w = (larg - 6 * mm) / 2

    ajuda = [
        ("⏱️", "Sessões curtas", "10 minutos por dia rendem mais que 1 hora no fim de semana."),
        ("🎯", "Uma tarefa por vez", "Cubra o resto da folha com uma folha em branco e mostre só a linha que está sendo feita."),
        ("👀", "Instrução visual", "Aponte, mostre, faça junto. Palavra falada some; o desenho fica."),
        ("🔁", "Repetir brincando", "Repetir é necessário. Mude o formato (dedo, giz, massinha, areia) em vez de repetir a mesma folha."),
        ("⚡", "Movimento antes", "5 minutos de pular, dançar ou correr antes de sentar melhora o foco."),
        ("🏆", "Elogio específico", "“Você seguiu a seta até o fim!” em vez de “muito bem”."),
        ("🎲", "Virar brincadeira", "Cronometrar, jogar dado, ganhar adesivo — o jogo sustenta a atenção."),
        ("😴", "Sono e rotina", "Criança cansada não aprende letra nova. Sono regular é parte do método."),
    ]
    atrapalha = [
        ("🚫", "Muitas ordens juntas", "“Pega o lápis, senta, olha a folha, escreve” = 4 ordens. Diga uma de cada vez."),
        ("⏳", "Sessões longas", "Depois de 10–15 minutos o cérebro TDAH já saiu da mesa. Insistir gera briga, não leitura."),
        ("📄", "Folha cheia", "Muitos estímulos competem entre si. Menos itens por página = mais foco."),
        ("🗣️", "Comparação", "“A vizinha já lê” desmotiva e não ensina nada."),
        ("❌", "Corrigir tudo", "Corrigir cada erro quebra o fluxo. Escolha 1 coisa por vez para ajustar."),
        ("😤", "Castigo por errar", "Erro é informação: mostra o que precisa ser reensinado."),
        ("📱", "Tela antes da tarefa", "Telas aumentam a busca por estímulo rápido e dificultam a concentração."),
        ("🤫", "Silêncio absoluto", "Muitas crianças focam melhor com ruído branco ou música instrumental baixa."),
    ]

    # altura das colunas calculada pelo conteúdo
    def altura_bloco(itens, w):
        h = 16 * mm
        for fig, tit, txt in itens:
            h += (len(quebrar(txt, w - 20 * mm, 8.4, FONT)) * 4.0 + 5.0) * mm
        return h + 2 * mm

    h_col = max(altura_bloco(ajuda, col_w), altura_bloco(atrapalha, col_w))
    y = topo - 5 * mm
    for i, (itens, cor, cor_l, cab) in enumerate([
            (ajuda, GREEN, GREEN_L, "O QUE AJUDA"),
            (atrapalha, CORAL, CORAL_L, "O QUE ATRAPALHA")]):
        x = M + i * (col_w + 6 * mm)
        rrect(c, x, y - h_col, col_w, h_col, 10, cor_l, None)
        texto(c, x + 5 * mm, y - 9 * mm, cab, 11, FONT_B, cor)
        yy = y - 17 * mm
        for fig, tit, txt in itens:
            emoji(c, fig, x + 8 * mm, yy + 1 * mm, 8.5 * mm, cor)
            texto(c, x + 15 * mm, yy, tit, 9.2, FONT_B, INK)
            linhas = quebrar(txt, col_w - 20 * mm, 8.4, FONT)
            for j, ln in enumerate(linhas):
                texto(c, x + 15 * mm, yy - (j + 1) * 4.0 * mm, ln, 8.4, FONT, SOFT)
            yy -= (len(linhas) * 4.0 + 5.0) * mm

    # faixa final: quando procurar avaliação + adaptações na escola
    y2 = y - h_col - 5 * mm
    h2 = y2 - M - 4 * mm
    metade = (larg - 6 * mm) / 2
    for i, (cab, cor, cor_l, itens) in enumerate([
        ("QUANDO PROCURAR AVALIAÇÃO", BLUE, HexColor("#EEF4F8"), [
            ("Troca letras", "Confunde letras parecidas de forma insistente, lê muito devagar e adivinha palavras pelo contexto."),
            ("Fala", "Troca sons ao falar, some sílabas, não repete palavras longas."),
            ("Escuta e visão", "Não ouve bem, aproxima muito o papel, aperta os olhos."),
            ("Sofrimento", "Chora, evita a tarefa, diz que “é burra”, recusa ir à escola."),
            ("Sempre foi assim?", "Dificuldade que começou cedo e não melhora com o tempo pede avaliação."),
        ]),
        ("O QUE PEDIR NA ESCOLA", PURPLE, HexColor("#F1EEF6"), [
            ("Sentar na frente", "Perto do professor, longe da janela e da porta."),
            ("Tarefa reduzida", "Mesmo conteúdo, menos repetições — qualidade, não quantidade."),
            ("Instrução em partes", "Uma ordem por vez, com apoio escrito ou desenhado."),
            ("Tempo extra", "Mais tempo para copiar e para provas; pausas curtas permitidas."),
            ("Sem constrangimento", "Não ler em voz alta na frente da turma sem aviso ou preparo."),
        ]),
    ]):
        x = M + i * (metade + 6 * mm)
        rrect(c, x, y2 - h2, metade, h2, 10, cor_l, None)
        texto(c, x + 5 * mm, y2 - 8 * mm, cab, 9.5, FONT_B, cor)
        yy = y2 - 16 * mm
        for tit, txt in itens:
            texto(c, x + 5 * mm, yy, "•  " + tit, 8.4, FONT_B, INK)
            linhas = quebrar(txt, metade - 10 * mm, 8.0, FONT)
            for j, ln in enumerate(linhas):
                texto(c, x + 5 * mm, yy - (j + 1) * 3.8 * mm, ln, 8.0, FONT, SOFT)
            yy -= len(linhas) * 3.8 * mm + 3.0 * mm
        texto(c, x + 5 * mm, y2 - h2 + 4 * mm,
              "Leve este material na reunião. Ele é seu apoio." if i == 1
              else "Este material é apoio, não diagnóstico.",
              7.6, FONT_I, SOFT)

    rodape(c, pag, total, "Guia do adulto • 1 de 4")


def rotina(c, pag, total):
    fundo(c)
    topo = faixa_titulo(c, "ROTINA DE 10 MINUTOS", "O mesmo horário, todos os dias, sempre com começo e fim.",
                        AMBER, AMBER_L, etiqueta="guia")
    larg = W - 2 * M

    passos = [
        ("1", "PREPARAR", "2 min", "Escolha UMA folha. Deixe só ela sobre a mesa, junto com lápis e borracha. Tire o resto da vista."),
        ("2", "AQUECER", "2 min", "Brincadeira rápida: achar a letra no ambiente, cantar o alfabeto, jogar o dado da trilha."),
        ("3", "FAZER JUNTO", "4 min", "Você faz a primeira linha junto, falando o que faz. Depois a criança repete sozinha."),
        ("4", "FECHAR BEM", "2 min", "Guarde tudo, marque o quadro de adesivos e diga exatamente o que ela fez bem."),
    ]
    y = topo - 6 * mm
    for num, tit, tempo, txt in passos:
        h = 27 * mm
        rrect(c, M, y - h, larg, h, 10, WHITE, LINE, 1)
        numero_passo(c, M + 10 * mm, y - h / 2, num, 7, WHITE, AMBER, 11)
        texto(c, M + 20 * mm, y - 8 * mm, tit, 11, FONT_B, INK)
        chip(c, M + 20 * mm + largura(tit, 11, FONT_B) + 4 * mm, y - 9 * mm, tempo,
             AMBER, AMBER_L, 7.5)
        linhas = quebrar(txt, larg - 26 * mm, 8.8, FONT)
        for j, ln in enumerate(linhas):
            texto(c, M + 20 * mm, y - 14 * mm - j * 4.2 * mm, ln, 8.8, FONT, SOFT)
        y -= h + 3.5 * mm

    # semana
    y -= 3 * mm
    texto(c, M, y, "SUGESTÃO DE SEMANA", 9.5, FONT_B, AMBER)
    y -= 5 * mm
    semana = [
        ("SEG", "Uma letra nova", "folha de letra"),
        ("TER", "Repetir a letra", "traçar grande (giz, massinha)"),
        ("QUA", "Família silábica", "sílabas com a letra"),
        ("QUI", "Jogo", "memória, bingo ou trilha"),
        ("SEX", "Leitura", "frases do nível atual"),
        ("SÁB", "Revisão leve", "2 minutos, só o que já sabe"),
        ("DOM", "Descanso", "sem tarefa — e sem culpa"),
    ]
    cw = larg / 7
    hh = 22 * mm
    for i, (dia, tarefa, det) in enumerate(semana):
        x = M + i * cw
        cor = PALETA[i % 7]
        cor_l = PALETA_L[i % 7]
        rrect(c, x + 0.8 * mm, y - hh, cw - 1.6 * mm, hh, 6, cor_l, None)
        texto(c, x + cw / 2, y - 6 * mm, dia, 8.5, FONT_B, cor, "c")
        for j, ln in enumerate(quebrar(tarefa, cw - 3 * mm, 7.6, FONT_B)):
            texto(c, x + cw / 2, y - 11 * mm - j * 3.6 * mm, ln, 7.6, FONT_B, INK, "c")
        for j, ln in enumerate(quebrar(det, cw - 3 * mm, 6.8, FONT)):
            texto(c, x + cw / 2, y - 17.5 * mm - j * 3.2 * mm, ln, 6.8, FONT, SOFT, "c")

    y -= hh + 6 * mm
    rrect(c, M, M + 4 * mm, larg, y - M - 4 * mm, 10, TEAL_L, None)
    texto(c, M + 5 * mm, y - 8 * mm, "REGRA DE OURO", 9, FONT_B, TEAL)
    paragrafo(c, M + 5 * mm, y - 14 * mm, larg - 10 * mm,
              "Se em 10 minutos a criança não engajou, encerre com carinho e tente de novo "
              "amanhã. Insistir depois do limite ensina que ler é sofrimento — e isso é "
              "muito mais difícil de desfazer do que uma sílaba esquecida.", 9, FONT, INK)
    rodape(c, pag, total, "Guia do adulto • 2 de 4")


def quadro_recompensas(c, pag, total):
    fundo(c)
    topo = faixa_titulo(c, "QUADRO DE CONQUISTAS", "Pinte um círculo a cada dia de tarefa feita. Sem prêmio por nota: o prêmio é o esforço.",
                        PINK, PINK_L, etiqueta="guia")
    larg = W - 2 * M

    # 4 semanas x 7 dias
    y = topo - 13 * mm
    texto(c, M, y + 6 * mm, "MÊS DE:", 10, FONT_B, INK)
    linha(c, M + 18 * mm, y + 5.5 * mm, M + 70 * mm, y + 5.5 * mm, LINE, 1)
    dias = ["S", "T", "Q", "Q", "S", "S", "D"]
    for semana in range(4):
        yy = y - semana * 26 * mm
        texto(c, M + 2 * mm, yy - 10 * mm, f"SEMANA {semana + 1}", 8, FONT_B, SOFT)
        for d in range(7):
            cx = M + 34 * mm + d * ((larg - 34 * mm) / 7)
            c.setStrokeColor(HexColor("#C9CDD4"))
            c.setLineWidth(1)
            c.setFillColor(WHITE)
            c.circle(cx, yy - 12 * mm, 7.2 * mm, stroke=1, fill=1)
            texto(c, cx, yy - 22 * mm, dias[d], 7, FONT, SOFT, "c")

    # prêmios combinados
    y2 = y - 4 * 26 * mm - 4 * mm
    rrect(c, M, y2 - 34 * mm, larg, 34 * mm, 10, AMBER_L, None)
    texto(c, M + 5 * mm, y2 - 8 * mm, "COMBINE ANTES: O QUE ELA GANHA AO COMPLETAR...", 9, FONT_B, AMBER)
    metas = [("7 dias", "_________________________"), ("14 dias", "_________________________"),
             ("21 dias", "_________________________"), ("30 dias", "_________________________")]
    for i, (m, linha_txt) in enumerate(metas):
        col, row = i % 2, i // 2
        x = M + 6 * mm + col * ((larg - 12 * mm) / 2)
        yy = y2 - 16 * mm - row * 9 * mm
        texto(c, x, yy, m, 8.5, FONT_B, INK)
        texto(c, x + 14 * mm, yy, "→", 8.5, FONT, SOFT)
        linha(c, x + 20 * mm, yy - 1, x + 20 * mm + 55 * mm, yy - 1, HexColor("#B9C0C9"), 0.9)

    # dicas de recompensa
    y3 = y2 - 38 * mm
    rrect(c, M, M + 4 * mm, larg, y3 - M - 4 * mm, 10, WHITE, LINE, 1)
    texto(c, M + 5 * mm, y3 - 8 * mm, "RECOMPENSAS QUE FUNCIONAM MELHOR", 9, FONT_B, TEAL)
    opcoes = [
        "Escolher o jantar ou o filme da noite",
        "10 minutos extras de brincadeira com você",
        "Um adesivo para colar no caderno",
        "Ir ao parque ou andar de bicicleta",
        "Escolher a história da noite (sem cobrar leitura)",
        "Dormir 15 minutos mais tarde no fim de semana",
        "Ligar para alguém querido e contar a conquista",
        "Escolher a música do caminho da escola",
    ]
    yy = y3 - 17 * mm
    for i, op in enumerate(opcoes):
        col, row = i % 2, i // 2
        x = M + 6 * mm + col * ((larg - 12 * mm) / 2)
        yyy = yy - row * 8.5 * mm
        c.setFillColor(PINK)
        c.circle(x + 1.5 * mm, yyy + 2.2 * mm, 1.2 * mm, stroke=0, fill=1)
        texto(c, x + 5 * mm, yyy, op, 8.2, FONT, INK)
    rodape(c, pag, total, "Guia do adulto • 3 de 4")


def registro(c, pag, total):
    fundo(c)
    topo = faixa_titulo(c, "REGISTRO DE PROGRESSO", "Preencha 1 vez por semana. Serve para ver o avanço e conversar com profissionais.",
                        TEAL, TEAL_L, etiqueta="guia")
    larg = W - 2 * M
    y = topo - 8 * mm

    # o que observar
    texto(c, M, y, "O QUE OBSERVAR (marque o que já aparece)", 9.5, FONT_B, INK)
    y -= 7 * mm
    itens = [
        "Reconhece o próprio nome escrito",
        "Nomeia as letras do alfabeto sem apoio",
        "Junta sílabas simples (BA, CA, DA…)",
        "Lê palavras de 2 sílabas",
        "Lê palavras de 3 sílabas",
        "Lê frases curtas com apoio de figura",
        "Escreve o próprio nome sem modelo",
        "Escreve palavras ditadas com sílabas simples",
        "Segue a seta de traçado até o fim",
        "Permanece 10 minutos na tarefa",
    ]
    for i, it in enumerate(itens):
        col, row = i % 2, i // 2
        x = M + col * (larg / 2)
        yy = y - row * 8.6 * mm
        checkbox(c, x, yy - 1.5 * mm, 4.6 * mm, HexColor("#9AA3AF"), 1)
        texto(c, x + 7 * mm, yy, it, 8.6, FONT, INK)

    y2 = y - 5 * 8.6 * mm - 6 * mm
    # tabela semanal
    cols = [24, 20, 46, 50, 40]
    cabecalho = ["SEMANA", "DIAS FEITOS", "LETRA / SÍLABA", "O QUE FOI FÁCIL", "O QUE AINDA CONFUNDE"]
    x = M
    hh = 9 * mm
    rrect(c, M, y2 - hh, larg, hh, 4, TEAL, None)
    for i, (txt, w) in enumerate(zip(cabecalho, cols)):
        texto(c, x + 2 * mm, y2 - 6 * mm, txt, 6.8, FONT_B, WHITE)
        x += w * mm
    for r in range(6):
        yy = y2 - hh - (r + 1) * 11 * mm
        c.setFillColor(WHITE if r % 2 == 0 else HexColor("#F7F9FB"))
        c.rect(M, yy, larg, 11 * mm, stroke=0, fill=1)
        c.setStrokeColor(HexColor("#E1E6EC"))
        c.setLineWidth(0.6)
        c.rect(M, yy, larg, 11 * mm, stroke=1, fill=0)
        x = M
        for w in cols[:-1]:
            x += w * mm
            c.line(x, yy, x, yy + 11 * mm)

    y3 = y2 - hh - 6 * 11 * mm - 5 * mm
    # "está lendo" e "próximo passo"
    h_box = y3 - M - 4 * mm
    rrect(c, M, M + 4 * mm, larg, h_box, 10, AMBER_L, None)
    texto(c, M + 5 * mm, y3 - 8 * mm, "PARA LEVAR AO PROFISSIONAL", 9, FONT_B, AMBER)
    paragrafo(c, M + 5 * mm, y3 - 14 * mm, larg - 10 * mm,
              "Leve este registro e 3 folhas feitas pela criança nas consultas de "
              "fonoaudiologia, neuropediatria ou psicopedagogia. O padrão dos erros "
              "(troca de letras parecidas, sílabas invertidas, leitura silabada) ajuda "
              "no diagnóstico.", 8.6, FONT, INK)
    # anotações livres
    yy = y3 - 30 * mm
    texto(c, M + 5 * mm, yy, "ANOTAÇÕES E CONQUISTAS DA SEMANA", 8, FONT_B, AMBER)
    for k in range(3):
        linha(c, M + 5 * mm, yy - 8 * mm - k * 8 * mm, W - M - 5 * mm,
              yy - 8 * mm - k * 8 * mm, HexColor("#D6C7A8"), 0.9)
    rodape(c, pag, total, "Guia do adulto • 4 de 4")


def certificados(c, pag, total):
    """Dois certificados por folha (recortar no meio)."""
    fundo(c)
    larg = W - 2 * M
    alt = (H - 2 * M - 10 * mm) / 2
    for k in range(2):
        y = H - M - k * (alt + 10 * mm) - alt
        cor = TEAL if k == 0 else PURPLE
        cor_l = TEAL_L if k == 0 else PURPLE_L
        rrect(c, M, y, larg, alt, 12, cor_l, None)
        rrect(c, M + 4 * mm, y + 4 * mm, larg - 8 * mm, alt - 8 * mm, 9,
              WHITE, cor, 1.6)
        # moldura interna pontilhada
        rrect(c, M + 7 * mm, y + 7 * mm, larg - 14 * mm, alt - 14 * mm, 6,
              None, cor, 0.8, dash=[3, 3])
        estrela(c, M + larg / 2, y + alt - 18 * mm, 8 * mm, AMBER)
        texto(c, W / 2, y + alt - 30 * mm, "CERTIFICADO", 24, FONT_B, cor, "c")
        texto(c, W / 2, y + alt - 38 * mm, "de leitura", 11, FONT, SOFT, "c")
        texto(c, W / 2, y + alt - 48 * mm, "Entregue para", 9, FONT, SOFT, "c")
        linha(c, M + 22 * mm, y + alt - 60 * mm, W - M - 22 * mm, y + alt - 60 * mm,
              HexColor("#9AA3AF"), 1.2)
        texto(c, W / 2, y + alt - 70 * mm, "por ter concluído com esforço:", 9, FONT, SOFT, "c")
        if k == 0:
            metas = "AS 26 LETRAS DO ALFABETO"
        else:
            metas = "AS SÍLABAS E AS PRIMEIRAS PALAVRAS"
        texto(c, W / 2, y + alt - 82 * mm, metas, 13, FONT_B, cor, "c")
        coruja(c, M + 22 * mm, y + 20 * mm, 11 * mm, AMBER, AMBER_L, WHITE, CORAL, INK)
        linha(c, W - M - 66 * mm, y + 18 * mm, W - M - 18 * mm, y + 18 * mm,
              HexColor("#9AA3AF"), 1)
        texto(c, W - M - 42 * mm, y + 13 * mm, "data", 7.5, FONT, SOFT, "c")
        linha(c, M + 30 * mm, y + 18 * mm, M + 62 * mm, y + 18 * mm,
              HexColor("#9AA3AF"), 1)
        texto(c, M + 46 * mm, y + 13 * mm, "assinatura", 7.5, FONT, SOFT, "c")

    # linha de corte
    yy = H - M - alt - 5 * mm
    linha(c, M, yy, W - M, yy, HexColor("#B9C0C9"), 0.8, dash=[4, 4])
    rodape(c, pag, total, "Certificados • recorte no meio da folha")


def cartoes_pausa(c, pag, total):
    """Cartões de pausa/elogio para recortar."""
    fundo(c)
    texto(c, W / 2, H - M - 8 * mm, "CARTÕES DE PAUSA E ELOGIO", 15, FONT_B, TEAL, "c")
    texto(c, W / 2, H - M - 15 * mm,
          "Recorte, dobre e deixe numa caixinha. Use durante a tarefa.", 9, FONT, SOFT, "c")
    cartoes = [
        ("😮‍💨", "PAUSA DE 1 MINUTO", "Levante, beba água, volte.", TEAL, TEAL_L),
        ("💪", "VOCÊ TENTOU!", "Errar faz parte. Tente de novo.", CORAL, CORAL_L),
        ("👀", "OLHA O COMEÇO", "A bolinha verde mostra onde começar.", BLUE, BLUE_L),
        ("✏️", "DEVAGAR", "Sem pressa. Letra bonita é letra calma.", PURPLE, PURPLE_L),
        ("🎉", "CONSEGUIU!", "Escolha um adesivo para o quadro.", AMBER, AMBER_L),
        ("🤝", "FAZ COMIGO", "Vamos fazer a primeira juntos.", GREEN, GREEN_L),
        ("⏱️", "FALTAM 2 MINUTOS", "Depois a gente para.", PINK, PINK_L),
        ("🧠", "OLHA SÓ ISSO", "Seu cérebro está aprendendo!", TEAL, TEAL_L),
    ]
    larg = W - 2 * M
    cols, rows = 2, 4
    cw = (larg - 6 * mm) / cols
    ch = (H - M - 22 * mm - M) / rows
    for i, (fig, tit, txt, cor, cor_l) in enumerate(cartoes):
        col, row = i % cols, i // cols
        x = M + col * (cw + 6 * mm)
        y = H - M - 22 * mm - (row + 1) * ch
        rrect(c, x, y + 1 * mm, cw, ch - 3 * mm, 8, cor_l, cor, 1.2)
        emoji(c, fig, x + 12 * mm, y + ch / 2 + 4 * mm, 13 * mm, cor)
        texto(c, x + 23 * mm, y + ch / 2 + 4 * mm, tit, 9, FONT_B, cor)
        for j, ln in enumerate(quebrar(txt, cw - 28 * mm, 8, FONT)):
            texto(c, x + 23 * mm, y + ch / 2 - 2 * mm - j * 4 * mm, ln, 8, FONT, INK)
    rodape(c, pag, total, "Cartões de apoio • recorte e use durante a tarefa")


def primeira_semana(c, pag, total):
    """Plano de impressão e uso da primeira semana."""
    fundo(c)
    topo = faixa_titulo(c, "COMECE AQUI — PRIMEIRA SEMANA",
                        "Imprima só estas páginas. O resto fica guardado.",
                        TEAL, TEAL_L, etiqueta="guia")
    larg = W - 2 * M
    y = topo - 5 * mm

    # 1. imprimir
    bloco_h = 58 * mm
    rrect(c, M, y - bloco_h, larg, bloco_h, 10, WHITE, LINE, 1)
    texto(c, M + 5 * mm, y - 8 * mm, "1. O QUE IMPRIMIR HOJE", 10, FONT_B, TEAL)
    itens = [
        ("01", "Capa + instruções", "p. 1 e 2 do caderno de letras"),
        ("01", "Folha da letra A", "p. 3 (uma só!)"),
        ("01", "Letras que se parecem", "p. 55 — leia você primeiro"),
        ("05", "Guia do adulto", "p. 1 a 5, para você ler"),
        ("05", "Quadro de conquistas", "p. 4 — cole na parede"),
    ]
    for i, (arq, o_que, det) in enumerate(itens):
        yy = y - 17 * mm - i * 8.2 * mm
        c.setFillColor(TEAL)
        c.roundRect(M + 6 * mm, yy - 2.4 * mm, 9 * mm, 5.6 * mm, 2, stroke=0, fill=1)
        texto(c, M + 10.5 * mm, yy - 1.2 * mm, arq, 5.8, FONT_B, WHITE, "c")
        texto(c, M + 17 * mm, yy, o_que, 8.6, FONT_B, INK)
        texto(c, M + 20 * mm + largura(o_que, 8.6, FONT_B), yy, "—", 8.6, FONT, SOFT)
        texto(c, M + 24 * mm + largura(o_que, 8.6, FONT_B), yy, det, 8, FONT, SOFT)

    # 2. rotina
    y2 = y - bloco_h - 5 * mm
    h2 = 36 * mm
    rrect(c, M, y2 - h2, larg, h2, 10, AMBER_L, None)
    texto(c, M + 5 * mm, y2 - 8 * mm, "2. A ROTINA DA SEMANA", 10, FONT_B, AMBER)
    dias = ["SEG", "TER", "QUA", "QUI", "SEX", "SÁB", "DOM"]
    tarefas = ["Letra A\ncolorir", "Letra A\ntraçar", "Letra A\ncaça-letra",
               "Letra A\nminúscula", "Jogo da\nmemória", "Revisão\nleve", "Descanso"]
    cw = (larg - 10 * mm) / 7
    for i, (d, t) in enumerate(zip(dias, tarefas)):
        x = M + 5 * mm + i * cw
        rrect(c, x + 0.8 * mm, y2 - h2 + 6 * mm, cw - 1.6 * mm, h2 - 16 * mm, 6,
              WHITE, HexColor("#E3D6BC"), 0.9)
        texto(c, x + cw / 2, y2 - h2 + h2 - 15 * mm, d, 7.6, FONT_B, AMBER, "c")
        for j, ln in enumerate(t.split("\n")):
            texto(c, x + cw / 2, y2 - h2 + 13 * mm - j * 4 * mm, ln, 7.0, FONT, INK, "c")

    # 3. o que observar
    y3 = y2 - h2 - 5 * mm
    h3 = y3 - M - 4 * mm
    rrect(c, M, M + 4 * mm, larg, h3, 10, HexColor("#F7F9FB"), LINE, 1)
    texto(c, M + 5 * mm, y3 - 8 * mm, "3. O QUE VOCÊ VAI OBSERVAR (e não cobrar)", 10,
          FONT_B, BLUE)
    obs = [
        ("Segunda", "Ela olhou a folha por mais de 2 minutos?"),
        ("Terça", "Ela acertou o traçado sem você apontar?"),
        ("Quarta", "Ela achou a letra A no caça-letra sozinha?"),
        ("Quinta", "Ela reconheceu a letra A em outra palavra (nome, placa, livro)?"),
        ("Sexta", "Ela pediu para jogar de novo?"),
    ]
    yy = y3 - 16 * mm
    for dia, txt in obs:
        texto(c, M + 5 * mm, yy, dia, 8.4, FONT_B, BLUE)
        linhas = quebrar(txt, larg - 32 * mm, 8.4, FONT)
        for j, ln in enumerate(linhas):
            texto(c, M + 24 * mm, yy - j * 3.9 * mm, ln, 8.4, FONT, INK)
        checkbox(c, W - M - 12 * mm, yy - 1.5 * mm, 5 * mm, HexColor("#B9C0C9"), 1)
        yy -= len(linhas) * 3.9 * mm + 2.6 * mm

    linha(c, M + 5 * mm, yy + 3 * mm, W - M - 5 * mm, yy + 3 * mm,
          HexColor("#DFE5EC"), 0.8)

    # 4. ambiente
    y4 = yy - 4 * mm
    texto(c, M + 5 * mm, y4, "4. PREPARE O AMBIENTE (5 MINUTOS, UMA VEZ SÓ)", 10,
          FONT_B, PURPLE)
    ambiente = [
        ("🪑", "Mesa livre", "Só o material do dia. Nada de brinquedo ou celular por perto."),
        ("💡", "Luz e postura", "Luz pela frente, pés apoiados, folha na altura do peito."),
        ("🔇", "Som constante", "Ruído branco ou música instrumental baixa ajudam mais que silêncio."),
        ("📦", "Caixa do dia", "Uma caixa com lápis, borracha, adesivos e o quadro de conquistas."),
    ]
    yy2 = y4 - 7 * mm
    for fig, tit, txt in ambiente:
        emoji(c, fig, M + 9 * mm, yy2 + 1 * mm, 6.5 * mm, PURPLE)
        texto(c, M + 16 * mm, yy2, tit + ":", 8.4, FONT_B, INK)
        texto(c, M + 16 * mm + largura(tit + ":", 8.4, FONT_B) + 2 * mm, yy2, txt,
              8.2, FONT, SOFT)
        yy2 -= 6.4 * mm
    # 5. combinado com a criança
    y5 = yy2 - 1 * mm
    rrect(c, M + 5 * mm, M + 26 * mm, larg - 10 * mm, y5 - M - 26 * mm, 8, AMBER_L, None)
    texto(c, M + 11 * mm, y5 - 8 * mm, "5. COMBINE COM ELA ANTES DE COMEÇAR", 9.5,
          FONT_B, AMBER)
    combo = [
        "Quanto tempo: “são 10 minutos, depois a gente para”.",
        "O que ganha: “no fim, você escolhe o adesivo”.",
        "Pode errar: “errar faz parte, eu não vou brigar”.",
        "Pode parar: “se cansar, fala que a gente para”.",
    ]
    meia = (larg - 22 * mm) / 2
    for i, t in enumerate(combo):
        col, row = i % 2, i // 2
        x = M + 11 * mm + col * meia
        yc = y5 - 15 * mm - row * 7 * mm
        c.setFillColor(AMBER)
        c.circle(x + 1 * mm, yc + 2.2 * mm, 1.2 * mm, stroke=0, fill=1)
        for j, ln in enumerate(quebrar(t, meia - 6 * mm, 8.2, FONT)):
            texto(c, x + 5 * mm, yc - j * 4.0 * mm, ln, 8.2, FONT, INK)
    texto(c, M + 5 * mm, M + 15 * mm,
          "Se a semana foi difícil, não recomece do zero: repita a mesma letra. Repetir é o método.",
          7.6, FONT_I, SOFT)
    rodape(c, pag, total, "Guia do adulto • comece por aqui")
