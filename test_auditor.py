# Importa SO a funcao do auditor.py (o exemplo com prints nao roda,
# gracas ao "if __name__ == '__main__'" que colocamos la).
from auditor import tags_faltando, servico_do_arn, filtrar_por_servico

obrigatorias = ["Project", "Environment", "Owner"]


def test_recurso_sem_nenhuma_tag():
    recurso = {"nome": "vazio", "tags": {}}
    assert tags_faltando(recurso, obrigatorias) == ["Project", "Environment", "Owner"]


def test_recurso_faltando_so_owner():
    recurso = {"nome": "quase", "tags": {"Project": "x", "Environment": "prod"}}
    assert tags_faltando(recurso, obrigatorias) == ["Owner"]


def test_recurso_completo():
    recurso = {"nome": "ok", "tags": {"Project": "x", "Environment": "prod", "Owner": "rodrigo"}}
    assert tags_faltando(recurso, obrigatorias) == []


# A lista de obrigatorias e um PARAMETRO, entao a mesma funcao serve para
# qualquer conjunto de tags que o usuario exigir via --required-tags.
def test_lista_de_obrigatorias_customizada():
    recurso = {"nome": "custom", "tags": {"Project": "x", "Environment": "prod", "Owner": "rodrigo"}}
    assert tags_faltando(recurso, ["CostCenter"]) == ["CostCenter"]


# --- servico_do_arn: le o 3o campo do ARN ---

def test_servico_do_arn_le_o_servico():
    assert servico_do_arn("arn:aws:payments::123456789012:payment-instrument/x") == "payments"


def test_servico_do_arn_com_nome_simples_devolve_none():
    # O modo sample usa nomes que nao sao ARN -> nao tem servico.
    assert servico_do_arn("bucket-antigo") is None


# --- filtrar_por_servico: remove os servicos excluidos ---

def test_filtrar_remove_o_servico_excluido():
    recursos = [
        {"nome": "arn:aws:s3:::meu-bucket", "tags": {}},
        {"nome": "arn:aws:payments::123456789012:payment-instrument/x", "tags": {}},
    ]
    resultado = filtrar_por_servico(recursos, ["payments"])
    assert len(resultado) == 1
    assert resultado[0]["nome"] == "arn:aws:s3:::meu-bucket"


def test_filtrar_sem_exclusao_devolve_tudo():
    recursos = [{"nome": "arn:aws:s3:::meu-bucket", "tags": {}}]
    assert filtrar_por_servico(recursos, []) == recursos
