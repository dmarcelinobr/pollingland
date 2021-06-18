#!python3
# manager_db.py
# -*- coding: utf-8 -*-
"""
    Este App gerencia um banco de dados sqlite3.
    Pode-se usar o modo interativo com python ou python3 ou ipython ou ipython3.
    
    Banco de dados: 'pollingpoint.db'
    Schema: 'pollingpoint_schema.sql'
    Tabelas: 'aprovacao' e 'intencao'
"""

import os
import sqlite3
import io
import datetime
import csv

class Connect(object):

    ''' A classe Connect representa o banco de dados. '''

    def __init__(self, db_name):
        try:
            # conectando...
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
            # imprimindo nome do banco
            print("Banco:", db_name)
            # lendo a versão do SQLite
            self.cursor.execute('SELECT SQLITE_VERSION()')
            self.data = self.cursor.fetchone()
            # imprimindo a versão do SQLite
            print("SQLite version: %s" % self.data)
        except sqlite3.Error:
            print("Erro ao abrir banco.")
            return False

    def commit_db(self):
        if self.conn:
            self.conn.commit()

    def close_db(self):
        if self.conn:
            self.conn.close()
            print("Conexão fechada.")



# Class for manipulating intencao de votos
class IntencaoDb(object):
    
    tb_name = 'intencao'

    ''' A classe IntencaoDb representa funções para manipular dados de pesquisas de intenção de votos no banco de dados. '''

    def __init__(self):
        self.db = Connect('pollingpoint.db')
        self.tb_name
        
    # create_schema
    def criar_schema(self, schema_name='sql/intencao_schema.sql'):
        print("Criando tabela %s ..." % self.tb_name)

        try:
            with open(schema_name, 'rt') as f:
                schema = f.read()
                self.db.cursor.executescript(schema)
        except sqlite3.Error:
            print("Aviso: A tabela %s já existe." % self.tb_name)
            return False

        print("Tabela %s criada com sucesso." % self.tb_name)



    ''' CREATE '''

    # insert_one_register
    def inserir_um_registro(self):
        try:
            self.db.cursor.execute("""
                INSERT OR FAIL INTO intencao (id, data_ini, data_fim, empresa, nome, cargo, turno, partido, candidato, voto, erro, ic, amostra, ufs, cidades, tipo, modo, pergunta)
                VALUES ((SELECT IFNULL(MAX(id), 0) + 1 FROM intencao), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """)
            # gravando no bd
            self.db.commit_db()
            print("Um registro inserido com sucesso.")
        except sqlite3.IntegrityError:
            print("Aviso: A pesquisa deve ser única!")
            return False
            
    
    
    def inserir_um_df(self, df_name):
        try:
            df = df_name
            for i, row in df.iterrows():
                self.db.cursor.execute("""
                INSERT OR FAIL INTO intencao (id, data_ini, data_fim, empresa, nome, cargo, turno, partido, candidato, voto, erro, ic, amostra, ufs, cidades, tipo, modo, pergunta)
                VALUES ((SELECT IFNULL(MAX(id), 0) + 1 FROM intencao), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, row)
            # gravando no bd
            self.db.commit_db()
            print("Dados importados do DataFrame com sucesso.")
        except sqlite3.IntegrityError:
            print("Aviso: A pesquisa deve ser única!")
            return False


    # insert_with_list
    def inserir_de_lista(self, lista=None):
        # criando uma lista de dados
        try:
            self.db.cursor.executemany("""
                INSERT OR FAIL INTO intencao (id, data_ini, data_fim, empresa, nome, cargo, turno, partido, candidato, voto, erro, ic, amostra, ufs, cidades, tipo, modo, pergunta)
                VALUES ((SELECT IFNULL(MAX(id), 0) + 1 FROM intencao), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, lista)
            # gravando no bd
            self.db.commit_db()
            print("Dados inseridos da lista com sucesso: %s registros." %
                  len(lista))
        except sqlite3.IntegrityError:
            print("Aviso: A pesquisa deve ser única!")
            return False



    ''' READ '''

    # read_pesquisas
    def ler_todas_pesquisas(self):
        sql = 'SELECT * FROM intencao ORDER BY data_fim'
        r = self.db.cursor.execute(sql)
        return r.fetchall()



    # print_all_pesquisas
    def imprimir_todas_pesquisas(self):
        lista = self.ler_todas_pesquisas()
        print('{} {} {} {} {} {} {} {} {}'.format('id', 'data_fim', 'nome', 'cargo', 'turno', 'candidato', 'voto', 'amostra', 'tipo'))
        for c in lista:
            print('{} {} {} {} {} {} {} {} {}'.format(
                c[0], c[1], c[2],
                c[3], c[4], c[5],
                c[6], c[7], c[8]))
                

    # find_pesquisa
    def localizar_pesquisa(self, nome='Datafolha'):
        r = self.db.cursor.execute(
            'SELECT * FROM intencao WHERE nome = ?', (nome,))
        return r.fetchone()


    # print_pesquisa
    def imprimir_pesquisa(self, nome):
        if self.localizar_pesquisa(nome) == None:
            print('Não existe pesquisa com o nome informado.')
        else:
            print(self.localizar_pesquisa(nome))


    # count_pesquisas
    def contar_pesquisas(self):
        r = self.db.cursor.execute(
            'SELECT COUNT(*) FROM intencao')
        print("Total de pesquisas registradas:", r.fetchone()[0])


    # count_pesquisas_por_empresa
    def contar_pesquisas_por_empresa(self, empresa="Poder360"):
        r = self.db.cursor.execute(
            'SELECT COUNT(*) FROM intencao WHERE empresa = ?', (empresa,))
        print("Total de pesquisas da empresa", empresa, ":", r.fetchone()[0])


    # find_pesquisa_por_data
    def localizar_pesquisa_por_data(self, data='2021-01-01'):
        resultado = self.db.cursor.execute(
            'SELECT * FROM intencao WHERE data_fim > ?', (data,))
        print("Pesquisas realizadas depois de", data, ":")
        for pesquisa in resultado.fetchall():
            print(pesquisa)


    # find_pesquisa_por_turno
    def localizar_pesquisa_por_turno(self, turno='2'):
        resultado = self.db.cursor.execute(
            'SELECT * FROM intencao WHERE turno = ?', (turno,))
        print("Pesquisas sobre o", turno, "turno:")
        for pesquisa in resultado.fetchall():
            print(pesquisa)


    # find_pesquisa_por_candidato
    def localizar_pesquisa_por_candidato(self, candidato='Lula'):
        resultado = self.db.cursor.execute(
        'SELECT * FROM intencao WHERE candidato = ?', (candidato,))
        print("Pesquisa com o candidato", candidato, ":")
        for pesquisa in resultado.fetchall():
            print(pesquisa)

    # tabela_select
    def tabela_select(self, sql="SELECT * FROM intencao;"):
        r = self.db.cursor.execute(sql)
        # gravando no bd
        self.db.commit_db()
        for intencao in r.fetchall():
            print(intencao)

    # myselect
    def meu_select(self, sql="SELECT AVG(voto) FROM intencao WHERE presidente='Jair Bolsonaro';"):
        r = self.db.cursor.execute(sql)
        # gravando no bd
        self.db.commit_db()
        for intencao in r.fetchall():
            print(intencao)



    ''' UPDATE '''

    # update_data
    def atualizar(self, id):
        try:
            c = self.localizar_pesquisa(id)
            if c:
                self.nova_data_ini = input('data_ini: ')
                self.db.cursor.execute("""
                UPDATE intencao
                SET data_ini = ?
                WHERE id = ?
                """, (self.nova_data_ini, id,))
                # gravando no bd
                self.db.commit_db()
                print("Dados atualizados com sucesso.")
            else:
                print('Não existe pesquisa com o id informado.')
        except e:
            raise e


    ''' DELETE '''


    # delete_data
    def excluir(self, id):
        try:
            c = self.localizar_pesquisa(id)
            # verificando se existe pesquisa com o ID passado, caso exista
            if c:
                self.db.cursor.execute("""
                DELETE FROM intencao WHERE id = ?
                """, (id,))
                # gravando no bd
                self.db.commit_db()
                print("Registro %d excluído com sucesso." % id)
            else:
                print('Não existe pesquisa com o id informado.')
        except e:
            raise e



    ''' Lendo informações do banco de dados '''

    def table_info(self):
        # obtendo informações da tabela
        t = self.db.cursor.execute(
            'PRAGMA table_info({})'.format(self.tb_name))
        colunas = [tupla[1] for tupla in t.fetchall()]
        print('Colunas:', colunas)

    def table_list(self):
        # listando as tabelas do bd
        l = self.db.cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' ORDER BY name
        """)
        print('Tabelas:')
        for tabela in l.fetchall():
            print("%s" % (tabela))

    def table_schema(self):
        # obtendo o schema da tabela
        s = self.db.cursor.execute("""
        SELECT sql FROM sqlite_master WHERE type='table' AND name=?
        """, (self.tb_name,))

        print('Schema:')
        for schema in s.fetchall():
            print("%s" % (schema))



    ''' Fazendo backup do banco de dados (exportando dados) '''

    def backup(self, file_name='sql/pollingpoint_bkp.sql'):
        with io.open(file_name, 'w') as f:
            for linha in self.db.conn.iterdump():
                f.write('%s\n' % linha)

        print('Backup realizado com sucesso.')
        print('Salvo como %s' % file_name)

    ''' Recuperando o banco de dados (importando dados) '''


    # import_data
    def importar_dados(self, db_name='pollingpoint_recovery.db', file_name='sql/pollingpoint_bkp.sql'):
        try:
            self.db = Connect(db_name)
            f = io.open(file_name, 'r')
            sql = f.read()
            self.db.cursor.executescript(sql)
            print('Banco de dados recuperado com sucesso.')
            print('Salvo como %s' % db_name)
        except sqlite3.OperationalError:
            print(
                "Aviso: O banco de dados %s já existe. Exclua-o e faça novamente." %
                db_name)
            return False


       # close_connection
    def fechar_conexao(self):
        self.db.close_db()






class AprovacaoDb(object):

    ''' A classe AprovacaoDb representa funções para manipular dados de pesquisas de popularidade no banco de dados. '''
    
    tb_name = 'aprovacao'

    def __init__(self):
        self.db = Connect('pollingpoint.db')
        self.tb_name


    # create_schema
    def criar_schema(self, schema_name='sql/aprovacao_schema.sql'):
        print("Criando tabela %s ..." % self.tb_name)

        try:
            with open(schema_name, 'rt') as f:
                schema = f.read()
                self.db.cursor.executescript(schema)
        except sqlite3.Error:
            print("Aviso: A tabela %s já existe." % self.tb_name)
            return False

        print("Tabela %s criada com sucesso." % self.tb_name)



    ''' CREATE '''

    # insert_one_register
    def inserir_um_registro(self):
        try:
            self.db.cursor.execute("""
                INSERT OR FAIL INTO aprovacao (id, data_ini, data_fim, empresa, nome, positiva, regular, negativa, nsnr, erro, ic, amostra, ufs, cidades, partido, presidente, tipo, pergunta, modo)
                VALUES ((SELECT IFNULL(MAX(id), 0) + 1 FROM aprovacao), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """)
            # gravando no bd
            self.db.commit_db()
            print("Um registro inserido com sucesso.")
        except sqlite3.IntegrityError:
            print("Aviso: A pesquisa deve ser única!")
            return False
            
    
    
    def inserir_um_df(self, df_name):
        try:
            df = df_name
            for i, row in df.iterrows():
                self.db.cursor.execute("""
                INSERT OR FAIL INTO aprovacao (id, data_ini, data_fim, empresa, nome, positiva, regular, negativa, nsnr, erro, ic, amostra, ufs, cidades, partido, presidente, tipo, pergunta, modo)
                VALUES ((SELECT IFNULL(MAX(id), 0) + 1 FROM aprovacao), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, row)
            # gravando no bd
            self.db.commit_db()
            print("Dados importados do DataFrame com sucesso.")
        except sqlite3.IntegrityError:
            print("Aviso: A pesquisa deve ser única!")
            return False

    
    # insert_with_list
    def inserir_de_lista(self, lista=None):
        # criando uma lista de dados
        try:
            self.db.cursor.executemany("""
            INSERT OR FAIL INTO aprovacao (id, data_ini, data_fim, empresa, nome, positiva, regular, negativa, nsnr, erro, ic, amostra, ufs, cidades, partido, presidente, tipo, pergunta, modo)
            VALUES ((SELECT IFNULL(MAX(id), 0) + 1 FROM aprovacao), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, lista)
            # gravando no bd
            self.db.commit_db()
            print("Dados inseridos da lista com sucesso: %s registros." %
                  len(lista))
        except sqlite3.IntegrityError:
            print("Aviso: A pesquisa deve ser única!")
            return False


    ''' READ '''

    # read_pesquisas
    def ler_todas_pesquisas(self):
        sql = 'SELECT * FROM aprovacao ORDER BY data_fim'
        r = self.db.cursor.execute(sql)
        return r.fetchall()



    # print_all_pesquisas
    def imprimir_todas_pesquisas(self):
        lista = self.ler_todas_pesquisas()
        print('{} {} {} {} {} {} {} {} {}'.format('id', 'data_fim', 'nome', 'presidente', 'positiva', 'regular', 'negativa', 'amostra', 'tipo'))
        for c in lista:
            print('{} {} {} {} {} {} {} {} {}'.format(
                c[0], c[1], c[2],
                c[3], c[4], c[5],
                c[6], c[7], c[8]))
                

    # find_pesquisa
    def localizar_pesquisa(self, nome='Datafolha'):
        r = self.db.cursor.execute(
            'SELECT * FROM aprovacao WHERE nome = ?', (nome,))
        return r.fetchone()


    # print_pesquisa
    def imprimir_pesquisa(self, nome):
        if self.localizar_pesquisa(nome) == None:
            print('Não existe pesquisa com o nome informado.')
        else:
            print(self.localizar_pesquisa(nome))


    # count_pesquisas
    def contar_pesquisas(self):
        r = self.db.cursor.execute(
            'SELECT COUNT(*) FROM aprovacao')
        print("Total de pesquisas registradas:", r.fetchone()[0])


    # count_pesquisas_por_empresa
    def contar_pesquisas_por_empresa(self, empresa="Poder360"):
        r = self.db.cursor.execute(
            'SELECT COUNT(*) FROM aprovacao WHERE empresa = ?', (empresa,))
        print("Total de pesquisas da empresa", empresa, ":", r.fetchone()[0])


    # find_pesquisa_por_data
    def localizar_pesquisa_por_data(self, data='2021-01-01'):
        resultado = self.db.cursor.execute(
            'SELECT * FROM aprovacao WHERE data_fim > ?', (data,))
        print("Pesquisas realizadas depois de", data, ":")
        for pesquisa in resultado.fetchall():
            print(pesquisa)


    # find_pesquisa_por_presidente
    def localizar_pesquisa_por_presidente(self, presidente='Lula'):
        resultado = self.db.cursor.execute(
        'SELECT * FROM aprovacao WHERE presidente = ?', (presidente,))
        print("Pesquisa com o presidente", presidente, ":")
        for pesquisa in resultado.fetchall():
            print(pesquisa)

    # myselect
    def tabela_select(self, sql="SELECT * FROM aprovacao;"):
        r = self.db.cursor.execute(sql)
        # gravando no bd
        self.db.commit_db()
        for aprovacao in r.fetchall():
            print(aprovacao)

    # myselect
    def meu_select(self, sql="SELECT AVG(positiva) FROM aprovacao WHERE presidente='Jair Bolsonaro';"):
        r = self.db.cursor.execute(sql)
        # gravando no bd
        self.db.commit_db()
        for aprovacao in r.fetchall():
            print(aprovacao)


    ''' UPDATE '''

    # update_data
    def atualizar(self, id):
        try:
            c = self.localizar_pesquisa(id)
            if c:
                self.nova_data_ini = input('data_ini: ')
                self.db.cursor.execute("""
                UPDATE aprovacao
                SET data_ini = ?
                WHERE id = ?
                """, (self.nova_data_ini, id,))
                # gravando no bd
                self.db.commit_db()
                print("Dados atualizados com sucesso.")
            else:
                print('Não existe pesquisa com o id informado.')
        except e:
            raise e


    ''' DELETE '''

    # delete_data
    def excluir(self, id):
        try:
            c = self.localizar_pesquisa(id)
            # verificando se existe pesquisa com o ID passado, caso exista
            if c:
                self.db.cursor.execute("""
                DELETE FROM aprovacao WHERE id = ?
                """, (id,))
                # gravando no bd
                self.db.commit_db()
                print("Registro %d excluído com sucesso." % id)
            else:
                print('Não existe pesquisa com o id informado.')
        except e:
            raise e



    ''' Lendo informações do banco de dados '''

    def table_info(self):
        # obtendo informações da tabela
        t = self.db.cursor.execute(
            'PRAGMA table_info({})'.format(self.tb_name))
        colunas = [tupla[1] for tupla in t.fetchall()]
        print('Colunas:', colunas)

    def table_list(self):
        # listando as tabelas do bd
        l = self.db.cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' ORDER BY name
        """)
        print('Tabelas:')
        for tabela in l.fetchall():
            print("%s" % (tabela))

    def table_schema(self):
        # obtendo o schema da tabela
        s = self.db.cursor.execute("""
        SELECT sql FROM sqlite_master WHERE type='table' AND name=?
        """, (self.tb_name,))

        print('Schema:')
        for schema in s.fetchall():
            print("%s" % (schema))



    ''' Fazendo backup do banco de dados (exportando dados) '''

    def backup(self, file_name='sql/pollingpoint_bkp.sql'):
        with io.open(file_name, 'w') as f:
            for linha in self.db.conn.iterdump():
                f.write('%s\n' % linha)

        print('Backup realizado com sucesso.')
        print('Salvo como %s' % file_name)

    ''' Recuperando o banco de dados (importando dados) '''


    # import_data
    def importar_dados(self, db_name='pollingpoint_recovery.db', file_name='sql/pollingpoint_bkp.sql'):
        try:
            self.db = Connect(db_name)
            f = io.open(file_name, 'r')
            sql = f.read()
            self.db.cursor.executescript(sql)
            print('Banco de dados recuperado com sucesso.')
            print('Salvo como %s' % db_name)
        except sqlite3.OperationalError:
            print(
                "Aviso: O banco de dados %s já existe. Exclua-o e faça novamente." %
                db_name)
            return False

       # close_connection
    def fechar_conexao(self):
        self.db.close_db()