import json

import pika
import time
import random
import threading
import sys

rabbitmq_host = 'rabbitmq'
exchange = 'direct_exchange'


container_name = "deposito"
container_fabrica = "fabrica"

def solicitar_produtos_para_fabrica(produto, qtd):

    message = {
        "produzir":{
            "produto":produto,
            "qtd":qtd,
        }
    }
    json_message = json.dumps(message)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.basic_publish(exchange=exchange, routing_key=container_fabrica, body=json_message)
    print(f"{container_name} published: {json_message} to {container_fabrica}", flush=True)


def consume_messages():
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()

    channel.queue_declare(queue=container_name)
    channel.queue_bind(exchange=exchange, queue=container_name, routing_key=container_name)

    def callback(ch, method, properties, body):
        message = json.loads(body)
        print(f"{container_name} received: {message}", flush=True)
        if "produzir" in message:
            solicitar_produtos_para_fabrica(message["produzir"]["produto"],message["produzir"]["qtd"])
        if "produzido" in message:
            print(f'produziu {message["produzido"]["produto"],message["produzido"]["qtd"]}')
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
    setup_rabbitmq()
    consume_messages()

if __name__ == '__main__':
    main()
