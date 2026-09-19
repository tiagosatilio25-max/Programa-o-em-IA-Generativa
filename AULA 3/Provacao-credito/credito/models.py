"""Modelos de dados do simulador de crédito.

Mantido separado da lógica de negócio e da interface (separação de camadas):
esta classe representa apenas dados, sem nenhuma regra de negócio.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ResultadoSimulacao:
    """Resultado de uma simulação de crédito.

    Attributes:
        aprovado: True se o crédito foi aprovado.
        motivo: Explicação legível do resultado (mostrável ao usuário final).
        parcela_sugerida: Valor máximo de parcela sugerido quando negado.
            None quando aprovado ou quando a negativa é por idade mínima
            (nesse caso não existe parcela "sugerível").
    """

    aprovado: bool
    motivo: str
    parcela_sugerida: Optional[float] = None
