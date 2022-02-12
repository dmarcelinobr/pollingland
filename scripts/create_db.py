# 01_create_db.py
import sqlite3

# criando e conectando...
conn = sqlite3.connect('pollingpoints.db')
# desconectando...
conn.close()
