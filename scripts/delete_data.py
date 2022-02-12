# 08_delete_data.py
import sqlite3

conn = sqlite3.connect('pollingpoints.db')
cursor = conn.cursor()

cpf = '000.000.000-00'

# excluindo um registro da tabela
cursor.execute("""
DELETE FROM pollsters
WHERE cpf = ?
""", (cpf,))

conn.commit()

print('Registro excluido com sucesso.')

conn.close()
