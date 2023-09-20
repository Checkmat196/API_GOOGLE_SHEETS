# Bibliotecas

import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import datetime as dt
import pyodbc


# Caminho para o arquivo de credenciais do serviço Google
CREDENTIALS_FILE = 'CREDENCIAIS.json'
EXCEL_FILE = 'CHAMADOS_KEDU_RISCO.xlsx'
GOOGLE_SHEET_NAME = 'CHAMADOS_KEDU_RISCO'
# Token e ID da sala do telegram
TOKEN = '6610481082:AAFLElSIDG9szP8PloKRlq_J6xRqakcPfTc'
CHAT_ID = '-916560294'
# Consulta do sql
QUERY = 'Query.SQL'


# Parâmetros da conexão
SERVER = '35.196.69.75'
DATABASE = 'glpi-db'
USERNAME = 'mis-read'
PASSWORD = 'N*>M@tI`t^Ip|ag:'

# Conexão com o SQL
connection_string = f'DRIVER={{MySQL odbc 8.0 ANSI Driver}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'


conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Ler o conteúdo do arquivo sql
with open('Query.sql', 'r') as file:
    query = file.read()

# Usar read_sql_query para executar a consulta
df = pd.read_sql_query(query, conn)

# Configuração da API do Google Sheets
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)

# Abra a planilha e selecione a primeira aba
sheet = client.open(GOOGLE_SHEET_NAME).worksheet("chamados")

# Leia o arquivo Excel usando pandas (Em caso do banco estiver fora do ar)
#df = pd.read_excel(EXCEL_FILE, engine='openpyxl')

# Converta todas as colunas de Timestamp para string
for col in df.columns:
    if df[col].dtype == 'datetime64[ns]':  # Verifique se a coluna é de tipo Timestamp
        df[col] = df[col].astype(str)  # Converta para string

# Conexão com a api do Telegram

def send_telegram_message(chat_id, token, message):
    base_url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(base_url, data=payload)
    return response.json()

# Organizando o cabeçalho e colunas para computar na sheet online + Report

try:
    rows = [df.columns.tolist()] + df.values.tolist()

    data = rows

    end_col_letter = chr(64 + df.shape[1])  
    range_update = f"A1:{end_col_letter}{len(data) + 1}"

    sheet.update(range_update, data)
    print("Dados atualizados com sucesso!")

    send_telegram_message(CHAT_ID, TOKEN, "Dados atualizados com sucesso no Google Sheets!")
except Exception as e:
    print("Ocorreu um erro ao atualizar os dados!")
    print(str(e))
    send_telegram_message(CHAT_ID, TOKEN, f"Erro ao atualizar os dados no Google Sheets! Detalhes: {str(e)}")