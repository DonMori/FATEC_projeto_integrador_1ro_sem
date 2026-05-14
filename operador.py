import os
import json
from caminhos import PASTA_DADOS, ARQUIVO_OPERADOR


def garantir_arquivo():
    os.makedirs(PASTA_DADOS, exist_ok=True)
    if not os.path.exists(ARQUIVO_OPERADOR):
        with open(ARQUIVO_OPERADOR, 'w', encoding='utf-8') as f:
            json.dump({"nome": ""}, f)  # começa com nome vazio


# ── MUDANÇA PRINCIPAL ──
# Antes (TXT): lia o arquivo inteiro como texto simples com f.read()
# Agora (JSON): carrega um dicionário {"nome": "Felipe"} diretamente

def ler_operador():
    garantir_arquivo()
    with open(ARQUIVO_OPERADOR, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    nome = dados.get("nome", "").strip()
    return nome if nome else None


def salvar_operador(nome):
    garantir_arquivo()
    with open(ARQUIVO_OPERADOR, 'w', encoding='utf-8') as f:
        json.dump({"nome": nome}, f, ensure_ascii=False, indent=4)


def configurar_operador():
    nome = ler_operador()
    if nome:
        print(f"\n  Bem-vindo de volta, {nome}!")
        input("  Pressione ENTER para continuar...")
    else:
        print("\n  ── Primeiro Acesso ──")
        print("  Nenhum operador cadastrado. Vamos configurar agora.\n")
        while True:
            novo_nome = input("  Digite o nome do operador: ").strip()
            if novo_nome:
                salvar_operador(novo_nome)
                print(f"\n  [✓] Operador '{novo_nome}' cadastrado com sucesso!")
                input("  Pressione ENTER para continuar...")
                break
            else:
                print("  [!] O nome não pode estar vazio.")


def trocar_operador():
    atual = ler_operador()
    print(f"\n  ── Trocar Operador ──")
    if atual:
        print(f"  Operador atual: {atual}")

    while True:
        novo_nome = input("\n  Digite o novo nome do operador: ").strip()
        if novo_nome:
            salvar_operador(novo_nome)
            print(f"\n  [✓] Operador atualizado para '{novo_nome}'!")
            input("\n  Pressione ENTER para continuar...")
            break
        else:
            print("  [!] O nome não pode estar vazio.")
