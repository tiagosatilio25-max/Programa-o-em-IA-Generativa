"""Interface de linha de comando (CLI) do simulador de crédito.

Responsabilidade única deste módulo: coletar input do usuário via terminal,
validar formato (não regra de negócio) e delegar a decisão ao módulo
`credito.service`. Nenhuma regra financeira vive aqui.
"""

from credito.service import DadosInvalidosError, analisar_credito


def _ler_numero(mensagem: str, tipo=float):
    """Lê um número do terminal, repetindo até receber um valor válido.

    Trata `ValueError` explicitamente (conversão de string para número),
    conforme exigido no STYLE do módulo, sem deixar o programa quebrar
    por digitação incorreta do usuário.
    """
    while True:
        bruto = input(mensagem).strip().replace(",", ".")
        try:
            valor = tipo(bruto)
        except ValueError:
            print("  ⚠️  Valor inválido. Digite apenas números.")
            continue
        if valor < 0:
            print("  ⚠️  O valor não pode ser negativo.")
            continue
        return valor


def executar_cli() -> None:
    """Ponto de entrada da interface de terminal."""
    print("=" * 50)
    print("  SIMULADOR DE APROVAÇÃO DE CRÉDITO BANCÁRIO")
    print("=" * 50)

    idade = int(_ler_numero("Idade (anos): ", tipo=int))
    renda = _ler_numero("Renda mensal (R$): ", tipo=float)
    parcela = _ler_numero("Valor da parcela desejada (R$): ", tipo=float)

    try:
        resultado = analisar_credito(idade=idade, renda=renda, parcela=parcela)
    except DadosInvalidosError as erro:
        # Erro de negócio conhecido: mostramos a mensagem da própria exceção,
        # sem vazar stack trace ao usuário final.
        print(f"\n❌ Não foi possível simular: {erro}")
        return
    except Exception:
        # Qualquer erro não previsto: mensagem genérica, nunca o erro cru.
        print("\n❌ Ocorreu um erro inesperado. Tente novamente.")
        return

    print()
    if resultado.aprovado:
        print(f"✅ {resultado.motivo}")
    else:
        print(f"🚫 {resultado.motivo}")
        if resultado.parcela_sugerida is not None:
            print(f"💡 Sugerimos uma parcela de até R$ {resultado.parcela_sugerida:.2f}.")


if __name__ == "__main__":
    executar_cli()
