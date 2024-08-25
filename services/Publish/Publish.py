import pika
import requests
import json
import time
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Função para conectar ao RabbitMQ e declarar a fila
def connect_to_rabbitmq():
    try:
        logger.info('Conectando ao RabbitMQ...')
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()
        queue_name = 'metric_BTC'
        channel.queue_declare(queue=queue_name, durable=True)
        logger.info('Conectado ao RabbitMQ e fila declarada.')
        return connection, channel, queue_name
    except Exception as e:
        logger.error(f'Erro ao conectar ao RabbitMQ: {e}')
        raise

# URL da API
api_url = 'https://economia.awesomeapi.com.br/json/last/BTC'

# Função para buscar dados da API
def fetch_data_from_api(api_url):
    try:
        logger.info('Fazendo requisição para a API...')
        response = requests.get(api_url)
        logger.info(f'Resposta recebida: {response.status_code}')
        response.raise_for_status()
        data = response.json()
        logger.info(f'Dados recebidos: {data}')
        return data
    except requests.RequestException as e:
        logger.error(f'Erro ao buscar dados da API: {e}')
        raise


# Conectar ao RabbitMQ
connection, channel, queue_name = connect_to_rabbitmq()

try:
    while True:
        # Busque os dados da API
        data = fetch_data_from_api(api_url)

        # Publique os dados na fila
        if isinstance(data, dict):
            # Caso a resposta seja um dicionário
            for key, item in data.items():
                message = json.dumps(item)  # Converta o item em uma string JSON
                channel.basic_publish(
                    exchange='',
                    routing_key=queue_name,
                    body=message,
                    properties=pika.BasicProperties(
                        delivery_mode=2,  # Torna a mensagem persistente
                    )
                )
                logger.info(f"Mensagem enviada: {message}")
        elif isinstance(data, list):
            # Caso a resposta seja uma lista
            for item in data:
                message = json.dumps(item)  # Converta o item em uma string JSON
                channel.basic_publish(
                    exchange='',
                    routing_key=queue_name,
                    body=message,
                    properties=pika.BasicProperties(
                        delivery_mode=2,  # Torna a mensagem persistente
                    )
                )
                logger.info(f"Mensagem enviada: {message}")
        else:
            logger.error('Formato de dados recebido inesperado.')

        # Atraso de 60 segundos
        logger.info('Aguardando 60 segundos antes da próxima consulta...')
        time.sleep(60)

except KeyboardInterrupt:
    logger.info('Interrompido pelo usuário.')

finally:
    # Feche a conexão com o RabbitMQ
    if 'connection' in locals() and connection.is_open:
        connection.close()
        logger.info('Conexão com RabbitMQ fechada.')
