import json

import pika
import time
import random
import threading
import sys

rabbitmq_host = 'rabbitmq'
exchange = 'direct_exchange'

# Nome do container é passado como argumento (container1 ou container2)
container_name = "linha_producao"
container_deposito_produtos = 'deposito'
container_estoque = 'estoque'

PRODUTOS = {'Pv1': [58, 98, 45, 65, 53, 11, 41, 46, 30, 35, 90, 65, 21, 58, 49, 2, 35, 70, 43, 47, 63, 13, 53, 17, 0, 1, 2, 3, 4,
         5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
         34, 35, 36, 37, 38, 39, 40, 41, 42],
 'Pv2': [70, 46, 67, 3, 40, 63, 24, 62, 60, 81, 59, 67, 87, 58, 75, 100, 43, 15, 47, 42, 62, 39, 79, 31, 61, 76, 76, 2,
         0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
         30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42],
 'Pv3': [41, 2, 98, 21, 41, 99, 51, 2, 78, 54, 94, 60, 93, 99, 11, 91, 77, 35, 98, 66, 46, 71, 30, 50, 0, 1, 2, 3, 4, 5,
         6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
         35, 36, 37, 38, 39, 40, 41, 42],
 'Pv4': [84, 17, 58, 50, 99, 73, 83, 26, 15, 89, 24, 87, 79, 86, 57, 30, 44, 8, 44, 90, 36, 89, 99, 69, 82, 50, 28, 52,
         56, 52, 32, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
         27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42],
 'Pv5': [13, 19, 60, 78, 19, 47, 80, 38, 86, 36, 71, 70, 4, 50, 57, 40, 34, 65, 2, 22, 65, 25, 6, 4, 14, 39, 0, 1, 2, 3,
         4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32,
         33, 34, 35, 36, 37, 38, 39, 40, 41, 42]}

solicitacoes = {}

def publish_message(channel, message):
    # Converter a mensagem em string e garantir codificação correta
    if not isinstance(message, str):
        message = str(message)
    channel.basic_publish(exchange=exchange, routing_key=container_deposito_produtos, body=message.encode('utf-8'))
    print(f"{container_name} published: {message}")

def receber_ordem_producao(produto, qtd, id_solicitacao_fabrica, fabrica):
    id_solicitacao_linha = f"{id_solicitacao_fabrica}-{container_name}"
    if produto in PRODUTOS:

        if (id_solicitacao_linha not in solicitacoes):
            solicitacoes[id_solicitacao_linha] = {
                "fabrica": fabrica,
                "produto": produto,
                "qtd": qtd,
                "pecas": [],
                "pecas_necessarias": PRODUTOS[produto]
            }

        for peca in PRODUTOS[produto]:
            id_solicitacao_linha_peca = f"{id_solicitacao_linha}-{peca}"
            message = {
                "solicitacao_peca":{
                    "peca":peca,
                    "qtd":qtd,
                    "id_solicitacao_linha":id_solicitacao_linha,
                    "linha":container_name,
                }
            }
            json_message = json.dumps(message)
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
            channel = connection.channel()
            channel.basic_publish(exchange=exchange, routing_key=container_estoque, body=json_message)
            print(f"{container_name} published: {json_message} to {container_estoque}", flush=True)

def receber_peca(peca, qtd, id_solicitacao_linha):
    if id_solicitacao_linha in solicitacoes:
        solicitacoes[id_solicitacao_linha]["pecas"].append(peca)
        if sorted(solicitacoes[id_solicitacao_linha]["pecas_necessarias"]) == sorted(solicitacoes[id_solicitacao_linha]["pecas"]):
            message = {
                "produziu": {
                    "produto": solicitacoes[id_solicitacao_linha]["produto"],
                    "qtd": solicitacoes[id_solicitacao_linha]["qtd"],
                }
            }
            json_message = json.dumps(message)
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
            channel = connection.channel()
            channel.basic_publish(exchange=exchange, routing_key=solicitacoes[id_solicitacao_linha]["fabrica"], body=json_message)
            print(f"{container_name} published: {json_message} to {solicitacoes[id_solicitacao_linha]['fabrica']}", flush=True)
        # if produto in PRODUTOS:
        #     for peca in PRODUTOS[produto]:
        #         message = {
        #             "solicitacao_peca":{
        #                 "peca":peca,
        #                 "qtd":qtd,
        #                 "id_solicitacao_linha":id_solicitacao_linha,
        #                 "linha":container_name,
        #             }
        #         }
        #         json_message = json.dumps(message)
        #         connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
        #         channel = connection.channel()
        #         channel.basic_publish(exchange=exchange, routing_key=container_estoque, body=json_message)
        #         print(f"{container_name} published: {json_message} to {container_estoque}", flush=True)
# def publish_initial_message(channel):
#     # Enviar a primeira mensagem assim que o container iniciar
#     message = f"Initial message from {container_name} to {target_container}"
#     publish_message(channel, message)

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
        if "produzir" in message:
            receber_ordem_producao(message["produzir"]["produto"],message["produzir"]["qtd"],message["produzir"]["id_solicitacao_fabrica"],message["produzir"]["fabrica"])
        if "enviando_pecas" in message:
            receber_peca(message["enviando_pecas"]["peca"], message["enviando_pecas"]["qtd"],
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
    print("#########################main", flush=True)
    # Enviar uma mensagem inicial assim que o container for iniciado
    # receber_ordem_producao("Pv1",5)


    # Thread para publicar mensagens periodicamente

    # Consumir mensagens
    consume_messages()

if __name__ == '__main__':
    main()
print("#############################################abriu a fabrica", flush=True)