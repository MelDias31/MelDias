# -*- coding: utf-8 -*-
"""Gera folhas de contato (miniaturas) para revisão visual dos PDFs."""
import sys
import os
import pymupdf
from PIL import Image

SAIDA = "/tmp/revisao"


def contato(caminho_pdf, prefixo, dpi=62, colunas=4):
    os.makedirs(SAIDA, exist_ok=True)
    doc = pymupdf.open(caminho_pdf)
    imagens = []
    for i in range(len(doc)):
        pix = doc[i].get_pixmap(dpi=dpi)
        imagens.append(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
    if not imagens:
        return []
    w, h = imagens[0].size
    linhas = (len(imagens) + colunas - 1) // colunas
    folha = Image.new("RGB", (colunas * (w + 10) + 10, linhas * (h + 10) + 10), "white")
    for i, im in enumerate(imagens):
        r, c = divmod(i, colunas)
        folha.paste(im, (10 + c * (w + 10), 10 + r * (h + 10)))
    saidas = []
    # divide em blocos de no máximo 8 miniaturas para leitura
    por_bloco = colunas * 3
    for b in range(0, len(imagens), por_bloco):
        sub = imagens[b:b + por_bloco]
        linhas = (len(sub) + colunas - 1) // colunas
        f = Image.new("RGB", (colunas * (w + 10) + 10, linhas * (h + 10) + 10), "white")
        for i, im in enumerate(sub):
            r, c = divmod(i, colunas)
            f.paste(im, (10 + c * (w + 10), 10 + r * (h + 10)))
        p = f"{SAIDA}/{prefixo}_{b // por_bloco}.png"
        f.save(p)
        saidas.append(p)
    return saidas


if __name__ == "__main__":
    pdf = sys.argv[1]
    pref = sys.argv[2] if len(sys.argv) > 2 else "pg"
    for p in contato(pdf, pref):
        print(p)
