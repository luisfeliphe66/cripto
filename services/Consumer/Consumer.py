import pika
import json
import logging
from pymongo import MongoClient

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Conectar ao MongoDB
def connect_to_mongodb():
    client = MongoClient('mongodb://admin:password@mongodb:27017/')
    db = client['BTCBRL']
    collection = db['BTC']
    return collection

# Função para conectar ao RabbitMQ e declarar a fila
def connect_to_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    queue_name = 'metric_BTC'
    channel.queue_declare(queue=queue_name, durable=True)
    return connection, channel, queue_name

# Função para processar e salvar a mensagem no MongoDB
def callback(ch, method, properties, body):
    message = json.loads(body.decode())
    logger.info(f"Mensagem recebida: {message}")
    
    # Salvar a mensagem no MongoDB
    collection.insert_one(message)
    logger.info(f"Mensagem salva no MongoDB: {message}")


    # Acknowledge que a mensagem foi processada
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Conectar ao RabbitMQ e MongoDB
connection, channel, queue_name = connect_to_rabbitmq()
collection = connect_to_mongodb()

try:
    # Consome mensagens da fila
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    logger.info('Aguardando mensagens. Pressione CTRL+C para sair.')
    channel.start_consuming()

except KeyboardInterrupt:
    logger.info('Interrompido pelo usuário.')

finally:
    # Feche a conexão com o RabbitMQ
    connection.close()
    logger.info('Conexão com RabbitMQ fechada.')