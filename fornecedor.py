class Fornecedor:
    def __init__(self, redis_connection):
        self.redis = redis_connection

    def enviar_pecas(self, parte):
        print(f"Fornecedor enviando 100 unidades de {parte}.")
        # Reabastece tanto o EstoquePartes do warehouse quanto o EstoquePartes da linha de produção
        self.redis.set(f"warehouse:{parte}", 100)
