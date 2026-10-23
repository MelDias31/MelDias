# -*- coding: utf-8 -*-
"""Junta os 6 cadernos em um único PDF, com sumário e marcadores.

Uso:
    python src/juntar.py            (depois de rodar src/gerar.py)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pymupdf
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.pagesizes import A4

from base import (W, H, M, INK, SOFT, WHITE, LINE, TEAL, TEAL_L, AMBER, AMBER_L,
                  BLUE, BLUE_L, PURPLE, PURPLE_L, GREEN, GREEN_L, HexColor,
                  FONT, FONT_B, FONT_I, texto, quebrar, rrect, linha,
                  faixa_titulo, rodape, fundo, registrar_fontes, PDF, metadados)

ARQUIVO = "00-kit-ler-sem-pressa-completo.pdf"

CADERNOS = [
    ("01", "01-caderno-do-alfabeto.pdf", "Meu alfabeto", "criança",
     "26 letras para colorir, traçar e achar · maiúsculas e minúsculas · mural · bingo", TEAL, TEAL_L),
    ("02", "02-silabas-e-palavras.pdf", "Sílabas e palavras", "criança",
     "15 famílias silábicas · 9 grupos complexos · escada de palavras · leitura rápida", BLUE, BLUE_L),
    ("03", "03-leitura-e-escrita.pdf", "Leitura e escrita", "criança",
     "5 níveis de frases · histórias curtas · ditado de figuras · folhas de escrita", PURPLE, PURPLE_L),
    ("04", "04-jogos-e-fichas.pdf", "Jogos e fichas", "família",
     "memória · bingo · trilha · ligue-ligue · caça-palavras · dominó · forca", AMBER, AMBER_L),
    ("05", "05-guia-do-adulto.pdf", "Guia do adulto", "adulto",
     "guia TDAH · rotina de 10 min · quadro de conquistas · registro · certificado", GREEN, GREEN_L),
    ("06", "06-cronograma-do-alfabeto.pdf", "Cronograma do alfabeto", "adulto",
     "13 semanas, 2 letras por semana · dia a dia · o que observar · se ela travar", HexColor("#6F5E86"), PURPLE_L),
]


def paginas():
    """Confere os arquivos e devolve a lista com o número de páginas."""
    out = []
    for cod, arq, nome, quem, desc, cor, cor_l in CADERNOS:
        caminho = os.path.join(PDF, arq)
        if not os.path.exists(caminho):
            raise SystemExit(f"Falta o arquivo {arq}. Rode: python src/gerar.py")
        n = pymupdf.open(caminho).page_count
        out.append(dict(cod=cod, arq=arq, caminho=caminho, nome=nome, quem=quem,
                        desc=desc, cor=cor, cor_l=cor_l, n=n))
    return out


def sumario(c, itens):
    """Página de abertura do arquivo único."""
    fundo(c)
    total_kit = sum(i["n"] for i in itens) + 1
    topo = faixa_titulo(c, "KIT LER SEM PRESSA — ARQUIVO COMPLETO",
                        "Os 6 cadernos em um só PDF, na ordem de uso.",
                        TEAL, TEAL_L, etiqueta="arquivo único")
    larg = W - 2 * M
    y = topo - 6 * mm

    rrect(c, M, y - 20 * mm, larg, 20 * mm, 10, WHITE, LINE, 1)
    texto(c, M + 6 * mm, y - 7.4 * mm, "COMO USAR ESTE ARQUIVO", 9.0, FONT_B, TEAL)
    para = ("Cada caderno começa numa página nova e mantém a numeração própria no rodapé "
            "(por exemplo, “12 / 59”). O número grande ao lado de cada título é a página "
            "deste arquivo único, para achar rápido no celular ou na impressora.")
    for j, ln in enumerate(quebrar(para, larg - 12 * mm, 8.8, FONT)):
        texto(c, M + 6 * mm, y - 13.2 * mm - j * 4.0 * mm, ln, 8.8, FONT, INK)
    y -= 25 * mm

    texto(c, M, y, "O QUE TEM AQUI DENTRO", 9.6, FONT_B, TEAL)
    y -= 7.2 * mm

    # cabeçalho da tabela
    h_cab = 6.0 * mm
    rrect(c, M, y - h_cab, larg, h_cab, 3, HexColor("#EFF3F6"), None)
    texto(c, M + 4 * mm, y - 4.1 * mm, "PÁG.", 7.4, FONT_B, SOFT)
    texto(c, M + 22 * mm, y - 4.1 * mm, "CADERNO", 7.4, FONT_B, SOFT)
    texto(c, W - M - 4 * mm, y - 4.1 * mm, "PARA", 7.4, FONT_B, SOFT, "r")
    y -= h_cab

    h_lin = 19.5 * mm
    for i, it in enumerate(itens):
        if i % 2 == 0:
            c.setFillColor(HexColor("#FBFCFD"))
            c.rect(M, y - h_lin, larg, h_lin, stroke=0, fill=1)
        # selo com o código
        rrect(c, M + 3 * mm, y - 11.6 * mm, 11 * mm, 8.0 * mm, 2.4, it["cor_l"], None)
        texto(c, M + 8.5 * mm, y - 9.5 * mm, it["cod"], 8.4, FONT_B, it["cor"], "c")
        # nome e descrição
        texto(c, M + 18 * mm, y - 6.4 * mm, it["nome"], 11, FONT_B, INK)
        desc = it["desc"]
        for j, ln in enumerate(quebrar(desc, larg - 30 * mm, 8.4, FONT)):
            texto(c, M + 18 * mm, y - 10.4 * mm - j * 3.9 * mm, ln, 8.4, FONT, SOFT)
        # páginas e público
        texto(c, W - M - 4 * mm, y - 6.4 * mm,
              f"p. {it['inicio']}–{it['fim']}", 8.6, FONT_B, it["cor"], "r")
        texto(c, W - M - 4 * mm, y - 11.0 * mm, f"{it['n']} páginas", 7.8, FONT, SOFT, "r")
        texto(c, W - M - 4 * mm, y - 15.0 * mm, it["quem"], 7.8, FONT_I, SOFT, "r")
        linha(c, M, y - h_lin, W - M, y - h_lin, HexColor("#EDF0F4"), 0.8)
        y -= h_lin

    y -= 7 * mm

    # ordem de leitura sugerida
    rrect(c, M, y - 34 * mm, larg, 34 * mm, 10, AMBER_L, None)
    texto(c, M + 6 * mm, y - 8 * mm, "POR ONDE COMEÇAR", 9.2, FONT_B, AMBER)
    passos = [
        ("1", "Leia o guia do adulto",
         "páginas " + _faixa(itens, "05", 1, 5) + " — leva 5 minutos"),
        ("2", "Siga o cronograma",
         "a lista de impressão está na página " + _pnum(itens, "06", 2)),
        ("3", "Imprima só a semana 1",
         "o dia a dia começa na página " + _pnum(itens, "06", 3)),
    ]
    yy = y - 16.0 * mm
    for n, t, d in passos:
        c.setFillColor(AMBER)
        c.circle(M + 9 * mm, yy + 3.2 * mm, 3.2 * mm, stroke=0, fill=1)
        texto(c, M + 9 * mm, yy + 2.2 * mm, n, 7.8, FONT_B, WHITE, "c")
        texto(c, M + 15 * mm, yy + 3.4 * mm, t, 9.0, FONT_B, INK)
        texto(c, M + 15 * mm, yy - 0.6 * mm, d, 8.4, FONT, SOFT)
        yy -= 9.2 * mm

    y -= 44 * mm

    rrect(c, M, y - 22 * mm, larg, 22 * mm, 9, TEAL_L, None)
    texto(c, M + 6 * mm, y - 7.6 * mm, "O QUE ESTE ARQUIVO NÃO É", 9.0, FONT_B, TEAL)
    aviso = ("Material de apoio pedagógico. Não substitui avaliação ou tratamento médico, "
             "fonoaudiológico ou psicopedagógico. Se a dificuldade persistir, procure um "
             "profissional e leve três folhas feitas pela criança.")
    for j, ln in enumerate(quebrar(aviso, larg - 12 * mm, 8.6, FONT)):
        texto(c, M + 6 * mm, y - 13.2 * mm - j * 3.9 * mm, ln, 8.6, FONT, INK)

    # rodapé próprio do arquivo
    yy = M - 6
    linha(c, M, yy + 9, W - M, yy + 9, HexColor("#E4E7EC"), 0.8)
    texto(c, M, yy - 1, "Kit Ler sem Pressa • arquivo único • uso livre em casa e na escola",
          7.5, FONT, SOFT)
    texto(c, W - M, yy - 1, f"1 / {total_kit}", 8, FONT_B, SOFT, "r")


def _p(itens, cod, pag):
    for it in itens:
        if it["cod"] == cod:
            return f"página {it['inicio'] + pag - 1}"
    return ""


def _pnum(itens, cod, pag):
    for it in itens:
        if it["cod"] == cod:
            return str(it["inicio"] + pag - 1)
    return ""


def _faixa(itens, cod, a, b):
    for it in itens:
        if it["cod"] == cod:
            return f"{it['inicio'] + a - 1} a {it['inicio'] + b - 1}"
    return ""


def main():
    registrar_fontes()
    itens = paginas()

    # numera as páginas de cada caderno dentro do arquivo único
    p = 2  # a página 1 é o sumário
    for it in itens:
        it["inicio"] = p
        it["fim"] = p + it["n"] - 1
        p += it["n"]

    # 1. sumário em PDF temporário
    tmp = os.path.join(PDF, "_sumario.pdf")
    c = rl_canvas.Canvas(tmp, pagesize=A4, pageCompression=1)
    metadados(c, "Kit Ler sem Pressa — arquivo completo",
              "Os 6 cadernos do kit em um único PDF A4")
    sumario(c, itens)
    c.showPage()
    c.save()

    # 2. junta tudo
    saida = pymupdf.open()
    saida.insert_pdf(pymupdf.open(tmp))
    for it in itens:
        saida.insert_pdf(pymupdf.open(it["caminho"]))

    # 3. marcadores (índice lateral do leitor de PDF)
    toc = [[1, "Sumário e como usar", 1]]
    for it in itens:
        toc.append([1, f"{it['cod']} — {it['nome']}", it["inicio"]])
    # semanas do cronograma
    cro = next(i for i in itens if i["cod"] == "06")
    for n in range(13):
        toc.append([2, f"Semana {n + 1}", cro["inicio"] + 2 + n])
    toc.append([2, "Depois das 13 semanas", cro["fim"]])
    toc.sort(key=lambda e: e[2])
    # reordena respeitando a hierarquia: recalcula em duas passagens
    toc = _hierarquia(toc)
    saida.set_toc(toc)

    saida.set_metadata({
        "title": "Kit Ler sem Pressa — material completo",
        "author": "Material de apoio à alfabetização",
        "subject": "Alfabetização A4 para criança com TDAH — 6 cadernos em um só PDF",
        "keywords": "alfabetização, TDAH, A4, sílabas, jogos, cronograma",
        "creator": "Kit Ler sem Pressa",
    })
    destino = os.path.join(PDF, ARQUIVO)
    saida.save(destino, garbage=3, deflate=True)
    saida.close()
    os.remove(tmp)

    d = pymupdf.open(destino)
    print(f"{ARQUIVO}  {d.page_count} páginas  "
          f"{os.path.getsize(destino) / 1e6:.1f} MB")
    for it in itens:
        print(f"  {it['cod']}  p. {it['inicio']:3d}–{it['fim']:3d}  {it['nome']}")


def _hierarquia(toc):
    """Garante que cada nível 2 venha depois do seu nível 1."""
    saida, atual = [], None
    nivel1 = [e for e in toc if e[0] == 1]
    nivel2 = [e for e in toc if e[0] == 2]
    for e1 in nivel1:
        saida.append(e1)
        prox = nivel1[nivel1.index(e1) + 1][2] if nivel1.index(e1) + 1 < len(nivel1) else 10 ** 6
        for e2 in nivel2:
            if e1[2] < e2[2] < prox:
                saida.append(e2)
    return saida


if __name__ == "__main__":
    main()
