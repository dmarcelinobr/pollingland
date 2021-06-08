# 11_backup.py
import sqlite3
import io

conn = sqlite3.connect('pollingpoint.db')

with io.open('pollingpoint_dump.sql', 'w') as f:
    for linha in conn.iterdump():
        f.write('%s\n' % linha)

print('Backup realizado com sucesso.')
print('Salvo como pollingpoint_dump.sql')

conn.close()
