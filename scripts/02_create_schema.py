# 02_create_schema.py
import sqlite3

# conectando...
conn = sqlite3.connect('pollingpoint.db')
# definindo um cursor
cursor = conn.cursor()

# criando a tabela (schema)
cursor.execute("""
CREATE TABLE empresas (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	nome TEXT NOT NULL,
	razao_social TEXT NOT NULL,
	cnpj VARCHAR(18) NOT NULL,
	email TEXT,
	telefone TEXT,
	cidade TEXT,
	uf VARCHAR(2) NOT NULL,
	fundacao YEAR NOT NULL,
	timestamp DATETIME NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
	/* CONSTRAINT pk_empresa PRIMARY KEY(cnpj, nome), */
	-- nome da empresa nao deve ser NULL e ter valores combinaveis em aprovacao/empresa.
    CONSTRAINT fk_empresa FOREIGN KEY(nome) REFERENCES aprovacao(empresa),
	CONSTRAINT fk2_empresa FOREIGN KEY(nome) REFERENCES intencao(empresa),
	/* CHECK (email LIKE '%_@_%_.__%'), */
	CHECK (cnpj LIKE '__.___.___/____-__')
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
CREATE TABLE pollsters (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	empresa TEXT NOT NULL,
	nome TEXT NOT NULL,
	cpf VARCHAR(16) UNIQUE NOT NULL,
	email TEXT,
	telefone TEXT,
	timestamp DATETIME NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
	/* CONSTRAINT pk_pollster PRIMARY KEY(cpf), */ 
    CONSTRAINT fk_pollster FOREIGN KEY(empresa) REFERENCES empresas(nome),
	CHECK (cpf LIKE '___.___.___-__')
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
CREATE TABLE ranking (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	empresa TEXT NOT NULL,
	score NUMERIC(2,2) NOT NULL,
	classe TEXT NOT NULL,
	eleicao TEXT NOT NULL,
	ano YEAR NOT NULL,
	timestamp DATETIME NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
    CONSTRAINT fk_ranking FOREIGN KEY(empresa) REFERENCES empresas(nome),
	CONSTRAINT fk2_ranking FOREIGN KEY(empresa) REFERENCES aprovacao(empresa),
	CONSTRAINT fk3_ranking FOREIGN KEY(empresa) REFERENCES intencao(empresa),
	CHECK (ano LIKE '____')
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
CREATE TABLE aprovacao (
	id INTEGER UNIQUE,
	data_ini DATE,
	data_fim DATE NOT NULL,
	empresa TEXT NOT NULL,
	nome TEXT NOT NULL,
	positiva NUMERIC(2,1) NOT NULL,
	regular NUMERIC(2,1),
	negativa NUMERIC(2,1) NOT NULL,
	nsnr NUMERIC(2,1),
	erro NUMERIC(2,1),
	ic INTEGER,
	amostra INTEGER,
	ufs TEXT,
	cidades TEXT,
	partido TEXT NOT NULL,
    presidente TEXT NOT NULL,
	tipo TEXT NOT NULL,
	pergunta TEXT,
	modo TEXT NOT NULL,
	timestamp DATETIME NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
	CONSTRAINT pk_aprovacao PRIMARY KEY(data_fim, empresa, nome, tipo),
    CONSTRAINT fk_aprovacao FOREIGN KEY(empresa) REFERENCES empresas(nome),
	CONSTRAINT fk2_aprovacao FOREIGN KEY(empresa) REFERENCES ranking(empresa),
	CHECK (data_ini LIKE '____-__-__'),
	CHECK (data_fim LIKE '____-__-__')
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
CREATE TABLE intencao (
	id INTEGER UNIQUE,
	data_ini DATE,
	data_fim DATE NOT NULL,
	empresa TEXT NOT NULL,
	nome TEXT NOT NULL,
	cargo TEXT NOT NULL,
	turno INTEGER NOT NULL,
	candidato TEXT NOT NULL,
	partido TEXT NOT NULL,
	voto NUMERIC(2,1) NOT NULL,
	erro NUMERIC(2,1),
	ic NUMERIC(2,1),
	amostra INTEGER,
	ufs TEXT,
	cidades TEXT,
	tipo TEXT NOT NULL,
	modo TEXT NOT NULL,
	pergunta TEXT,
	timestamp DATETIME NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
	CONSTRAINT pk_intencao PRIMARY KEY(data_fim, empresa, nome, cargo, turno, candidato, tipo),
    CONSTRAINT fk_intencao FOREIGN KEY(empresa) REFERENCES empresas(nome),
	CONSTRAINT fk2_intencao FOREIGN KEY(empresa) REFERENCES ranking(empresa),
	CHECK (data_ini LIKE '____-__-__'),
	CHECK (data_fim LIKE '____-__-__')
);
""")

print('Tabela criada com sucesso.')
# desconectando...
conn.close()
