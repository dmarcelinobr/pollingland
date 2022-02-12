# 10_view_table_info.py
import sqlite3

conn = sqlite3.connect('pollingpoints.db')
cursor = conn.cursor()
nome_tabela = 'eleitoral'

# obtendo informações da tabela
cursor.execute('PRAGMA table_info({})'.format(nome_tabela))

colunas = [tupla[1] for tupla in cursor.fetchall()]
print('Colunas:', colunas)
# ou
# for coluna in colunas:
#    print(coluna)

# listando as tabelas do bd
cursor.execute("""
SELECT empresa FROM sqlite_master WHERE type='table' ORDER BY empresa
""")

print('Tabelas:')
for tabela in cursor.fetchall():
    print("%s" % (tabela))

# obtendo o schema da tabela
cursor.execute("""
SELECT sql FROM sqlite_master WHERE type='table' AND name=?
""", (nome_tabela,))

print('Schema:')
for schema in cursor.fetchall():
    print("%s" % (schema))

conn.close()
