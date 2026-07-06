"""Gera transações de vendas de um e-commerce e carrega num banco SQLite."""
import numpy as np
import pandas as pd
import sqlite3
from pathlib import Path

RNG = np.random.default_rng(2024)
N = 20000
BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "dados"; DATA.mkdir(exist_ok=True)

CATEGORIAS = {
    "Eletrônicos": (200, 4000),
    "Vestuário": (40, 400),
    "Casa": (30, 900),
    "Livros": (20, 120),
    "Esportes": (50, 800),
}
REGIOES = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]

def gerar():
    datas = pd.to_datetime("2023-01-01") + pd.to_timedelta(
        RNG.integers(0, 730, N), unit="D"
    )
    categoria = RNG.choice(list(CATEGORIAS), N, p=[0.2, 0.3, 0.2, 0.15, 0.15])
    preco = np.array([RNG.uniform(*CATEGORIAS[c]) for c in categoria]).round(2)
    quantidade = RNG.integers(1, 5, N)
    regiao = RNG.choice(REGIOES, N, p=[0.45, 0.2, 0.18, 0.1, 0.07])
    canal = RNG.choice(["App", "Site", "Marketplace"], N, p=[0.4, 0.35, 0.25])

    df = pd.DataFrame({
        "id_pedido": np.arange(1, N + 1),
        "data": datas.date,
        "categoria": categoria,
        "regiao": regiao,
        "canal": canal,
        "quantidade": quantidade,
        "preco_unitario": preco,
        "receita": (preco * quantidade).round(2),
    })
    df.to_csv(DATA / "vendas.csv", index=False)

    con = sqlite3.connect(DATA / "vendas.db")
    df.to_sql("vendas", con, if_exists="replace", index=False)
    con.close()
    print(f"Gerado: {len(df)} pedidos | receita total = R$ {df['receita'].sum():,.0f}")
    print(f"CSV e SQLite salvos em {DATA}")
    return df

if __name__ == "__main__":
    gerar()
