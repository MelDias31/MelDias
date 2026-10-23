# Kit Ler sem Pressa

Material completo de alfabetização em **PDF A4** para uma criança de 6 anos com **TDAH** e
dificuldade de memorizar as letras. Feito para ser usado **10 minutos por dia**, em casa,
por quem não é professor.

**5 cadernos · 126 páginas · ~14 MB · tudo em A4 (210 × 297 mm)**

---

## O que tem dentro

| Arquivo | Páginas | Para quem | Conteúdo |
|---|---|---|---|
| **01-caderno-do-alfabeto.pdf** | 59 | criança | Capa, instruções, **26 folhas de letras** (colorir + traçar + caça-letra), **26 folhas de minúsculas**, letras que se parecem, mural do alfabeto, bingo de letras, mapa das 26 letras |
| **02-silabas-e-palavras.pdf** | 28 | criança | **15 famílias silábicas** (BA BE BI BO BU…), **9 grupos complexos** (CH, LH, NH, RR, SS, ÃO, CE/CI, GE/GI, QU/GU), escada de palavras, leitura rápida |
| **03-leitura-e-escrita.pdf** | 15 | criança | **5 níveis de frases**, 6 histórias curtas, ditado de figuras, folhas de escrita, autoavaliação |
| **04-jogos-e-fichas.pdf** | 16 | família | Memória, bingo (6 cartelas + fichas), trilha com dado e peões, ligue-ligue, 3 caça-palavras, dominó de sílabas, forca |
| **05-guia-do-adulto.pdf** | 8 | adulto | **Comece aqui**, guia TDAH (o que ajuda / o que atrapalha), rotina de 10 min, quadro de conquistas, registro de progresso, cartões de pausa, certificados |

---

## Como começar (hoje)

1. Imprima **apenas** as páginas 1 e 2 do caderno 01 + a **folha da letra A** (página 3) +
   as páginas 1 a 5 do caderno **05**.
2. Leia o **guia do adulto** (5 minutos de leitura). Ele explica a rotina.
3. Cole o **quadro de conquistas** na parede.
4. Sente-se ao lado, use **10 minutos**, e pare antes do cansaço.

A página **"Comece aqui — primeira semana"** (página 2 do guia) traz o plano dia a dia.

### Por que essa ordem de letras

Não comece pelo alfabeto em ordem. Comece pelo **nome dela**, depois vogais
(A, E, I, O, U), depois as consoantes de som regular e forma simples
(M, P, B, D, T, L, C, S, R, N, F, V, G, J, Z) e só no fim **X, Q, H, K, W, Y**.

---

## O que torna o material adequado ao TDAH

- **Uma tarefa por página.** Nada de três exercícios competindo na mesma folha.
- **10 minutos por dia**, com começo e fim previsíveis.
- **Instruções numeradas** (1, 2, 3) com no máximo 12 palavras.
- **Marcador verde** de onde começar e **setas** indicando a direção do traço.
- **Repetição com variação:** a mesma letra aparece para colorir, tracejar, pontilhar e
  procurar — repetir sem tédio.
- **Letras parecidas lado a lado** (b/d, p/q, m/n, u/v), porque é ali que a criança troca.
- **Caça-letra com distratores parecidos**, treinando a discriminação visual.
- **Elogio ao esforço**, nunca nota ou comparação.
- **Figura-âncora** para cada letra: a imagem ajuda a memória, que é o ponto fraco.

---

## Impressão

- Papel **A4**, retrato, **100% de escala** (desmarque "ajustar à página").
- **Preto e branco funciona**: as páginas foram desenhadas para continuar legíveis sem cor.
  Imprimir colorido ajuda, mas não é obrigatório.
- Jogos: cole em cartolina antes de recortar, para durar mais.
- Sugestão: imprima os cadernos 01 e 02 em **frente e verso** e encaderne; os jogos
  (04) e o guia (05) imprima em **folhas soltas**.

---

## O que observar (sinais para buscar avaliação)

Leve este material e 3 folhas feitas pela criança ao fonoaudiólogo, neuropediatra ou
psicopedagogo se notar:

- troca de letras parecidas de forma **insistente**, mesmo depois de muito treino;
- leitura que não evolui há meses;
- troca de sons na fala, sílabas sumindo;
- choro, recusa ou fala de "não consigo" diante da tarefa;
- dificuldade que já existia antes da alfabetização e não melhora.

Este material é **apoio pedagógico** e não substitui diagnóstico ou tratamento.

---

## Regenerar os PDFs

```bash
python3 -m venv .venv
.venv/bin/pip install reportlab fonttools pillow pymupdf
.venv/bin/python material-leitura/src/gerar.py
```

O gerador é determinístico: rodar de novo produz exatamente os mesmos arquivos.
As fontes usadas (Andika, SIL OFL; Noto Emoji, Apache 2.0) já estão em `fontes/`.

O prompt completo usado para definir o material está em [`PROMPT.md`](PROMPT.md).
