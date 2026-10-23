# -*- coding: utf-8 -*-
"""Conteúdo pedagógico: alfabeto, palavras-âncora, sílabas, frases e jogos."""

# letra -> (palavra-âncora, emoji, cor_idx, "som/letra" dica)
ALFABETO = {
    "A": ("ABELHA",     "🐝", 4),
    "B": ("BOLA",       "⚽", 1),
    "C": ("CASA",       "🏠", 2),
    "D": ("DADO",       "🎲", 3),
    "E": ("ELEFANTE",   "🐘", 5),
    "F": ("FLOR",       "🌸", 6),
    "G": ("GATO",       "🐱", 0),
    "H": ("HELICÓPTERO","🚁", 2),
    "I": ("ILHA",       "🏝️", 1),
    "J": ("JACARÉ",     "🐊", 5),
    "K": ("KIWI",       "🥝", 4),
    "L": ("LUA",        "🌙", 3),
    "M": ("MAÇÃ",       "🍎", 1),
    "N": ("NAVIO",      "🚢", 2),
    "O": ("OVO",        "🥚", 4),
    "P": ("PATO",       "🦆", 0),
    "Q": ("QUEIJO",     "🧀", 4),
    "R": ("RATO",       "🐭", 6),
    "S": ("SOL",        "☀️", 4),
    "T": ("TARTARUGA",  "🐢", 5),
    "U": ("UVA",        "🍇", 3),
    "V": ("VACA",       "🐄", 2),
    "W": ("WAFFLE",     "🧇", 4),
    "X": ("XÍCARA",     "☕", 1),
    "Y": ("YOGA",       "🧘", 6),
    "Z": ("ZEBRA",      "🦓", 3),
}

# Ordem de ensino (não é a ordem alfabética): vogais, consoantes regulares
# e, por último, as letras de uso raro ou som irregular.
ORDEM = "AEIOUMPBDTLCSRNFVGJZXQHKWY"

# Ordem alfabética: usada no mural da parede e no bingo (só como repertório).
ALFABETO_AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Rima/apoio de memória: "B de bola, b de bola"
DICA_LETRA = {
    "A": "A de ABELHA. A letra A tem duas pernas e um degrau no meio.",
    "B": "B de BOLA. A letra B tem uma barriga em cima e outra embaixo.",
    "C": "C de CASA. O C é uma meia-lua aberta para a direita.",
    "D": "D de DADO. O D é uma barriga grande com uma reta do lado.",
    "E": "E de ELEFANTE. O E é uma reta com três braços.",
    "F": "F de FLOR. O F é uma reta com dois braços.",
    "G": "G de GATO. O G é o C que ganhou um degrau.",
    "H": "H de HELICÓPTERO. O H são duas retas com uma ponte no meio.",
    "I": "I de ILHA. O I é uma reta sozinha, com um chapéu e um pé.",
    "J": "J de JACARÉ. O J desce e faz uma curva para a esquerda.",
    "K": "K de KIWI. O K tem uma reta e dois braços abertos.",
    "L": "L de LUA. O L desce e faz um pé para a direita.",
    "M": "M de MAÇÃ. O M são duas montanhas.",
    "N": "N de NAVIO. O N são duas retas com uma ponte inclinada.",
    "O": "O de OVO. O O é uma bolinha fechada, começa no topo.",
    "P": "P de PATO. O P tem uma barriga só, em cima.",
    "Q": "Q de QUEIJO. O Q é o O com um rabinho.",
    "R": "R de RATO. O R é o P com uma perna.",
    "S": "S de SOL. O S é uma cobrinha.",
    "T": "T de TARTARUGA. O T tem um chapéu em cima.",
    "U": "U de UVA. O U é um copo sem tampa.",
    "V": "V de VACA. O V é um vale fundo.",
    "W": "W de WAFFLE. O W são dois V juntos.",
    "X": "X de XÍCARA. O X é um cruzamento.",
    "Y": "Y de YOGA. O Y é um V com uma perna embaixo.",
    "Z": "Z de ZEBRA. O Z é um raio.",
}

