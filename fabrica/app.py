import json

import pika
import time
import random
import threading
import sys

rabbitmq_host = 'rabbitmq'
exchange = 'direct_exchange'


container_name = "fabrica"
container_deposito_produtos = 'deposito'
container_estoque = 'estoque'
container_linha = 'linha_producao'
qtd_producao = 0


def receber_ordem_producao(produto, qtd):
    global qtd_producao
    qtd_producao += 1
    id_solicitacao = f"qtd_producao_{qtd_producao}_container_name"
    message = {
        "produzir":{
            "produto":produto,
            "qtd":qtd,
            "id_solicitacao_fabrica":id_solicitacao,
            "fabrica":container_name,
        }
    }
    json_message = json.dumps(message)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.basic_publish(exchange=exchange, routing_key=container_linha, body=json_message)
    print(f"{container_name} published: {json_message} to {container_linha}", flush=True)

def receber_produto(produto, qtd):
    global qtd_producao
    message = {
        "produziu": {
            "produto": produto,
            "qtd": qtd,
        }
    }
    json_message = json.dumps(message)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.basic_publish(exchange=exchange, routing_key=container_deposito_produtos, body=json_message)
    print(f"{container_name} published: {json_message} to {container_deposito_produtos}", flush=True)

def consume_messages():
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()

    channel.queue_declare(queue=container_name)
    channel.queue_bind(exchange=exchange, queue=container_name, routing_key=container_name)

    def callback(ch, method, properties, body):
        message = json.loads(body)
        print(f"{container_name} received: {message}", flush=True)
        if "produzir" in message:
            receber_ordem_producao(message["produzir"]["produto"],message["produzir"]["qtd"])
        if "produziu" in message:
            receber_produto(message["produziu"]["produto"],message["produziu"]["qtd"])
    # Consumir mensagens
    channel.basic_consume(queue=container_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


def setup_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()

    # Declarar exchange do tipo direct
    channel.exchange_declare(exchange=exchange, exchange_type='direct')

    # Declarar fila específica para este container
    channel.queue_declare(queue=container_name)
    channel.queue_bind(exchange=exchange, queue=container_name, routing_key=container_name)


def main():
    # Configuração do RabbitMQ
    setup_rabbitmq()

    consume_messages()

if __name__ == '__main__':
    main()
