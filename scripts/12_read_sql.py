# 12_read_sql.py
import sqlite3
import io

conn = sqlite3.connect('pollingpoint_recuperado.db')
cursor = conn.cursor()

f = io.open('pollingpoint_dump.sql', 'r')
sql = f.read()
cursor.executescript(sql)

print('Banco de dados recuperado com sucesso.')
print('Salvo como pollingpoint_recuperado.db')

conn.close()
