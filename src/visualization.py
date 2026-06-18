import matplotlib.pyplot as plt


def grafico_saldo_mensal(resumo_mensal):

    resumo_mensal["periodo"] = (
        resumo_mensal["ano"].astype(str)
        + "-"
        + resumo_mensal["mes"].astype(str).str.zfill(2)
    )

    plt.figure(figsize=(10, 5))

    plt.plot(
        resumo_mensal["periodo"],
        resumo_mensal["Saldo"],
        marker="o"
    )

    plt.axhline(
        y=0,
        color="red",
        linestyle="--"
    )

    plt.title("Saldo Mensal Projetado")
    plt.xlabel("Período")
    plt.ylabel("Saldo")
    plt.xticks(rotation=45)
    plt.grid()

    plt.tight_layout()

    plt.show()