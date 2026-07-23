# Importa SO a funcao do auditor.py (o exemplo com prints nao roda,
# gracas ao "if __name__ == '__main__'" que colocamos la).
from auditor import tags_faltando

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