# Sílabas simples (consoante + vogal) por família
FAMILIAS = [
    ("B", "BA BE BI BO BU", [("BOLA", "⚽", "BO"), ("BALA", "🍬", "BA"),
                             ("BICO", "🐦", "BI"), ("BODE", "🐐", "BO")]),
    ("C", "CA CO CU", [("CASA", "🏠", "CA"), ("COELHO", "🐰", "CO"),
                       ("CUBO", "🧊", "CU"), ("COCO", "🥥", "CO")]),
    ("D", "DA DE DI DO DU", [("DADO", "🎲", "DA"), ("DEDO", "👆", "DE"),
                             ("DIA", "☀️", "DI"), ("DOCE", "🍬", "DO")]),
    ("F", "FA FE FI FO FU", [("FACA", "🔪", "FA"), ("FADA", "🧚", "FA"),
                             ("FOGO", "🔥", "FO"), ("FITA", "🎀", "FI")]),
    ("G", "GA GO GU", [("GATO", "🐱", "GA"), ("GALO", "🐔", "GA"),
                       ("GOTA", "💧", "GO"), ("GUDE", "🧩", "GU")]),
    ("J", "JA JE JI JO JU", [("JACARÉ", "🐊", "JA"), ("JANELA", "🪟", "JA"),
                             ("JIPE", "🚙", "JI"), ("JOGO", "🎮", "JO")]),
    ("L", "LA LE LI LO LU", [("LUA", "🌙", "LU"), ("LATA", "🥫", "LA"),
                             ("LEÃO", "🦁", "LE"), ("LIVRO", "📖", "LI")]),
    ("M", "MA ME MI MO MU", [("MAÇÃ", "🍎", "MA"), ("MALA", "🧳", "MA"),
                             ("MEL", "🍯", "ME"), ("MOLA", "🧷", "MO")]),
    ("N", "NA NE NI NO NU", [("NAVIO", "🚢", "NA"), ("NUVEM", "☁️", "NU"),
                             ("NINHO", "🪹", "NI"), ("NOVE", "9", "NO")]),
    ("P", "PA PE PI PO PU", [("PATO", "🦆", "PA"), ("PÃO", "🍞", "PÃO"),
                             ("PIPA", "🪁", "PI"), ("POTE", "🍯", "PO")]),
    ("R", "RA RE RI RO RU", [("RATO", "🐭", "RA"), ("RODA", "🛞", "RO"),
                             ("RIO", "🏞️", "RI"), ("REMÉDIO", "💊", "RE")]),
    ("S", "SA SE SI SO SU", [("SAPO", "🐸", "SA"), ("SINO", "🔔", "SI"),
                             ("SOPA", "🍲", "SO"), ("SUCO", "🧃", "SU")]),
    ("T", "TA TE TI TO TU", [("TATU", "🦡", "TA"), ("TETO", "🏠", "TE"),
                             ("TIGRE", "🐯", "TI"), ("TOCA", "🕳️", "TO")]),
    ("V", "VA VE VI VO VU", [("VACA", "🐄", "VA"), ("VELA", "🕯️", "VE"),
                             ("VILA", "🏘️", "VI"), ("VOVÓ", "👵", "VO")]),
    ("Z", "ZA ZE ZI ZO ZU", [("ZEBRA", "🦓", "ZE"), ("ZERO", "0", "ZE"),
                             ("ZINCO", "🔩", "ZI"), ("ZOOLÓGICO", "🦁", "ZO")]),
]


# Letras que se parecem: (letra, dica de memória)
PARECIDAS = [
    ("b", "A barriga do B fica do lado DIREITO. O pauzinho fica atrás.", "⚽"),
    ("d", "A barriga do D fica do lado ESQUERDO. Parece a boca de um cachorro virada para trás.", "🐶"),
    ("p", "O P tem a barriga em CIMA e o pauzinho desce.", "🦆"),
    ("q", "O Q tem a barriga em CIMA e um rabinho na direita.", "🧀"),
]

