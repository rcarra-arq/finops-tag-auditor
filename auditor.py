# Um EXEMPLO de recursos, no espirito do que a AWS devolve.
# Cada recurso tem um nome e um conjunto de tags.
recursos = [
    {"nome": "bucket-acervo-fotos", "tags": {"Project": "acervo", "Environment": "prod", "Owner": "rodrigo"}},
    {"nome": "bucket-teste-antigo", "tags": {}},
    {"nome": "vol-do-servidor",     "tags": {"Project": "acervo", "Environment": "prod"}},
]

# A "checklist": as tags que TODO recurso deveria ter.
tags_obrigatorias = ["Project", "Environment", "Owner"]

# Laco de fora: passa por cada recurso.
for recurso in recursos:
    # Comeca com uma lista VAZIA; vamos guardar aqui as tags que faltam.
    faltando = []

    # Laco de dentro: se a tag NAO esta no recurso, adiciona na lista.
    for tag in tags_obrigatorias:
        if tag not in recurso["tags"]:
            faltando.append(tag)

    # Decide o que imprimir com base no que sobrou em "faltando".
    if faltando:
        print("FALTA", recurso["nome"], "-> faltam:", faltando)
    else:
        print("OK   ", recurso["nome"])
