from pymongo import MongoClient
import mysql.connector
from mysql.connector import Error
import schedule
import time
from datetime import datetime
import logging

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[logging.StreamHandler()]  # StreamHandler envia logs para o stdout
)

def fetch_mongodb_data():
    try:
        # Conexão com o MongoDB
        mongo_client = MongoClient("mongodb://admin:password@mongodb:27017/")
        database = mongo_client['BTCBRL']
        collection = database['BTC']

        # Buscando todos os registros da coleção
        documents = collection.find()
        return documents

    except Exception as e:
        logging.error(f"Erro ao conectar ou buscar dados do MongoDB: {e}")

def insert_into_mariadb(records):
    try:
        # Conexão com o MariaDB
        connection = None
        connection = mysql.connector.connect(
            host='mariadb',
            user='admin',
            password='admin',
            database='BTC'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            # Verifica se a tabela BTCBRL existe e cria se não existir
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS BTCBRL (
                    code VARCHAR(255) PRIMARY KEY,
                    codein VARCHAR(255),
                    name VARCHAR(255),
                    high VARCHAR(255),
                    low VARCHAR(255),
                    varBid VARCHAR(255),
                    pctChange VARCHAR(255),
                    bid VARCHAR(255),
                    ask VARCHAR(255),
                    timestamp INT,
                    create_date DATETIME
                ) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
            """)


            # Inserindo os dados no MariaDB
            for record in records:
                insert_query = """
                    INSERT INTO BTCBRL (code, codein, name, high, low, varBid, pctChange, bid, ask, timestamp, create_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    codein = VALUES(codein),
                    name = VALUES(name),
                    high = VALUES(high),
                    low = VALUES(low),
                    varBid = VALUES(varBid),
                    pctChange = VALUES(pctChange),
                    bid = VALUES(bid),
                    ask = VALUES(ask),
                    timestamp = VALUES(timestamp),
                    create_date = VALUES(create_date)
                """
                values = (
                    record.get('code'),  # "BTC"
                    record.get('codein'),  # "BRL"
                    record.get('name'),  # "Bitcoin/Real Brasileiro"
                    float(record.get('high')),  # Ex: "354404"
                    float(record.get('low')),  # Ex: "345786"
                    float(record.get('varBid')),  # Ex: "-5762"
                    float(record.get('pctChange')),  # Ex: "-1.63"
                    float(record.get('bid')),  # Ex: "347443"
                    float(record.get('ask')),  # Ex: "347443"
                    int(record.get('timestamp')),  # Ex: "1724721241"
                    record.get('create_date')  # Ex: "2024-08-26 22:14:01"
                )
                cursor.execute(insert_query, values)

            # Commitando as alterações
            connection.commit()
            logging.info("Dados inseridos com sucesso no MariaDB.")
    except Error as e:
        logging.error(f"Erro ao conectar ou inserir dados no MariaDB: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def job():
    logging.info("Executando o job para buscar e inserir dados.")
    mongo_records = fetch_mongodb_data()
    if mongo_records:
        insert_into_mariadb(mongo_records)

# Agendando o script para ser executado diariamente às 20:00
schedule.every().day.at("03:07").do(job)

if __name__ == "__main__":
    while True:
        logging.info("Checando agendamentos...")
        schedule.run_pending()  # Verifica se há tarefas agendadas para serem executadas
        time.sleep(10)  # Espera 60 segundos antes de verificar novamente