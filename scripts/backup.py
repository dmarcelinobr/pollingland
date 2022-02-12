# 11_backup.py
import sqlite3
import io

conn = sqlite3.connect('pollingpoints.db')

with io.open('pollingpoints_dump.sql', 'w') as f:
    for linha in conn.iterdump():
        f.write('%s\n' % linha)

print('Backup realizado com sucesso.')
print('Salvo como pollingpoints_dump.sql')

conn.close()
