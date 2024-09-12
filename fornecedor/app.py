import json

import pika
import time
import random
import threading
import sys

rabbitmq_host = 'rabbitmq'
exchange = 'direct_exchange'

# Nome do container é passado como argumento (container1 ou container2)
container_name = "fornecedor"
container_estoque = 'estoque'


def enviar_peca(peca, qtd, id_solicitacao):
    message = {
        "enviando_pecas":{
            "peca":peca,
            "qtd":qtd,
            "id_solicitacao_linha":id_solicitacao,
        }
    }
    json_message = json.dumps(message)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.basic_publish(exchange=exchange, routing_key=container_estoque, body=json_message)
    print(f"{container_name} published: {json_message} to {container_estoque}", flush=True)
def solicitacao_peca(peca, qtd, id_solicitacao_linha):
    enviar_peca(peca, qtd, id_solicitacao_linha)

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