# Frases curtas por nível (com figura de apoio)
FRASES = [
    ("Nível 1 — sílabas", [
        ("BÁ", "BA", "🐑"), ("BÊ", "BE", "🍼"), ("BÁ-BÁ", "ba ba", "🐑"),
        ("O BOI", "o boi", "🐂"), ("A UVA", "a uva", "🍇"),
        ("O OVO", "o ovo", "🥚"), ("A BOLA", "a bola", "⚽"),
    ]),
    ("Nível 2 — palavras de 2 sílabas", [
        ("O GATO", "o gato", "🐱"), ("A CASA", "a casa", "🏠"),
        ("O PATO", "o pato", "🦆"), ("A LUA", "a lua", "🌙"),
        ("O SAPO", "o sapo", "🐸"), ("A MALA", "a mala", "🧳"),
    ]),
    ("Nível 3 — com artigo e cor", [
        ("O GATO É PRETO.", "o gato é preto", "🐱"),
        ("A BOLA É AZUL.", "a bola é azul", "⚽"),
        ("O SOL É AMARELO.", "o sol é amarelo", "☀️"),
        ("A FLOR É ROSA.", "a flor é rosa", "🌸"),
    ]),
    ("Nível 4 — frases com ação", [
        ("O MENINO PULA.", "o menino pula", "🧒"),
        ("A MENINA CANTA.", "a menina canta", "🎤"),
        ("O CACHORRO CORRE.", "o cachorro corre", "🐶"),
        ("O PEIXE NADA.", "o peixe nada", "🐟"),
    ]),
    ("Nível 5 — duas frases", [
        ("O GATO SOBE NA MESA.\nELE QUER O PEIXE.", "o gato sobe na mesa. ele quer o peixe.", "🐱"),
        ("A MENINA TEM UMA BOLA.\nELA JOGA COM O PAI.", "a menina tem uma bola. ela joga com o pai.", "⚽"),
        ("O PATO ESTÁ NO LAGO.\nELE NADA MUITO BEM.", "o pato está no lago. ele nada muito bem.", "🦆"),
    ]),
]

# Palavras para caça-palavras / bingo
BINGO_POOL = [
    ("BOLA", "⚽"), ("CASA", "🏠"), ("GATO", "🐱"), ("PATO", "🦆"),
    ("LUA", "🌙"), ("SOL", "☀️"), ("MALA", "🧳"), ("UVA", "🍇"),
    ("FLOR", "🌸"), ("PEIXE", "🐟"), ("DADO", "🎲"), ("OVO", "🥚"),
    ("SAPO", "🐸"), ("NAVIO", "🚢"), ("MEL", "🍯"), ("PÃO", "🍞"),
]


# ------------------------------------------------------------------ jogos
# Pares para o jogo da memória (figura x palavra)
MEMORIA = [
    ("BOLA", "⚽"), ("CASA", "🏠"), ("GATO", "🐱"), ("PATO", "🦆"),
    ("LUA", "🌙"), ("SOL", "☀️"), ("MALA", "🧳"), ("UVA", "🍇"),
    ("FLOR", "🌸"), ("PEIXE", "🐟"), ("DADO", "🎲"), ("OVO", "🥚"),
]

# Caça-palavras: (título, palavras, grade montada à mão, dicas com figura)
CACA = [
    ("Letras e sílabas soltas", ["BOLA", "CASA", "GATO", "PATO", "LUA", "SOL"],
     [list("BOLACASA"), list("XGATOPATO"), list("LUASOLMAL"),
      list("DADEOVOUV"), list("FLORPEIXE"), list("BOLAMALA")],
     [("BOLA", "⚽"), ("CASA", "🏠"), ("GATO", "🐱"), ("SOL", "☀️")]),
]

# Ligue a figura à palavra
LIGUE = [
    [("BOLA", "⚽"), ("CASA", "🏠"), ("GATO", "🐱"), ("FLOR", "🌸"),
     ("LUA", "🌙"), ("PATO", "🦆")],
    [("UVA", "🍇"), ("PEIXE", "🐟"), ("DADO", "🎲"), ("SOL", "☀️"),
     ("MALA", "🧳"), ("OVO", "🥚")],
    [("SAPO", "🐸"), ("NAVIO", "🚢"), ("MEL", "🍯"), ("BORBOLETA", "🦋"),
     ("CACHORRO", "🐶"), ("TARTARUGA", "🐢")],
]

