def limpar_transacoes(df):

    df["descricao"] = df["descricao"].str.strip()
    df["categoria"] = df["categoria"].str.strip()
    df["tipo_pagamento"] = df["tipo_pagamento"].str.strip()
    df["cartao"] = df["cartao"].str.strip()

    return(df)