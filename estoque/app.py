import json

import pika
import time
import random
import threading
import sys

pecas_em_estoque = [0] * 100
rabbitmq_host = 'rabbitmq'
exchange = 'direct_exchange'

# Nome do container é passado como argumento (container1 ou container2)
container_name = "estoque"
container_deposito_produtos = 'deposito'
container_estoque = 'estoque'
container_linha = 'linha_producao'
container_fornecedor = 'fornecedor'
solicitacoes = {}
margem_pecas_a_mais = 10


def publish_message(channel, message):
    # Converter a mensagem em string e garantir codificação correta
    if not isinstance(message, str):
        message = str(message)
    channel.basic_publish(exchange=exchange, routing_key=container_deposito_produtos, body=message.encode('utf-8'))
    print(f"{container_name} published: {message}")


def enviar_peca(peca, qtd, id_solicitacao_linha, linha):
    pecas_em_estoque[peca]-=qtd
    message = {
        "enviando_pecas":{
            "peca":peca,
            "qtd":qtd,
            "id_solicitacao_linha":id_solicitacao_linha,
            "linha":linha,
        }
    }
    json_message = json.dumps(message)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.basic_publish(exchange=exchange, routing_key=linha, body=json_message)
    print(f"{container_name} published: {json_message} to {linha}", flush=True)
def solicitacao_peca(peca, qtd, id_solicitacao_linha, linha):
    global solicitacoes
    if (pecas_em_estoque[peca]>=qtd):
        enviar_peca(peca, qtd, id_solicitacao_linha, linha)
    else:
        qtd = qtd-pecas_em_estoque[peca]+margem_pecas_a_mais
        if (id_solicitacao_linha not in solicitacoes):
            solicitacoes[id_solicitacao_linha] = {
                "linha": linha,
            }
        message = {
            "solicitacao_peca": {
                "peca": peca,
                "qtd": qtd,
                "id_solicitacao_linha": id_solicitacao_linha,
            }
        }
        json_message = json.dumps(message)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
        channel = connection.channel()
        channel.basic_publish(exchange=exchange, routing_key=container_fornecedor, body=json_message)
        print(f"{container_name} published: {json_message} to {container_fornecedor}", flush=True)

def recebimento_peca(peca, qtd, id_solicitacao_linha):
    if (id_solicitacao_linha in solicitacoes):
        linha = solicitacoes[id_solicitacao_linha]["linha"]
        enviar_peca(peca, qtd, id_solicitacao_linha, linha)

def consume_messages():
    # Configurar um canal separado para consumo
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()

    # Declarar a fila do container
    channel.queue_declare(queue=container_name)

    # Ligar a fila à exchange com a chave de roteamento apropriada
    channel.queue_bind(exchange=exchange, queue=container_name, routing_key=container_name)

    # Função callback para processar mensagens recebidas
    def callback(ch, method, properties, body):
        message = json.loads(body)
        print(f"{container_name} received: {message}", flush=True)
        if "solicitacao_peca" in message:
            solicitacao_peca(message["solicitacao_peca"]["peca"], message["solicitacao_peca"]["qtd"],
                                   message["solicitacao_peca"]["id_solicitacao_linha"],
                                   message["solicitacao_peca"]["linha"])
        if "enviando_pecas" in message:
            recebimento_peca(message["enviando_pecas"]["peca"], message["enviando_pecas"]["qtd"],
                                   message["enviando_pecas"]["id_solicitacao_linha"],
                                  )
    # Consumir mensagens
    channel.basic_consume(queue=container_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

    print("###################inicio", flush=True)

def setup_rabbitmq():
    # Configuração do RabbitMQ (conexão e canais)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()

    # Declarar exchange do tipo direct
    channel.exchange_declare(exchange=exchange, exchange_type='direct')

    # Declarar fila específica para este container
    channel.queue_declare(queue=container_name)

    # Ligar a fila à exchange com a chave de roteamento apropriada
    channel.queue_bind(exchange=exchange, queue=container_name, routing_key=container_name)


def main():
    # Configuração do RabbitMQ
    setup_rabbitmq()
    print("main estoque", flush=True)
    # Enviar uma mensagem inicial assim que o container for iniciado
    # receber_ordem_producao("Pv1",5)


    # Thread para publicar mensagens periodicamente

    # Consumir mensagens
    consume_messages()

if __name__ == '__main__':
    main()
