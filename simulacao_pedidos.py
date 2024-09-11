import random
from estoque import EstoqueProdutos, EstoquePartes

def gerar_pedidos(estoque_produtos, estoque_partes):
    # Produtos
    produtos = ['Pv1', 'Pv2', 'Pv3', 'Pv4', 'Pv5']
    
    # Gerar pedidos aleatórios de 0 a 100 para cada produto
    pedidos = {produto: random.randint(0, 100) for produto in produtos}

    # Processar os pedidos
    for produto, quantidade in pedidos.items():
        # Verificar o nível de estoque do produto
        nivel_estoque = estoque_produtos.verificar(produto)
        
        # Se o nível de estoque for menor que o pedido, produzir o necessário
        if nivel_estoque < quantidade:
            falta = quantidade - nivel_estoque
            print(f"Estoque insuficiente para {produto}. Pedido: {quantidade}, Estoque atual: {nivel_estoque}. Produzindo {falta} unidades.")
            # Produzir o necessário usando as partes do estoque
            estoque_partes.emitir_reabastecimento(produto)
            estoque_produtos.incrementar(produto, falta)
        
        # Reduzir o estoque conforme o pedido
        estoque_produtos.decrementar(produto, quantidade)
        print(f"Pedido processado: {produto}, Quantidade: {quantidade}, Estoque atual: {estoque_produtos.verificar(produto)}")

    return pedidos