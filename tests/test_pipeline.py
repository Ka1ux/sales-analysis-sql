"""Testes de integração: roda o pipeline e valida os dados e o banco gerado."""
import sqlite3
import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable
SCRIPTS = ["src/01_gerar_dados.py", "src/02_analise.py"]


def _run(script):
    r = subprocess.run([PY, script], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, f"{script} falhou:\n{r.stderr}"


def test_pipeline_roda_sem_erro():
    for s in SCRIPTS:
        _run(s)


def test_csv_valido():
    _run("src/01_gerar_dados.py")
    df = pd.read_csv(ROOT / "dados" / "vendas.csv")
    assert len(df) > 1000
    assert (df["receita"] >= 0).all()
    assert (df["quantidade"] >= 1).all()


def test_banco_sqlite_tem_dados():
    _run("src/01_gerar_dados.py")
    con = sqlite3.connect(ROOT / "dados" / "vendas.db")
    n = con.execute("SELECT COUNT(*) FROM vendas").fetchone()[0]
    con.close()
    assert n > 1000
