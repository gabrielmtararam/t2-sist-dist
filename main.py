from fabrica import Fabrica
from estoque import Estoque

# Configuração inicial das fábricas
linhas_fabrica1 = {
    "linha1": {"tamanho_buffer": 100},
    "linha2": {"tamanho_buffer": 100},
    "linha3": {"tamanho_buffer": 100},
    "linha4": {"tamanho_buffer": 100},
    "linha5": {"tamanho_buffer": 100},
}

linhas_fabrica2 = {
    "linha1": {"tamanho_buffer": 100},
    "linha2": {"tamanho_buffer": 100},
    "linha3": {"tamanho_buffer": 100},
    "linha4": {"tamanho_buffer": 100},
    "linha5": {"tamanho_buffer": 100},
    "linha6": {"tamanho_buffer": 100},
    "linha7": {"tamanho_buffer": 100},
    "linha8": {"tamanho_buffer": 100},
}

fabrica1 = Fabrica("Fabrica 1", linhas_fabrica1)
fabrica2 = Fabrica("Fabrica 2", linhas_fabrica2)

estoque = Estoque()

def exibir_opcoes():
    print("Escolha uma opção:")
    print("1. Produzir produto")
    print("2. Consumir buffer")
    print("3. Verificar estoque")
    print("4. Status dos Buffers")
    print("5. Sair")

def main():
    while True:
        exibir_opcoes()
        opcao = input("Digite o número da opção desejada: ")

        if opcao == "1":  # Produzir produto
            fabrica = input("Escolha a fábrica (1 ou 2): ")
            linha = input(f"Escolha o número da linha da fábrica {fabrica} (ex: 1 para linha1): ")
            produto = input("Escolha o produto (Pv1, Pv2, Pv3, Pv4, Pv5): ")

            # Formata a linha corretamente com base no número inserido
            linha_nome = f"linha{linha}"
            
            if fabrica == "1":
                fabrica1.produzir_em_linha(linha_nome, produto, estoque)
            elif fabrica == "2":
                fabrica2.produzir_em_linha(linha_nome, produto, estoque)
            else:
                print("Fábrica inválida.")

        elif opcao == "2":  # Consumir buffer
            fabrica = input("Escolha a fábrica (1 ou 2): ")
            linha = input(f"Escolha o número da linha da fábrica {fabrica} (ex: 1 para linha1): ")

            # Formata a linha corretamente com base no número inserido
            linha_nome = f"linha{linha}"

            if fabrica == "1":
                fabrica1.consumir_em_linha(linha_nome)
            elif fabrica == "2":
                fabrica2.consumir_em_linha(linha_nome)
            else:
                print("Fábrica inválida.")

        elif opcao == "3":  # Verificar estoque
            parte = input("Digite o nome da parte para verificar o estoque: ")
            estoque_atual = estoque.verificar(parte)
            print(f"Estoque atual de {parte}: {estoque_atual}")

        elif opcao == "4":  # Status dos Buffers
            fabrica = input("Escolha a fábrica (1 ou 2): ")
            linha = input(f"Escolha o número da linha da fábrica {fabrica} (ex: 1 para linha1): ")

            # Formata a linha corretamente com base no número inserido
            linha_nome = f"linha{linha}"

            if fabrica == "1":
                status = fabrica1.status_buffer_linha(linha_nome)
            elif fabrica == "2":
                status = fabrica2.status_buffer_linha(linha_nome)
            else:
                print("Fábrica inválida.")
            if status is not None:
                print(f"Status do buffer da {linha_nome} da {fabrica}: {status} itens")

        elif opcao == "5":  # Sair
            print("Encerrando simulação.")
            break

        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()
