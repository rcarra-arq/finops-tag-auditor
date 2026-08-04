import argparse
import sys


# A funcao: recebe UM recurso e a lista de tags obrigatorias,
# e DEVOLVE a lista das tags que estao faltando nesse recurso.
def tags_faltando(recurso, obrigatorias):
    faltando = []
    for tag in obrigatorias:
        if tag not in recurso["tags"]:
            faltando.append(tag)
    return faltando


# Fonte de dados 1: um EXEMPLO fixo, no espirito do que a AWS devolve.
# Serve para rodar sem internet e para o CI (que nao tem credencial AWS).
def recursos_de_exemplo():
    return [
        {"nome": "bucket-acervo-fotos", "tags": {"Project": "acervo", "Environment": "prod", "Owner": "rodrigo"}},
        {"nome": "bucket-teste-antigo", "tags": {}},
        {"nome": "vol-do-servidor",     "tags": {"Project": "acervo", "Environment": "prod"}},
        # Um recurso do servico 'payments' (cartao salvo). A Tagging API lista,
        # mas a AWS nao deixa colocar tags -> falsa positiva sem --exclude-service.
        {"nome": "arn:aws:payments::123456789012:payment-instrument/exemplo", "tags": {}},
    ]


# Fonte de dados 2: os recursos REAIS da conta AWS.
# Usa a Resource Groups Tagging API, que lista recursos com suas tags.
# So precisa de permissao de LEITURA (tag:GetResources).
def recursos_da_aws():
    # Importamos o boto3 AQUI DENTRO (nao no topo do arquivo) de proposito:
    # assim o modo "sample", os testes e o CI funcionam sem ter o boto3
    # instalado nem credencial nenhuma.
    import boto3

    client = boto3.client("resourcegroupstaggingapi")

    recursos = []
    # O paginator resolve o problema de listas grandes: a AWS devolve os
    # resultados em "paginas" e ele busca todas para nos, uma por uma.
    paginator = client.get_paginator("get_resources")
    for pagina in paginator.paginate():
        for item in pagina["ResourceTagMappingList"]:
            # A AWS devolve tags como [{"Key": "...", "Value": "..."}].
            # Convertemos para o nosso formato {"Key": "Value"}.
            tags = {t["Key"]: t["Value"] for t in item["Tags"]}
            recursos.append({"nome": item["ResourceARN"], "tags": tags})
    return recursos


# Le o "servico" de dentro de um ARN da AWS.
# Um ARN tem o formato: arn:particao:servico:regiao:conta:recurso
# O servico e sempre o 3o campo. Nomes que NAO sao ARN (o modo sample usa
# nomes simples, tipo "bucket-antigo") nao tem servico -> devolvemos None.
def servico_do_arn(nome):
    partes = nome.split(":")
    if len(partes) >= 3 and partes[0] == "arn":
        return partes[2]
    return None


# Remove da lista os recursos cujo servico esta na lista de excluidos.
# Serve para casos como 'payments' (cartao de credito salvo): a Tagging API
# lista esses recursos, mas a AWS nao deixa colocar tags neles -> seriam
# falsas positivas eternas no relatorio.
def filtrar_por_servico(recursos, servicos_excluidos):
    if not servicos_excluidos:
        return recursos  # nada a excluir: devolve tudo como veio
    filtrados = []
    for recurso in recursos:
        if servico_do_arn(recurso["nome"]) in servicos_excluidos:
            continue  # pula este recurso
        filtrados.append(recurso)
    return filtrados


# Roda a auditoria em cima de uma lista de recursos e imprime o relatorio.
# DEVOLVE quantos recursos estao fora de conformidade (para virar exit code).
def auditar(recursos, obrigatorias):
    problemas = 0
    for recurso in recursos:
        faltando = tags_faltando(recurso, obrigatorias)
        if faltando:
            print("FALTA", recurso["nome"], "-> faltam:", faltando)
            problemas += 1
        else:
            print("OK   ", recurso["nome"])
    return problemas


# Este bloco so roda quando voce EXECUTA o arquivo (python auditor.py).
# Quando outro arquivo IMPORTA este (como o teste faz), ele NAO roda.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Audita recursos e aponta os que estao sem as tags obrigatorias."
    )
    parser.add_argument(
        "--source",
        choices=["sample", "aws"],
        default="sample",
        help="De onde ler os recursos: 'sample' (exemplo fixo, padrao) ou 'aws' (conta real).",
    )
    parser.add_argument(
        "--required-tags",
        nargs="+",
        default=["Project", "Environment", "Owner"],
        metavar="TAG",
        help="Tags obrigatorias a exigir (padrao: Project Environment Owner).",
    )
    parser.add_argument(
        "--exclude-service",
        nargs="+",
        default=[],
        metavar="SERVICO",
        help="Servicos AWS a ignorar (ex: payments). Util para recursos que a "
        "Tagging API lista mas que nao aceitam tags.",
    )
    args = parser.parse_args()

    tags_obrigatorias = args.required_tags

    if args.source == "aws":
        # Ler da AWS pode falhar por falta de permissao ou de credencial.
        # Uma ferramenta de verdade NAO joga um traceback na cara do usuario:
        # ela explica o problema e sai com um codigo de erro proprio.
        try:
            recursos = recursos_da_aws()
        except Exception as erro:
            print("ERRO ao ler recursos da AWS:", erro)
            print("Dica: o modo --source aws precisa de uma identidade com")
            print("permissao de leitura (tag:GetResources). A policy minima")
            print("necessaria esta em docs/iam-policy.json.")
            sys.exit(2)  # 2 = erro da ferramenta (diferente de 'achou problema')
    else:
        recursos = recursos_de_exemplo()

    # Tira da jogada os servicos que o usuario mandou ignorar (ex: payments).
    recursos = filtrar_por_servico(recursos, args.exclude_service)

    problemas = auditar(recursos, tags_obrigatorias)

    print()
    print(f"Resumo: {len(recursos)} recursos, {problemas} fora de conformidade.")

    # Codigos de saida com significado, para o CI/CD saber o que fazer:
    #   0 = tudo certo
    #   1 = achou recurso sem tag (BLOQUEIA o deploy)
    #   2 = a ferramenta nem rodou direito (erro de permissao/credencial)
    if problemas > 0:
        sys.exit(1)
