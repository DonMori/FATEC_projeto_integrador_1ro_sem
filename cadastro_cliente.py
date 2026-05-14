import os
import json
from caminhos import PASTA_DADOS, ARQUIVO_CLIENTES

# ─────────────────────────────────────────────
#  Funções auxiliares de leitura/escrita
# ─────────────────────────────────────────────

def garantir_arquivo():
    os.makedirs(PASTA_DADOS, exist_ok=True)
    if not os.path.exists(ARQUIVO_CLIENTES):
        with open(ARQUIVO_CLIENTES, 'w', encoding='utf-8') as f:
            json.dump([], f)  # começa com uma lista vazia


# ── MUDANÇA PRINCIPAL ──
# Antes (TXT): abria o arquivo linha por linha, procurava "---",
#              separava chave e valor manualmente com split(":")
# Agora (JSON): uma única linha carrega tudo — o Python entende
#               o formato automaticamente

def ler_todos_clientes():
    garantir_arquivo()
    with open(ARQUIVO_CLIENTES, 'r', encoding='utf-8') as f:
        return json.load(f)  # lê o arquivo e já devolve uma lista de dicionários


def salvar_todos_clientes(clientes):
    garantir_arquivo()
    with open(ARQUIVO_CLIENTES, 'w', encoding='utf-8') as f:
        json.dump(clientes, f, ensure_ascii=False, indent=4)
    # ensure_ascii=False → salva acentos corretamente (ã, ç, é...)
    # indent=4          → formata o arquivo com recuo de 4 espaços (legível)


# ─────────────────────────────────────────────
#  CREATE — Adicionar cliente
# ─────────────────────────────────────────────

def adicionar_cliente():
    print("\n  ── Adicionar Novo Cliente ──")
    nome  = input("  Nome:     ").strip()
    email = input("  E-mail:   ").strip()
    fone  = input("  Telefone: ").strip()

    if not nome:
        print("\n  [!] O nome não pode estar vazio.")
        input("\n  Pressione ENTER para continuar...")
        return

    clientes = ler_todos_clientes()

    if clientes:
        ultimo_id = max(int(c.get("ID", 0)) for c in clientes)
    else:
        ultimo_id = 0

    novo_cliente = {
        "ID":       str(ultimo_id + 1),
        "Nome":     nome,
        "Email":    email,
        "Telefone": fone,
    }

    clientes.append(novo_cliente)
    salvar_todos_clientes(clientes)

    print(f"\n  [✓] Cliente '{nome}' adicionado com sucesso! (ID: {novo_cliente['ID']})")
    input("\n  Pressione ENTER para continuar...")


# ─────────────────────────────────────────────
#  READ — Listar clientes
# ─────────────────────────────────────────────

def listar_clientes():
    print("\n  ── Lista de Clientes ──\n")
    clientes = ler_todos_clientes()

    if not clientes:
        print("  Nenhum cliente cadastrado ainda.")
    else:
        for c in clientes:
            print(f"  ID: {c.get('ID','?')} | Nome: {c.get('Nome','?')} "
                  f"| E-mail: {c.get('Email','?')} | Tel: {c.get('Telefone','?')}")

    input("\n  Pressione ENTER para continuar...")


# ─────────────────────────────────────────────
#  UPDATE — Atualizar cliente
# ─────────────────────────────────────────────

def atualizar_cliente():
    print("\n  ── Atualizar Cliente ──")
    listar_clientes_resumido()

    try:
        id_busca = int(input("\n  Digite o ID do cliente a atualizar: ").strip())
    except ValueError:
        print("\n  [!] ID inválido.")
        input("\n  Pressione ENTER para continuar...")
        return

    clientes = ler_todos_clientes()
    encontrado = False

    for cliente in clientes:
        if int(cliente.get("ID", -1)) == id_busca:
            encontrado = True
            print(f"\n  Cliente encontrado: {cliente.get('Nome')}")
            print("  (Deixe em branco para manter o valor atual)\n")

            novo_nome  = input(f"  Novo nome  [{cliente['Nome']}]:     ").strip()
            novo_email = input(f"  Novo email [{cliente['Email']}]:    ").strip()
            novo_fone  = input(f"  Novo tel.  [{cliente['Telefone']}]: ").strip()

            if novo_nome:  cliente["Nome"]     = novo_nome
            if novo_email: cliente["Email"]    = novo_email
            if novo_fone:  cliente["Telefone"] = novo_fone
            break

    if not encontrado:
        print(f"\n  [!] Nenhum cliente com ID {id_busca} encontrado.")
    else:
        salvar_todos_clientes(clientes)
        print("\n  [✓] Cliente atualizado com sucesso!")

    input("\n  Pressione ENTER para continuar...")


# ─────────────────────────────────────────────
#  DELETE — Excluir cliente
# ─────────────────────────────────────────────

def excluir_cliente():
    print("\n  ── Excluir Cliente ──")
    listar_clientes_resumido()

    try:
        id_busca = int(input("\n  Digite o ID do cliente a excluir: ").strip())
    except ValueError:
        print("\n  [!] ID inválido.")
        input("\n  Pressione ENTER para continuar...")
        return

    clientes = ler_todos_clientes()
    nova_lista = [c for c in clientes if int(c.get("ID", -1)) != id_busca]

    if len(nova_lista) == len(clientes):
        print(f"\n  [!] Nenhum cliente com ID {id_busca} encontrado.")
    else:
        confirmacao = input(f"\n  Tem certeza que deseja excluir o cliente ID {id_busca}? (s/n): ").strip().lower()
        if confirmacao == 's':
            salvar_todos_clientes(nova_lista)
            print("\n  [✓] Cliente excluído com sucesso!")
        else:
            print("\n  Operação cancelada.")

    input("\n  Pressione ENTER para continuar...")


# ─────────────────────────────────────────────
#  Auxiliar: lista resumida (usada internamente)
# ─────────────────────────────────────────────

def listar_clientes_resumido():
    clientes = ler_todos_clientes()
    if not clientes:
        print("\n  Nenhum cliente cadastrado.")
    else:
        print()
        for c in clientes:
            print(f"  ID: {c.get('ID','?')} — {c.get('Nome','?')}")
