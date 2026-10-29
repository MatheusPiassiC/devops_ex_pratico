FAIXAS = ((90, "A"), (70, "B"), (50, "C"))


def classificar_pontuacao(pontos: int) -> str:
    if pontos < 0:
        raise ValueError("pontuacao invalida")
    for minimo, conceito in FAIXAS:
        if pontos >= minimo:
            return conceito
    return "D"