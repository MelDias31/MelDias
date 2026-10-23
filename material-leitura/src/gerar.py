# -*- coding: utf-8 -*-
"""Gera todos os PDFs do Kit Ler sem Pressa (A4).

Uso:
    python src/gerar.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from base import registrar_fontes, PDF
from doc import Doc
import p_alfabeto as pa
import p_silabas as ps
import p_leitura as pl
import p_jogos as pj
import p_manual as pm
import p_cronograma as pc
from conteudo import (ALFABETO, ORDEM, FAMILIAS, COMPLEXAS, FRASES,
                      LIGUE, CACA)


def caderno_alfabeto():
    d = Doc("01-caderno-do-alfabeto.pdf", "Meu Alfabeto",
            "Cartilha A4 de alfabetização — 26 letras para colorir e traçar")
    d.add(pa.capa)
    d.add(pa.instrucoes)
    for L in ORDEM:
        d.add(pa.folha_letra, L)
    for L in ORDEM:
        d.add(pa.folha_letra_minuscula, L)
    d.add(pa.parecidas)
    d.add(pa.alfabeto_mural)
    d.add(pa.alfabeto_mural_2)
    d.add(pa.bingo_letras)
    d.add(pa.quadro_progresso)
    return d.render()


def caderno_silabas():
    d = Doc("02-silabas-e-palavras.pdf", "Sílabas e Palavras",
            "Famílias silábicas, sílabas complexas e escada de palavras")
    d.add(ps.capa)
    for f in FAMILIAS:
        d.add(ps.familia, f)
    for c in COMPLEXAS:
        d.add(ps.complexas, c)
    d.add(ps.niveis)
    d.add(ps.niveis2)
    d.add(ps.treino_leitura)
    return d.render()


def caderno_leitura():
    d = Doc("03-leitura-e-escrita.pdf", "Leitura e Escrita",
            "Frases, histórias curtas, ditado e folhas de escrita")
    d.add(pl.capa)
    for f in FRASES:
        d.add(pl.leitura_frases, f)
    d.add(pl.leitura_textos)
    d.add(pl.textos_2)
    d.add(pl.ditado_figuras)
    d.add(pl.ditado_figuras_2)
    for i in range(4):
        d.add(pl.escrita, i)
    d.add(pl.autoavaliacao)
    return d.render()


def caderno_jogos():
    d = Doc("04-jogos-e-fichas.pdf", "Jogos e Fichas",
            "Memória, bingo, trilha, ligue-ligue, caça-palavras e dominó")
    d.add(pj.capa_jogos)
    d.add(pj.instrucoes_jogos)
    d.add(pj.memoria, 0)
    d.add(pj.memoria, 1)
    d.add(pj.bingo)
    d.add(pj.bingo_fichas)
    d.add(pj.trilha)
    d.add(pj.trilha_fichas)
    for item in LIGUE:
        d.add(pj.ligue, item)
    for item in CACA:
        d.add(pj.caca_palavras, item)
    d.add(pj.caca_2)
    d.add(pj.caca_3)
    d.add(pj.domino)
    d.add(pj.domino_2)
    d.add(pj.forca)
    return d.render()


def guia_familia():
    d = Doc("05-guia-do-adulto.pdf", "Guia do Adulto",
            "Como ensinar uma criança com TDAH a ler — rotina, registro e certificados")
    d.add(pm.capa_kit)
    d.add(pm.primeira_semana)
    d.add(pm.guia_tdah)
    d.add(pm.rotina)
    d.add(pm.quadro_recompensas)
    d.add(pm.registro)
    d.add(pm.cartoes_pausa)
    d.add(pm.certificados)
    return d.render()


def cronograma():
    d = Doc("06-cronograma-4-semanas.pdf", "Cronograma de 4 Semanas",
            "Plano dia a dia do primeiro mês — o que fazer e o que imprimir")
    d.add(pc.capa)
    d.add(pc.lista_impressao)
    for n in range(4):
        d.add(pc.semana, n)
    d.add(pc.depois)
    return d.render()


def main():
    registrar_fontes()
    os.makedirs(PDF, exist_ok=True)
    for fn in (caderno_alfabeto, caderno_silabas, caderno_leitura,
               caderno_jogos, guia_familia, cronograma):
        caminho, total = fn()
        print(f"{os.path.basename(caminho):32s} {total:3d} páginas")


if __name__ == "__main__":
    main()
