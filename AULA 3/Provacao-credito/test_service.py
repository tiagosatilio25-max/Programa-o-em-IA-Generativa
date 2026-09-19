"""Testes do módulo credito.service.

Cobrem as três regras de negócio e a validação de inputs, servindo como
critério de aceite verificável do módulo (conforme exigido pela skill de
revisão de segurança/arquitetura).
"""

import pytest

from credito.service import DadosInvalidosError, analisar_credito


def test_nega_credito_para_menor_de_idade():
    resultado = analisar_credito(idade=17, renda=3000, parcela=200)
    assert resultado.aprovado is False
    assert resultado.parcela_sugerida is None


def test_aprova_dentro_da_margem_jovem_20_por_cento():
    # 20 anos, faixa 18-21 -> margem de 20%
    resultado = analisar_credito(idade=20, renda=2000, parcela=400)
    assert resultado.aprovado is True


def test_nega_e_sugere_parcela_maxima_faixa_jovem():
    resultado = analisar_credito(idade=19, renda=2000, parcela=500)
    assert resultado.aprovado is False
    assert resultado.parcela_sugerida == pytest.approx(400.0)


def test_aprova_dentro_da_margem_padrao_30_por_cento():
    resultado = analisar_credito(idade=30, renda=3000, parcela=900)
    assert resultado.aprovado is True


def test_nega_e_sugere_parcela_maxima_faixa_padrao():
    resultado = analisar_credito(idade=25, renda=3000, parcela=1200)
    assert resultado.aprovado is False
    assert resultado.parcela_sugerida == pytest.approx(900.0)


@pytest.mark.parametrize(
    "idade, renda, parcela",
    [
        (-5, 2000, 100),   # idade negativa
        (25, -100, 100),   # renda negativa
        (25, 2000, -50),   # parcela negativa
        (25, float("nan"), 100),  # renda inválida (NaN)
    ],
)
def test_lanca_erro_para_dados_invalidos(idade, renda, parcela):
    with pytest.raises(DadosInvalidosError):
        analisar_credito(idade=idade, renda=renda, parcela=parcela)
