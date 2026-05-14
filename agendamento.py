import os
import json
import time
import threading
from datetime import datetime
from cadastro_cliente import ler_todos_clientes
from operador import ler_operador
from caminhos import PASTA_DADOS, ARQUIVO_AGENDAMENTOS


# ─────────────────────────────────────────────
#  Leitura e escrita de agendamentos
# ─────────────────────────────────────────────

def garantir_arquivo():
    os.makedirs(PASTA_DADOS, exist_ok=True)
    if not os.path.exists(ARQUIVO_AGENDAMENTOS):
        with open(ARQUIVO_AGENDAMENTOS, 'w', encoding='utf-8') as f:
            json.dump([], f)


# ── MUDANÇA PRINCIPAL ──
# Antes (TXT): loop linha por linha, separava blocos por "---",
#              fazia split(":") para separar chave e valor
# Agora (JSON): uma linha carrega tudo como lista de dicionários

def ler_todos_agendamentos():
    garantir_arquivo()
    with open(ARQUIVO_AGENDAMENTOS, 'r', encoding='utf-8') as f:
        return json.load(f)


def salvar_todos_agendamentos(agendamentos):
    garantir_arquivo()
    with open(ARQUIVO_AGENDAMENTOS, 'w', encoding='utf-8') as f:
        json.dump(agendamentos, f, ensure_ascii=False, indent=4)


# ─────────────────────────────────────────────
#  Auxiliares
# ─────────────────────────────────────────────

def buscar_cliente_por_id(id_cliente):
    clientes = ler_todos_clientes()
    for c in clientes:
        if c.get("ID") == str(id_cliente):
            return c
    return None


def formatar_duracao(segundos):
    segundos = int(segundos)
    h = segundos // 3600
    m = (segundos % 3600) // 60
    s = segundos % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


def duracao_em_segundos(duracao_str):
    try:
        partes = duracao_str.split(":")
        return int(partes[0]) * 3600 + int(partes[1]) * 60 + int(partes[2])
    except Exception:
        return 0


def pedir_data_hora():
    while True:
        entrada = input("  Data e horário (DD/MM/AAAA HH:MM): ").strip()
        try:
            dt = datetime.strptime(entrada, "%d/%m/%Y %H:%M")
            return dt.strftime("%d/%m/%Y %H:%M")
        except ValueError:
            print("  [!] Formato inválido. Use DD/MM/AAAA HH:MM (ex: 25/06/2025 14:30)")


def listar_clientes_resumido():
    clientes = ler_todos_clientes()
    if not clientes:
        print("\n  Nenhum cliente cadastrado.")
        return False
    print()
    for c in clientes:
        print(f"  ID: {c.get('ID','?')} — {c.get('Nome','?')}")
    return True


# ─────────────────────────────────────────────
#  Estimativa de tempo
# ─────────────────────────────────────────────

def calcular_estimativa(id_cliente):
    agendamentos = ler_todos_agendamentos()
    concluidos = [
        ag for ag in agendamentos
        if ag.get("ID Cliente") == str(id_cliente)
        and ag.get("Status") == "concluido"
        and ag.get("Duracao Real") not in (None, "", "pendente")
    ]
    if not concluidos:
        return None
    ultimos = concluidos[-3:]
    total_seg = sum(duracao_em_segundos(ag["Duracao Real"]) for ag in ultimos)
    return total_seg // len(ultimos)


# ─────────────────────────────────────────────
#  CREATE — Criar agendamento
# ─────────────────────────────────────────────

