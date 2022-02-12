# 02_create_schema.py
import sqlite3

# conectando...
conn = sqlite3.connect('pollingpoints.db')
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
    FOREIGN KEY(nome) REFERENCES eleitoral(empresa),
    FOREIGN KEY(nome) REFERENCES popularidade(empresa),
	/* CONSTRAINT pk_empresa PRIMARY KEY(cnpj, razao_social), */
	-- nome da empresa nao deve ser NULL e ter valores combinaveis em aprovacao/empresa.
    /* CONSTRAINT fk_empresa FOREIGN KEY(nome) REFERENCES aprovacao(empresa), */
	/* CONSTRAINT fk2_empresa FOREIGN KEY(nome) REFERENCES intencao(empresa), */
	/* CHECK (email LIKE '%_@_%_.__%'), */
	CHECK (cnpj LIKE '__.___.___/____-__')
);
""")

print('Tabela empresas criada com sucesso.')
# desconectando...
conn.close()




# conectando...
conn = sqlite3.connect('pollingpoints.db')
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
	FOREIGN KEY(empresa) REFERENCES eleitoral(empresa),
	FOREIGN KEY(nome) REFERENCES popularidade(empresa),
	/* CONSTRAINT pk_pollster PRIMARY KEY(cpf), */ 
    /* CONSTRAINT fk_pollster FOREIGN KEY(empresa) REFERENCES empresas(nome), */ 
	CHECK (cpf LIKE '___.___.___-__')
);
""")

print('Tabela pollsters criada com sucesso.')
# desconectando...
conn.close()




# conectando...
conn = sqlite3.connect('pollingpoints.db')
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
    FOREIGN KEY(empresa) REFERENCES eleitoral(empresa),
	FOREIGN KEY(empresa) REFERENCES popularidade(empresa),
    /* CONSTRAINT fk_ranking FOREIGN KEY(empresa) REFERENCES empresas(nome),  */ 
	/* CONSTRAINT fk2_ranking FOREIGN KEY(empresa) REFERENCES aprovacao(empresa), */ 
	/* CONSTRAINT fk3_ranking FOREIGN KEY(empresa) REFERENCES intencao(empresa), */ 
	CHECK (ano LIKE '____')
);
""")

print('Tabela ranking criada com sucesso.')
# desconectando...
conn.close()



# conectando...
conn = sqlite3.connect('pollingpoints.db')
# definindo um cursor
cursor = conn.cursor()

# criando a tabela (schema)
cursor.execute("""
CREATE TABLE popularidade (
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
	stratum TEXT NOT NULL,
	partido TEXT NOT NULL,
    presidente TEXT NOT NULL,
	tipo TEXT NOT NULL,
    modo TEXT NOT NULL,
	pergunta TEXT,
	timestamp DATETIME NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
	CONSTRAINT pk_aprovacao PRIMARY KEY(data_fim, empresa, nome, stratum, presidente, tipo, modo),
	FOREIGN KEY(empresa) REFERENCES empresas(empresa),
	FOREIGN KEY(empresa) REFERENCES ranking(empresa),
    /* CONSTRAINT fk_aprovacao FOREIGN KEY(empresa) REFERENCES empresas(nome), */ 
	/* CONSTRAINT fk2_aprovacao FOREIGN KEY(empresa) REFERENCES ranking(empresa), */ 
	CHECK (data_ini LIKE '____-__-__'),
	CHECK (data_fim LIKE '____-__-__')
);
""")


print('Tabela popularidade criada com sucesso.')
# desconectando...
conn.close()




# conectando...
conn = sqlite3.connect('pollingpoints.db')
# definindo um cursor
cursor = conn.cursor()


# criando a tabela (schema)
cursor.execute("""
CREATE TABLE eleitoral (
	id INTEGER UNIQUE,
	data_ini DATE NOT NULL,
	data_fim DATE NOT NULL,
	empresa TEXT NOT NULL,
	nome TEXT NOT NULL,
	cargo TEXT NOT NULL,
	turno INTEGER NOT NULL,
	partido TEXT,
	candidato TEXT NOT NULL,
	voto NUMERIC(2,1) NOT NULL,
	erro NUMERIC(2,1),
	ic NUMERIC(2,1),
	amostra INTEGER,
	ufs TEXT,
	cidades TEXT,
	stratum TEXT NOT NULL,
	tipo TEXT NOT NULL,
	modo TEXT NOT NULL,
	cenario TEXT NOT NULL,
	pergunta TEXT,
	timestamp DATETIME NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
	CONSTRAINT pk_intencao PRIMARY KEY(data_fim, empresa, nome, cargo, turno, stratum, candidato, tipo, modo, cenario),
	FOREIGN KEY(empresa) REFERENCES empresas(empresa),
	FOREIGN KEY(empresa) REFERENCES ranking(empresa),
    /* CONSTRAINT fk_intencao FOREIGN KEY(empresa) REFERENCES empresas(nome), */ 
	/* CONSTRAINT fk2_intencao FOREIGN KEY(empresa) REFERENCES ranking(empresa), */ 
	CHECK (data_ini LIKE '____-__-__'),
	CHECK (data_fim LIKE '____-__-__')
);
""")

print('Tabela eleitoral criada com sucesso.')
# desconectando...
conn.close()



# conectando...
conn = sqlite3.connect('pollingpoints.db')
# definindo um cursor
cursor = conn.cursor()


# criando a tabela (schema)
cursor.execute("""
CREATE TABLE fundamentos (
	id INTEGER UNIQUE,
	periodo DATE NOT NULL,
	stratum TEXT NOT NULL,
    fonte TEXT NOT NULL,
	serie TEXT NOT NULL,
	indice TEXT NOT NULL,
	valor NUMERIC(2,4),
	timestamp DATETIME NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
	CONSTRAINT pk_intencao PRIMARY KEY(periodo, stratum, fonte, indice),
	CHECK (periodo LIKE '____-__')
);
""")

print('Tabela eleitoral criada com sucesso.')
# desconectando...
conn.close()