# Palavras para o dominó de sílabas
DOMINO = ["BA", "BE", "BI", "BO", "BU", "CA", "CO", "CU", "DA", "DE",
          "DI", "DO", "DU", "FA", "FE", "FI", "FO", "FU",
          "GA", "GO", "GU", "LA", "LE", "LI", "LO", "LU",
          "MA", "ME", "MI", "MO", "MU", "NA", "NE", "NI", "NO", "NU",
          "PA", "PE", "PI", "PO", "PU", "RA", "RE", "RI", "RO", "RU",
          "SA", "SE", "SI", "SO", "SU", "TA", "TE", "TI", "TO", "TU",
          "VA", "VE", "VI", "VO", "VU"]

# Trilha da leitura: casas especiais
TRILHA = [
    ("BA", 0), ("LE", 0), ("CA", 0), ("", 2), ("SA", 0),
    ("TO", 0), ("DA", 0), ("", 1), ("LA", 0), ("", 3),
    ("MA", 0), ("PO", 0), ("", 2), ("NE", 0), ("GA", 0),
    ("VA", 0), ("", 2), ("RI", 0), ("FI", 0), ("", 3),
    ("BO", 0), ("", 2), ("CU", 0), ("DE", 0), ("FO", 0),
    ("TE", 0),
]
# 26 casas (uma por letra do alfabeto) + a casa de CHEGADA, desenhada pelo tabuleiro.

# Sílabas complexas
COMPLEXAS = [
    ("CH", "CHA CHE CHI CHO CHU", [("CHUVA", "🌧️"), ("CHAVE", "🔑"),
                                   ("CHÁ", "☕"), ("CHUCHU", "🥒")]),
    ("LH", "LHA LHE LHI LHO LHU", [("MALHA", "🧶"), ("VELHO", "👴"),
                                   ("FILHO", "👦"), ("OLHO", "👁️")]),
    ("NH", "NHA NHE NHI NHO NHU", [("BANHO", "🛁"), ("NINHO", "🪹"),
                                   ("PINHA", "🌰"), ("GALINHA", "🐔")]),
    ("R / RR", "RA RE RI RO RU  /  RRA RRE RRI RRO RRU",
     [("RATO", "🐭"), ("CARRO", "🚗"), ("PORTA", "🚪"), ("FERRO", "🔩")]),
    ("S / SS", "SA SE SI SO SU  /  SSA SSE SSI SSO SSU",
     [("SAPO", "🐸"), ("PASSO", "👣"), ("SOPA", "🍲"), ("OSSO", "🦴")]),
    ("ÃO / ÃE", "ÃO  ÃE  ÕE", [("PÃO", "🍞"), ("MÃE", "👩"),
                               ("CORAÇÃO", "❤️"), ("LIMÃO", "🍋")]),
    ("CE / CI", "CE  CI", [("CEBOLA", "🧅"), ("CIDADE", "🏙️"),
                           ("CESTA", "🧺"), ("CINEMA", "🎬")]),
    ("GE / GI", "GE  GI", [("GELO", "🧊"), ("GIRAFA", "🦒"),
                           ("GEMA", "🥚"), ("GILETE", "🪒")]),
    ("QU / GU", "QUA QUE QUI QUO  /  GUA GUE GUI GUO",
     [("QUEIJO", "🧀"), ("QUATRO", "4"), ("GUITARRA", "🎸"), ("ÁGUIA", "🦅")]),
]

# Palavras por número de sílabas (para ditado/leitura)
NIVEIS_PALAVRAS = [
    ("2 sílabas", [("BOLA", "⚽"), ("CASA", "🏠"), ("GATO", "🐱"), ("PATO", "🦆"),
                   ("MALA", "🧳"), ("UVA", "🍇"), ("FACA", "🔪"), ("DEDO", "👆")]),
    ("3 sílabas", [("SAPATO", "👟"), ("BANANA", "🍌"), ("CAVALO", "🐴"),
                   ("JANELA", "🪟"), ("CAMISA", "👕"), ("PIPOCA", "🍿")]),
    ("4 sílabas", [("BORBOLETA", "🦋"), ("JACARÉ", "🐊"), ("TARTARUGA", "🐢"),
                   ("ELEFANTE", "🐘"), ("GELADEIRA", "🧊")]),
]
