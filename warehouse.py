from fornecedor import Fornecedor

class Warehouse:
    def __init__(self, redis_connection):
        self.redis = redis_connection
        self.nivel_minimo = 50  # Nível crítico para considerar pedido a fornecedor

    def processar_reabastecimento(self, parte):
        # Verificar se há EstoquePartes suficiente no warehouse
        EstoquePartes_atual = int(self.redis.get(f"warehouse:{parte}") or 0)
        if EstoquePartes_atual >= self.nivel_minimo:
            print(f"Reabastecendo parte {parte} a partir do EstoquePartes do warehouse.")
            self.redis.set(parte, EstoquePartes_atual + 50)
            self.redis.set(f"warehouse:{parte}", EstoquePartes_atual - 50)
        else:
            print(f"EstoquePartes do warehouse insuficiente para parte {parte}, solicitando ao fornecedor.")
            fornecedor = Fornecedor(self.redis)
            fornecedor.enviar_pecas(parte)
