# connect_db.py
import sqlite3

# conectando...
conn = sqlite3.connect('pollingpoint.db')
# desconectando...
conn.close()
