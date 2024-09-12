import json

import pika
import time

rabbitmq_host = 'rabbitmq'
exchange = 'direct_exchange'


container_name = "ordens"
container_deposito_produtos = 'deposito'
container_estoque = 'estoque'


def solicitar_produtos_para_deposito(produto, qtd):

    message = {
        "produzir":{
            "produto":produto,
            "qtd":qtd,
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
        print(f"{container_name} received: {body.decode()}")

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
    # Enviar uma mensagem de solicitação de produtos assim que o container for iniciado
    time.sleep(5)
    solicitar_produtos_para_deposito("Pv1", 7)


    # Consumir mensagens
    consume_messages()

if __name__ == '__main__':
    main()
