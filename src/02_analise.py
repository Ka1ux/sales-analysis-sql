"""EDA de vendas: responde perguntas de negócio e gera um dashboard de gráficos."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path

sns.set_theme(style="whitegrid")
BASE = Path(__file__).resolve().parent.parent
IMG = BASE / "imagens"; IMG.mkdir(exist_ok=True)

def main():
    df = pd.read_csv(BASE / "dados" / "vendas.csv", parse_dates=["data"])

    print("== KPIs ==")
    print(f"Receita total:  R$ {df['receita'].sum():,.0f}")
    print(f"Ticket médio:   R$ {df['receita'].mean():,.2f}")
    print(f"Nº de pedidos:  {len(df):,}")

    mensal = df.set_index("data").resample("ME")["receita"].sum() / 1000
    fig, ax = plt.subplots(figsize=(9, 4))
    mensal.plot(ax=ax, marker="o", color="#2a9d8f")
    ax.set(title="Receita mensal (R$ mil)", xlabel="", ylabel="R$ mil")
    fig.tight_layout(); fig.savefig(IMG / "receita_mensal.png", dpi=110); plt.close(fig)

    cat = df.groupby("categoria")["receita"].sum().sort_values(ascending=False) / 1000
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x=cat.values, y=cat.index, ax=ax, palette="mako")
    ax.set(title="Receita por categoria (R$ mil)", xlabel="R$ mil")
    fig.tight_layout(); fig.savefig(IMG / "receita_categoria.png", dpi=110); plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4))
    piv = df.pivot_table("receita", "regiao", "canal", aggfunc="sum") / 1000
    piv.plot(kind="bar", stacked=True, ax=ax, colormap="viridis")
    ax.set(title="Receita por região e canal (R$ mil)", xlabel="", ylabel="R$ mil")
    plt.xticks(rotation=30, ha="right")
    fig.tight_layout(); fig.savefig(IMG / "regiao_canal.png", dpi=110); plt.close(fig)

    ticket = df.groupby("canal")["receita"].mean().sort_values()
    print("\nTicket médio por canal:")
    print(ticket.round(2).to_string())

    print(f"\nDashboard salvo em {IMG}")

if __name__ == "__main__":
    main()
