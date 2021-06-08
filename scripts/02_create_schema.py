# 02_create_schema.py
import sqlite3

# conectando...
conn = sqlite3.connect('pollingpoint.db')
# definindo um cursor
cursor = conn.cursor()

# criando a tabela (schema)
cursor.execute("""
CREATE TABLE empresas (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	nome TEXT NOT NULL,
	idade INTEGER,
	cnpj VARCHAR(13) NOT NULL,
	email TEXT,
	fone TEXT,
	cidade TEXT,
	uf VARCHAR(2) NOT NULL,
	criada_em DATE NOT NULL
	CONSTRAINT pk_empresa PRIMARY KEY(cnpj),
    CONSTRAINT fk_empresa FOREIGN KEY(nome) REFERENCES pesquisas(nome),
	# CONSTRAINT fk2_empresa FOREIGN KEY(idResponsavel) REFERENCES pollsters(CPF),
	# CHECK (email LIKE '%_@_%_.__%'),
	CHECK (CNPJ LIKE '__.___.___/____-__')
);
""")

print('Tabela criada com sucesso.')
# desconectando...
conn.close()




# conectando...
conn = sqlite3.connect('pollingpoint.db')
# definindo um cursor
cursor = conn.cursor()

# criando a tabela (schema)
cursor.execute("""
CREATE TABLE empresas (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	nome TEXT NOT NULL,
	idade INTEGER,
	cnpj VARCHAR(13) NOT NULL,
	email TEXT,
	fone TEXT,
	cidade TEXT,
	uf VARCHAR(2) NOT NULL,
	criada_em DATE NOT NULL
	CONSTRAINT pk_empresa PRIMARY KEY(cnpj),
    CONSTRAINT fk_empresa FOREIGN KEY(nome) REFERENCES pesquisas(nome),
	# CONSTRAINT fk2_empresa FOREIGN KEY(idResponsavel) REFERENCES pollsters(CPF),
	# CHECK (email LIKE '%_@_%_.__%'),
	CHECK (CNPJ LIKE '__.___.___/____-__')
);
""")

print('Tabela criada com sucesso.')
# desconectando...
conn.close()