# -*- coding: utf-8 -*-
"""Coletor de páginas: permite numerar 'x / total' com o total já conhecido."""
import os
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.pagesizes import A4

from base import PDF, metadados


class Doc:
    def __init__(self, arquivo, titulo, assunto):
        self.arquivo = arquivo
        self.titulo = titulo
        self.assunto = assunto
        self.paginas = []

    def add(self, fn, *args, **kwargs):
        self.paginas.append((fn, args, kwargs))

    def render(self):
        os.makedirs(PDF, exist_ok=True)
        caminho = os.path.join(PDF, self.arquivo)
        c = rl_canvas.Canvas(caminho, pagesize=A4, pageCompression=1)
        metadados(c, self.titulo, self.assunto)
        total = len(self.paginas)
        for i, (fn, args, kwargs) in enumerate(self.paginas, start=1):
            fn(c, i, total, *args, **kwargs)
            c.showPage()
        c.save()
        return caminho, total
