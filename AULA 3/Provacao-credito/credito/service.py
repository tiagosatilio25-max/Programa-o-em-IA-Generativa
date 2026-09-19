"""Lógica de negócio do simulador de crédito bancário.

Este módulo não depende de terminal, Streamlit ou qualquer forma de I/O —
pode ser testado isoladamente e reutilizado por qualquer interface
(CLI, web, API), respeitando a separação de camadas.
"""

from .models import ResultadoSimulacao

# --- Regras de negócio (constantes documentadas conforme especificação) ---

IDADE_MINIMA = 18
"""Idade mínima para contratar crédito (capacidade civil plena)."""

IDADE_LIMITE_JOVEM = 21
"""Limite superior da faixa de "jovem" com maior risco de crédito."""

PERCENTUAL_MAXIMO_JOVEM = 0.20
"""Percentual máximo de comprometimento de renda para jovens (18-21 anos)."""

PERCENTUAL_MAXIMO_PADRAO = 0.30
"""Percentual máximo de comprometimento de renda para o público geral (> 21 anos)."""


class DadosInvalidosError(Exception):
    """Erro de negócio para dados de entrada inconsistentes.

    Usar uma exceção específica (em vez de ValueError genérico ou deixar
    uma exceção não tratada estourar) permite que a camada de UI capture
    exatamente este erro e mostre uma mensagem amigável ao usuário, sem
    vazar detalhes internos de implementação.
    """


def _percentual_maximo_por_idade(idade: int) -> float:
    """Determina o percentual máximo de renda comprometível pela idade
    (fator de risco por idade)."""
    if IDADE_MINIMA <= idade <= IDADE_LIMITE_JOVEM:
        return PERCENTUAL_MAXIMO_JOVEM
    return PERCENTUAL_MAXIMO_PADRAO


def _validar_inputs(idade: int, renda: float, parcela: float) -> None:
    """Valida os dados de entrada antes de aplicar qualquer regra de negócio.

    Nunca confiar que os dados chegaram corretos da camada de UI — a
    validação de negócio deve ser independente da validação de formulário.
    """
    if not isinstance(idade, int) or idade <= 0 or idade > 120:
        raise DadosInvalidosError("Idade informada é inválida.")
    if renda != renda or renda in (float("inf"), float("-inf")) or renda <= 0:
        # `renda != renda` detecta NaN sem precisar importar math.
        raise DadosInvalidosError("Renda mensal informada é inválida.")
    if parcela != parcela or parcela in (float("inf"), float("-inf")) or parcela < 0:
        raise DadosInvalidosError("Valor de parcela informado é inválido.")


def analisar_credito(idade: int, renda: float, parcela: float) -> ResultadoSimulacao:
    """Analisa a elegibilidade de crédito conforme as regras de negócio.

    Args:
        idade: idade do solicitante, em anos completos.
        renda: renda mensal do solicitante, em R$.
        parcela: valor da parcela desejada pelo solicitante, em R$.

    Returns:
        ResultadoSimulacao com a decisão, o motivo e, se negado por
        estourar a margem de renda, a parcela máxima sugerida.

    Raises:
        DadosInvalidosError: se idade, renda ou parcela forem inconsistentes
            (ex: negativos, NaN, fora de uma faixa plausível).
    """
    _validar_inputs(idade, renda, parcela)

    # Regra 1: idade mínima (incapacidade civil abaixo de 18 anos).
    if idade < IDADE_MINIMA:
        return ResultadoSimulacao(
            aprovado=False,
            motivo="Crédito negado: idade mínima para contratação é 18 anos.",
            parcela_sugerida=None,
        )

    # Regra 2: fator de risco por idade define o percentual máximo de renda.
    percentual_maximo = _percentual_maximo_por_idade(idade)

    # Regra 3 / Fórmula de recálculo: Parcela Máxima = Renda * Percentual Máximo.
    margem_maxima = renda * percentual_maximo

    if parcela <= margem_maxima:
        return ResultadoSimulacao(
            aprovado=True,
            motivo="Crédito aprovado: parcela dentro da margem permitida.",
            parcela_sugerida=None,
        )

    return ResultadoSimulacao(
        aprovado=False,
        motivo=(
            f"Crédito negado: a parcela desejada ultrapassa "
            f"{percentual_maximo:.0%} da renda mensal informada."
        ),
        parcela_sugerida=round(margem_maxima, 2),
    )
