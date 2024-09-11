from fornecedor import Fornecedor

class Warehouse:
    def __init__(self, redis_connection):
        self.redis = redis_connection
        self.nivel_minimo = 50  # Nível crítico para considerar pedido a fornecedor

    def processar_reabastecimento(self, parte):
        # Verificar se há estoque suficiente no warehouse
        estoque_atual = int(self.redis.get(f"warehouse:{parte}") or 0)
        if estoque_atual >= self.nivel_minimo:
            print(f"Reabastecendo parte {parte} a partir do estoque do warehouse.")
            self.redis.set(parte, estoque_atual + 50)
            self.redis.set(f"warehouse:{parte}", estoque_atual - 50)
        else:
            print(f"Estoque do warehouse insuficiente para parte {parte}, solicitando ao fornecedor.")
            fornecedor = Fornecedor(self.redis)
            fornecedor.enviar_pecas(parte)
