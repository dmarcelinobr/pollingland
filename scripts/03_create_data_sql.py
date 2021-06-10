# 03_create_data_sql.py
import sqlite3

conn = sqlite3.connect('pollingpoint.db')
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
INSERT OR REPLACE INTO aprovacao (data_ini, data_fim, empresa, nome, positiva, regular, negativa, nsnr, erro, ic, amostra, ufs, cidades, partido, presidente, tipo, pergunta, modo)
VALUES ('1986-03-11', '1986-03-15', 'Datafolha', 'Datafolha', 71, 25, 2, 3, 3, 95, 1000, '10','10','PMDB', 'José Sarney', 'Avaliação do governo federal','Na sua opinião o presidente José Sarney está sendo ótimo, bom, regular, ruim ou péssimo?', 'FF')
""")



# gravando no bd
conn.commit()

print('Dados inseridos com sucesso.')

conn.close()
