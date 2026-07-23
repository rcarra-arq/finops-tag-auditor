# A funcao: recebe UM recurso e a lista de tags obrigatorias,
# e DEVOLVE a lista das tags que estao faltando nesse recurso.
def tags_faltando(recurso, obrigatorias):
    faltando = []
    for tag in obrigatorias:
        if tag not in recurso["tags"]:
            faltando.append(tag)
    return faltando


# Este bloco so roda quando voce EXECUTA o arquivo (python auditor.py).
# Quando outro arquivo IMPORTA este (como o teste vai fazer), ele NAO roda.
if __name__ == "__main__":
    # Um EXEMPLO de recursos, no espirito do que a AWS devolve.
    recursos = [
        {"nome": "bucket-acervo-fotos", "tags": {"Project": "acervo", "Environment": "prod", "Owner": "rodrigo"}},
        {"nome": "bucket-teste-antigo", "tags": {}},
        {"nome": "vol-do-servidor",     "tags": {"Project": "acervo", "Environment": "prod"}},
    ]

    tags_obrigatorias = ["Project", "Environment", "Owner"]

    for recurso in recursos:
        faltando = tags_faltando(recurso, tags_obrigatorias)
        if faltando:
            print("FALTA", recurso["nome"], "-> faltam:", faltando)
        else:
            print("OK   ", recurso["nome"])
