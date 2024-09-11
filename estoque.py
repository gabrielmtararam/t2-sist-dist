import redis
from warehouse import Warehouse

class EstoquePartes:
    def __init__(self, host='172.20.0.2', port=6379):
        self.redis = redis.Redis(host=host, port=port, db=0)
        # Níveis para controle Kanban
        self.kanban_niveis = {
            'verde': 100,
            'amarelo': 50,
            'vermelho': 20
        }

    def incrementar(self, parte, quantidade):
        atual = int(self.redis.get(parte) or 0)
        self.redis.set(parte, atual + quantidade)
        self.verificar_nivel_kanban(parte)

    def decrementar(self, parte, quantidade):
        atual = int(self.redis.get(parte) or 0)
        if atual >= quantidade:
            self.redis.set(parte, atual - quantidade)
            self.verificar_nivel_kanban(parte)
            return True
        return False

    def verificar(self, parte):
        return int(self.redis.get(parte) or 0)

    def verificar_nivel_kanban(self, parte):
        nivel = self.verificar(parte)
        if nivel >= self.kanban_niveis['verde']:
            print(f"Parte {parte} está em Nível Verde ({nivel}).")
        elif nivel >= self.kanban_niveis['amarelo']:
            print(f"Parte {parte} está em Nível Amarelo ({nivel}).")
        else:
            print(f"Parte {parte} está em Nível Vermelho ({nivel}). Emitindo ordem de reabastecimento.")
            self.emitir_reabastecimento(parte)

    def emitir_reabastecimento(self, parte):
        # Envia ordem de reabastecimento para o warehouse
        warehouse = Warehouse(self.redis)
        warehouse.processar_reabastecimento(parte)




class EstoqueProdutos:
    def __init__(self, host='172.20.0.2', port=6379):
        self.redis = redis.Redis(host=host, port=port, db=0)
        # Níveis para controle K

    def incrementar(self, produto, quantidade):
        atual = int(self.redis.get(produto) or 0)
        self.redis.set(produto, atual + quantidade)

    def decrementar(self, produto, quantidade):
        atual = int(self.redis.get(produto) or 0)
        if atual >= quantidade:
            self.redis.set(produto, atual - quantidade)
            return True
        return False

    def verificar(self, produto):
        return int(self.redis.get(produto) or 0)