def criar_agendamento():
    print("\n  ── Novo Agendamento ──\n")

    if not listar_clientes_resumido():
        input("\n  Pressione ENTER para continuar...")
        return

    try:
        id_cliente = int(input("\n  ID do cliente: ").strip())
    except ValueError:
        print("\n  [!] ID inválido.")
        input("\n  Pressione ENTER para continuar...")
        return

    cliente = buscar_cliente_por_id(id_cliente)
    if not cliente:
        print(f"\n  [!] Cliente com ID {id_cliente} não encontrado.")
        input("\n  Pressione ENTER para continuar...")
        return

    print(f"\n  Cliente selecionado: {cliente['Nome']}")

    estimativa = calcular_estimativa(id_cliente)
    if estimativa:
        print(f"  💡 Estimativa de duração (média dos últimos agendamentos): {formatar_duracao(estimativa)}")
    else:
        print("  💡 Ainda não há histórico de gravações para estimar a duração.")

    print()
    data_hora = pedir_data_hora()
    operador = ler_operador() or "Não informado"

    agendamentos = ler_todos_agendamentos()
    ultimo_id = max((int(ag.get("ID", 0)) for ag in agendamentos), default=0)

    novo = {
        "ID":           str(ultimo_id + 1),
        "ID Cliente":   str(id_cliente),
        "Cliente":      cliente["Nome"],
        "Operador":     operador,
        "Data Hora":    data_hora,
        "Status":       "agendado",
        "Duracao Real": "pendente",
    }

    agendamentos.append(novo)
    salvar_todos_agendamentos(agendamentos)

    print(f"\n  [✓] Agendamento criado com sucesso! (ID: {novo['ID']})")
    input("\n  Pressione ENTER para continuar...")


# ─────────────────────────────────────────────
#  READ — Listar agendamentos
# ─────────────────────────────────────────────

def listar_agendamentos():
    print("\n  ── Agendamentos ──\n")
    agendamentos = ler_todos_agendamentos()

    if not agendamentos:
        print("  Nenhum agendamento registrado ainda.")
    else:
        for ag in agendamentos:
            print(f"  ID: {ag.get('ID','?')} | Cliente: {ag.get('Cliente','?')} | "
                  f"Data: {ag.get('Data Hora','?')} | Status: {ag.get('Status','?')} | "
                  f"Duração: {ag.get('Duracao Real','?')}")

    input("\n  Pressione ENTER para continuar...")


# ─────────────────────────────────────────────
#  UPDATE — Atualizar agendamento
# ─────────────────────────────────────────────

def atualizar_agendamento():
    print("\n  ── Atualizar Agendamento ──")
    agendamentos = ler_todos_agendamentos()

    if not agendamentos:
        print("\n  Nenhum agendamento registrado.")
        input("\n  Pressione ENTER para continuar...")
        return

    for ag in agendamentos:
        print(f"  ID: {ag.get('ID','?')} | Cliente: {ag.get('Cliente','?')} | "
              f"Data: {ag.get('Data Hora','?')} | Status: {ag.get('Status','?')}")

    try:
        id_busca = int(input("\n  ID do agendamento a atualizar: ").strip())
    except ValueError:
        print("\n  [!] ID inválido.")
        input("\n  Pressione ENTER para continuar...")
        return

    encontrado = False
    for ag in agendamentos:
        if int(ag.get("ID", -1)) == id_busca:
            encontrado = True
            print(f"\n  Agendamento encontrado: Cliente {ag['Cliente']} — {ag['Data Hora']}")
            print("  (Deixe em branco para manter o valor atual)\n")

            nova_data = input(f"  Nova data/hora [{ag['Data Hora']}]: ").strip()
            if nova_data:
                try:
                    dt = datetime.strptime(nova_data, "%d/%m/%Y %H:%M")
                    ag["Data Hora"] = dt.strftime("%d/%m/%Y %H:%M")
                except ValueError:
                    print("  [!] Formato inválido, data não alterada.")

            print("  Status disponíveis: agendado | concluido | cancelado")
            novo_status = input(f"  Novo status [{ag['Status']}]: ").strip().lower()
            if novo_status in ("agendado", "concluido", "cancelado"):
                ag["Status"] = novo_status
            elif novo_status:
                print("  [!] Status inválido, mantido o anterior.")
            break

    if not encontrado:
        print(f"\n  [!] Agendamento ID {id_busca} não encontrado.")
    else:
        salvar_todos_agendamentos(agendamentos)
        print("\n  [✓] Agendamento atualizado com sucesso!")

    input("\n  Pressione ENTER para continuar...")


