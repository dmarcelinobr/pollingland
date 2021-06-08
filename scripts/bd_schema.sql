CREATE TABLE empresas (
	nome TEXT NOT NULL,
	razao_social TEXT NOT NULL,
	cnpj VARCHAR(18) NOT NULL,
	id_responsavel VARCHAR(16) NOT NULL,
	email TEXT,
	fone TEXT,
	cidade TEXT,
	uf VARCHAR(2) NOT NULL,
	criada_em YEAR NOT NULL,
	CONSTRAINT pk_empresa PRIMARY KEY(cnpj),
    CONSTRAINT fk_empresa FOREIGN KEY(nome) REFERENCES aprovacao(empresa),
	CONSTRAINT fk2_empresa FOREIGN KEY(nome) REFERENCES intencao(empresa),
	/* CONSTRAINT fk3_empresa FOREIGN KEY(id_responsavel) REFERENCES pollsters(cpf),*/
	/* CHECK (email LIKE '%_@_%_.__%'),*/
	CHECK (cnpj LIKE '__.___.___/____-__'),
	CHECK (id_responsavel LIKE '___.___.___-__')
);


CREATE TABLE pollsters (
	nome TEXT NOT NULL,
	cpf VARCHAR(16) NOT NULL,
	email TEXT,
	fone TEXT,
	CONSTRAINT pk_pollster PRIMARY KEY(cpf),
    CONSTRAINT fk_pollster FOREIGN KEY(cpf) REFERENCES empresas(id_responsavel),
	CHECK (cpf LIKE '___.___.___-__')
);


CREATE TABLE aprovacao (
	data_ini DATE NOT NULL,
	data_fim DATE NOT NULL,
	empresa TEXT NOT NULL,
	nome TEXT NOT NULL,
	positiva FLOAT NOT NULL,
	regular FLOAT,
	negativa FLOAT NOT NULL,
	nsnr FLOAT,
	erro FLOAT NOT NULL,
	ic INTEGER NOT NULL,
	n INTEGER NOT NULL,
	ufs TEXT,
	cidades TEXT,
	partido TEXT NOT NULL,
    presidente TEXT NOT NULL,
	tipo TEXT NOT NULL,
	pergunta TEXT,
	modo TEXT NOT NULL,
	CONSTRAINT pk_aprovacao PRIMARY KEY(data_fim, nome),
    CONSTRAINT fk_aprovacao FOREIGN KEY(empresa) REFERENCES empresas(nome),
	CHECK (data_fim LIKE '____-__-__')
);



CREATE TABLE intencao (
	data_ini DATE NOT NULL,
	data_fim DATE NOT NULL,
	empresa TEXT NOT NULL,
	nome TEXT NOT NULL,
	cargo TEXT NOT NULL,
	turno INTEGER NOT NULL,
	candidato TEXT NOT NULL,
	partido TEXT NOT NULL,
	voto FLOAT NOT NULL,
	erro FLOAT NOT NULL,
	ic FLOAT NOT NULL,
	n INTEGER NOT NULL,
	ufs TEXT,
	cidades TEXT,
	tipo TEXT NOT NULL,
	modo TEXT NOT NULL,
	pergunta TEXT,
	CONSTRAINT pk_intencao PRIMARY KEY(data_fim, nome, cargo, turno, candidato, tipo),
    CONSTRAINT fk_intencao FOREIGN KEY(empresa) REFERENCES empresas(nome),
	CHECK (data_fim LIKE '____-__-__')
);
