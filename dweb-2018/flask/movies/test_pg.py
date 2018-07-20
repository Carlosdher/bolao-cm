# -*- coding: utf-8 -*-

# Importar biblioteca psycopg2
import psycopg2
import psycopg2.extras

# Criar uma conexão com o banco de dados
try:
    conn = psycopg2.connect('dbname=movies user=guga password=gugasv2 host=127.0.0.1')

    # Criar um cursor para manipular o banco de dados
    # cur = conn.cursor()

    # INSERT: Executar as queries do banco de dados
    # cur.execute("INSERT INTO ator (nome, data_nasc, bio) VALUES ('Tim Allen', '1953-06-13', 'Timothy Alan Dick[1] (born June 13, 1953), known professionally as Tim Allen, is an American actor and comedian.')")
    # conn.commit()

    # Result as dict
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # SELECT
    cur.execute("SELECT * FROM ator")

    # Fetch all
    # print( cur.fetchall() )
    atores = cur.fetchall()
    print('%s Atores no banco de dados' % (len(atores)))
    print('------------------')
    for ator in atores:
        print( 'Nome: %s' % ator['nome'] )
        print( 'Bio: %s' % ator['bio'] )
        print('------------------')

    # # Fetch one
    # cur.execute("SELECT * FROM ator LIMIT 1")
    # ator = cur.fetchone()
    # while ator:
    #     print('------------------')
    #     print(ator)
    #     ator = cur.fetchone()

    # Fechar a conexão com o banco
    conn.close()
except psycopg2.OperationalError as connError:
    print('Não foi possível se conectar ao banco de dados. Verifique os dados de conexão.')
