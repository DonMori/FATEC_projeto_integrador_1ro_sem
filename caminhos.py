import os
import sys

# ─────────────────────────────────────────────
#  Detecta a pasta base corretamente,
#  tanto rodando como .py quanto como .exe
# ─────────────────────────────────────────────

if getattr(sys, 'frozen', False):
    PASTA_BASE = os.path.dirname(sys.executable)
else:
    PASTA_BASE = os.path.dirname(os.path.abspath(__file__))

PASTA_DADOS          = os.path.join(PASTA_BASE, "dados")

# ── Mudança: extensão .txt → .json ──
ARQUIVO_CLIENTES     = os.path.join(PASTA_DADOS, "clientes.json")
ARQUIVO_AGENDAMENTOS = os.path.join(PASTA_DADOS, "agendamentos.json")
ARQUIVO_OPERADOR     = os.path.join(PASTA_DADOS, "operador.json")
