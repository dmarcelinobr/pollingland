# 03_create_data_sql.py
import sqlite3

conn = sqlite3.connect('pollingpoints.db')
cursor = conn.cursor()

# inserindo dados na tabela
cursor.execute("""
INSERT OR REPLACE INTO empresas (nome, razao_social, cnpj, email, telefone, cidade, uf, fundacao)
VALUES ('Datafolha', 'Datafolha Instituto de Pesquisas LTDA', '07.630.546/0001-75', '', '(00) 00000-0000', 'São Paulo', 'SP', '1983')
""")

cursor.execute("""
INSERT OR REPLACE INTO pollsters (empresa, nome, cpf, email, telefone)
VALUES ('Datafolha', 'Mauro Paulino', '000.000.000-00', '', '(00) 00000-0000')
""")


cursor.execute("""
INSERT OR FAIL INTO popularidade (id, data_ini, data_fim, empresa, nome, positiva, regular, negativa, nsnr, erro, ic, amostra, ufs, cidades, partido, presidente, tipo, modo, pergunta)
VALUES ((SELECT IFNULL(MAX(id), 0) + 1 FROM popularidade), '2021-06-05', '2021-06-06', 'IDEIA Big Data', 'EXAME/IDEIA', 26, 23, 49, 2, 3, 95, 1252, 27, Null ,'(Sem partido)', 'Jair Bolsonaro', 'Avaliação do governo federal', 'CATI', 'Como você avalia o governo de Jair Bolsonaro até o momento?')
""")



# gravando no bd
conn.commit()

print('Dados inseridos com sucesso.')

conn.close()
