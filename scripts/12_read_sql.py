# 12_read_sql.py
import sqlite3
import io

conn = sqlite3.connect('pollingpoint_bkp.db')
cursor = conn.cursor()

f = io.open('sql/pollingpoint_bkp.sql', 'r')
sql = f.read()
cursor.executescript(sql)

print('Banco de dados recuperado com sucesso.')
print('Salvo como pollingpoint_bkp.db')

conn.close()
