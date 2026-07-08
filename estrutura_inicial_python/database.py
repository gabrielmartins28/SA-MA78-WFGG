import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def conectar():
    conexao = mysql.connector.connect(
        host = os.getenv('DB_HOST'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD'),
        database = os.getenv('DB_NAME'),
        port = int(os.getenv('DB_PORT')) # Convertido para número inteiro
    )
    
    print("✅ Conexão feita com sucesso!")
    return conexao

conectar()

