import os
from cadastro_cliente import (
    adicionar_cliente,
    listar_clientes,
    atualizar_cliente,
    excluir_cliente,
)
from agendamento import (
    criar_agendamento,
    listar_agendamentos,
    atualizar_agendamento,
    excluir_agendamento,
    iniciar_cronometro,
)
from operador import configurar_operador, trocar_operador

# ─────────────────────────────────────────────
#  Utilitário
# ─────────────────────────────────────────────

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


# ─────────────────────────────────────────────
#  Menu
# ─────────────────────────────────────────────

def exibir_menu():
    limpar_tela()
    print("=" * 45)
    print("      SISTEMA DE AGENDAMENTO DE GRAVAÇÕES")
    print("=" * 45)
    print("  ── Clientes ──")
    print("  1 - Adicionar novo cliente")
    print("  2 - Listar clientes")
    print("  3 - Atualizar cliente")
    print("  4 - Excluir cliente")
    print()
    print("  ── Agendamentos ──")
    print("  5 - Criar agendamento")
    print("  6 - Listar agendamentos")
    print("  7 - Atualizar agendamento")
    print("  8 - Excluir agendamento")
    print()
    print("  ── Gravação ──")
    print("  9 - Iniciar cronômetro de gravação")
    print()
    print("  ── Configurações ──")
    print("  10 - Trocar operador")
    print()
    print("  0  - Sair do programa")
    print("=" * 45)

    try:
        escolha = int(input("  Opção: "))
    except ValueError:
        escolha = -1

    return escolha


# ─────────────────────────────────────────────
#  Execução
# ─────────────────────────────────────────────

def executar_funcao(escolha):
    if escolha == 1:
        adicionar_cliente()
    elif escolha == 2:
        listar_clientes()
    elif escolha == 3:
        atualizar_cliente()
    elif escolha == 4:
        excluir_cliente()
    elif escolha == 5:
        criar_agendamento()
    elif escolha == 6:
        listar_agendamentos()
    elif escolha == 7:
        atualizar_agendamento()
    elif escolha == 8:
        excluir_agendamento()
    elif escolha == 9:
        iniciar_cronometro()
    elif escolha == 10:
        trocar_operador()
    elif escolha == 0:
        pass
    else:
        print("\n  [!] Opção inválida! Tente novamente.")
        input("\n  Pressione ENTER para continuar...")


# ─────────────────────────────────────────────
#  Loop principal
# ─────────────────────────────────────────────

def main():
    limpar_tela()
    configurar_operador()  # verifica/cadastra operador ao iniciar

    escolha = -1
    while escolha != 0:
        escolha = exibir_menu()
        if escolha == 0:
            print("\n  Encerrando o sistema... Até logo!\n")
            break
        executar_funcao(escolha)


if __name__ == "__main__":
    main()
