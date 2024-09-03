import pymongo
import mysql.connector
from mysql.connector import Error
from bson import ObjectId

# Conexão com MongoDB
mongo_client = pymongo.MongoClient("mongodb://admin:password@mongodb:27017/")
mongo_db = mongo_client["BTCBRL"]
mongo_collection = mongo_db["BTC"]

# Conexão com MariaDB
def connect_to_mariadb():
    try:
        mariadb_connection = mysql.connector.connect(
            host="mariadb",
            user="admin",
            password="admin",
            database="BTC",
            charset="utf8mb4",
            collation="utf8mb4_general_ci"
        )
        return mariadb_connection
    except Error as e:
        print(f"Erro ao conectar ao MariaDB: {e}")
        return None

# # Função para inserir registros no MariaDB
def insert_into_mariadb(mariadb_connection, data):
    cursor = mariadb_connection.cursor()

    # Aqui você precisa personalizar o SQL de inserção de acordo com a estrutura de seus dados
    sql_insert_query = """INSERT INTO BTCBRL (name, pctChange, create_date)
                          VALUES (%s, %s, %s)"""

    try:
        cursor.executemany(sql_insert_query, data)
        mariadb_connection.commit()
        print(f"{cursor.rowcount} registros foram inseridos.")
    except Error as e:
        print(f"Erro ao inserir no MariaDB: {e}")
        mariadb_connection.rollback()

# Extrair todos os registros do MongoDB
def fetch_mongodb_data():
    records = []
    for record in mongo_collection.find():
        # print(record)
        nome = convert_mongodb_data(record.get('name', None))
        variacao = convert_mongodb_data(record.get('pctChange', None))
        data_criacao = convert_mongodb_data(record.get('create_date', None))

        # Suponha que os campos do MongoDB
        # Você pode adaptar isso conforme a estrutura dos seus documentos MongoDB
        records.append((nome, variacao, data_criacao))
    return records

def main():
    # Buscar dados do MongoDB
    mongodb_data = fetch_mongodb_data()
    print(mongodb_data)

    # Conectar ao MariaDB e inserir os dados
    mariadb_connection = connect_to_mariadb()
    if mariadb_connection:
        insert_into_mariadb(mariadb_connection, mongodb_data)
        mariadb_connection.close()

def convert_mongodb_data(record):
    # Converte o ObjectId para string
    if isinstance(record, ObjectId):
        return str(record)
    
    # Se o dado for uma lista ou dicionário, faça a conversão para string
    if isinstance(record, (list, dict)):
        return str(record)

    # Outros tipos podem ser retornados diretamente (int, float, etc.)
    return record



if __name__ == "__main__":
    main()