# ─────────────────────────────────────────────
#  DELETE — Excluir agendamento
# ─────────────────────────────────────────────

def excluir_agendamento():
    print("\n  ── Excluir Agendamento ──")
    agendamentos = ler_todos_agendamentos()

    if not agendamentos:
        print("\n  Nenhum agendamento registrado.")
        input("\n  Pressione ENTER para continuar...")
        return

    for ag in agendamentos:
        print(f"  ID: {ag.get('ID','?')} | Cliente: {ag.get('Cliente','?')} | "
              f"Data: {ag.get('Data Hora','?')} | Status: {ag.get('Status','?')}")

    try:
        id_busca = int(input("\n  ID do agendamento a excluir: ").strip())
    except ValueError:
        print("\n  [!] ID inválido.")
        input("\n  Pressione ENTER para continuar...")
        return

    nova_lista = [ag for ag in agendamentos if int(ag.get("ID", -1)) != id_busca]

    if len(nova_lista) == len(agendamentos):
        print(f"\n  [!] Agendamento ID {id_busca} não encontrado.")
    else:
        confirmacao = input(f"\n  Confirmar exclusão do agendamento ID {id_busca}? (s/n): ").strip().lower()
        if confirmacao == 's':
            salvar_todos_agendamentos(nova_lista)
            print("\n  [✓] Agendamento excluído com sucesso!")
        else:
            print("\n  Operação cancelada.")

    input("\n  Pressione ENTER para continuar...")


# ─────────────────────────────────────────────
#  CRONÔMETRO — Iniciar gravação
# ─────────────────────────────────────────────

def iniciar_cronometro():
    print("\n  ── Iniciar Gravação ──")
    agendamentos = ler_todos_agendamentos()

    disponiveis = [ag for ag in agendamentos if ag.get("Status") == "agendado"]

    if not disponiveis:
        print("\n  Nenhum agendamento com status 'agendado' disponível.")
        input("\n  Pressione ENTER para continuar...")
        return

    for ag in disponiveis:
        print(f"  ID: {ag.get('ID','?')} | Cliente: {ag.get('Cliente','?')} | "
              f"Data: {ag.get('Data Hora','?')}")

    try:
        id_busca = int(input("\n  ID do agendamento para iniciar gravação: ").strip())
    except ValueError:
        print("\n  [!] ID inválido.")
        input("\n  Pressione ENTER para continuar...")
        return

    agendamento_alvo = None
    for ag in agendamentos:
        if int(ag.get("ID", -1)) == id_busca and ag.get("Status") == "agendado":
            agendamento_alvo = ag
            break

    if not agendamento_alvo:
        print(f"\n  [!] Agendamento ID {id_busca} não encontrado ou não está 'agendado'.")
        input("\n  Pressione ENTER para continuar...")
        return

    print(f"\n  Cliente: {agendamento_alvo['Cliente']}")
    print(f"  Operador: {agendamento_alvo['Operador']}")
    input("\n  Pressione ENTER para INICIAR a gravação...")

    inicio = time.time()
    parar = threading.Event()

    def exibir_tempo():
        while not parar.is_set():
            decorrido = time.time() - inicio
            print(f"\r  ⏱  Gravação em andamento... {formatar_duracao(decorrido)}", end="", flush=True)
            time.sleep(1)

    thread = threading.Thread(target=exibir_tempo, daemon=True)
    thread.start()

    input("\n\n  (Pressione ENTER para PARAR a gravação...)\n")
    parar.set()
    thread.join()

    fim = time.time()
    duracao_seg = int(fim - inicio)
    duracao_fmt = formatar_duracao(duracao_seg)

    for ag in agendamentos:
        if int(ag.get("ID", -1)) == id_busca:
            ag["Duracao Real"] = duracao_fmt
            ag["Status"]       = "concluido"
            break

    salvar_todos_agendamentos(agendamentos)

    print(f"\n  [✓] Gravação encerrada! Duração total: {duracao_fmt}")
    print(f"  [✓] Agendamento ID {id_busca} marcado como 'concluido'.")
    input("\n  Pressione ENTER para continuar...")
