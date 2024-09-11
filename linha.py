from buffer import Buffer
from produtos import Produto

PRODUTOS = {'Pv1': [58, 98, 45, 65, 53, 11, 41, 46, 30, 35, 90, 65, 21, 58, 49, 2, 35, 70, 43, 47, 63, 13, 53, 17, 0, 1, 2, 3, 4,
         5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
         34, 35, 36, 37, 38, 39, 40, 41, 42],
 'Pv2': [70, 46, 67, 3, 40, 63, 24, 62, 60, 81, 59, 67, 87, 58, 75, 100, 43, 15, 47, 42, 62, 39, 79, 31, 61, 76, 76, 2,
         0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
         30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42],
 'Pv3': [41, 2, 98, 21, 41, 99, 51, 2, 78, 54, 94, 60, 93, 99, 11, 91, 77, 35, 98, 66, 46, 71, 30, 50, 0, 1, 2, 3, 4, 5,
         6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
         35, 36, 37, 38, 39, 40, 41, 42],
 'Pv4': [84, 17, 58, 50, 99, 73, 83, 26, 15, 89, 24, 87, 79, 86, 57, 30, 44, 8, 44, 90, 36, 89, 99, 69, 82, 50, 28, 52,
         56, 52, 32, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
         27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42],
 'Pv5': [13, 19, 60, 78, 19, 47, 80, 38, 86, 36, 71, 70, 4, 50, 57, 40, 34, 65, 2, 22, 65, 25, 6, 4, 14, 39, 0, 1, 2, 3,
         4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32,
         33, 34, 35, 36, 37, 38, 39, 40, 41, 42]}
class LinhaProducao:
    def __init__(self, nome, tamanho_buffer):
        self.nome = nome
        self.buffer = Buffer(tamanho_buffer)

    def produzir(self, produto, estoque_partes, estoque_produtos, qtd):
        produziu = True
        if produto in PRODUTOS:
            for parte in PRODUTOS[produto]:
                if estoque_partes.decrementar(parte, qtd):
                    self.buffer.adicionar((parte, qtd))
                    print(f"[{self.nome}] Produzido {produto}, consumindo 1 de {parte}")
                else:
                    print(f"[{self.nome}] EstoquePartes insuficiente de {parte}. Solicitando reabastecimento.")
                    # Integração com o sistema Kanban para reabastecimento
                    estoque_partes.verificar_nivel_kanban(parte)  # Solicita reabastecimento se necessário
                    print(f"[{self.nome}] Aguardando reabastecimento de {parte}.")
                    produziu = False
            if produziu:
                print(f"produziu {produto} {qtd}")
                estoque_produtos.incrementar(produto, qtd)
        else:
            print(f"[{self.nome}] Produto {produto} não encontrado.")
    
    def consumir(self):
        item = self.buffer.consumir()
        if item:
            parte, quantidade = item
            print(f"[{self.nome}] Consumido {quantidade} de {parte} do buffer")
        else:
            print(f"[{self.nome}] Buffer vazio, nada a consumir.")
    
    def status_buffer(self):
        return self.buffer.nivel_atual()
