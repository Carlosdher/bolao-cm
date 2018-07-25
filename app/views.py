# -*- coding: utf-8 -*-
import psycopg2, psycopg2.extras

from flask import g, session, request, redirect, url_for, render_template

from app import app

@app.before_request
def before_request():
   g.db = psycopg2.connect("dbname=bolao user=postgres password=sousa123 host=127.0.0.1")

# Disconnect database
@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/')
def index():
	cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute("SELECT * FROM bolao")
	boloes = cur.fetchall()
	if 'name' in session:
		cur.execute("SELECT * FROM usuario WHERE email = '{}'".format(session['name']))
		usuario = cur.fetchall()
		return render_template('index.html', usuario = usuario, boloes = boloes)
	else:
		return render_template('index.html', boloes = boloes)

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	else:
		email=request.form['e-mail']
		senha=request.form['senha']
		cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cur.execute("SELECT * FROM Usuario") 
		usuarios = cur.fetchall()
		for usuario in usuarios:
			if usuario[1] == email and usuario[2] == senha: 
				session['name'] = usuario[1]
				print (session['name'])
				return redirect(url_for('index'))
			else:
				pass 		
		return render_template('login.html', error='Usuário não cadastrado')

@app.route('/cadastro', methods = ['GET', 'POST'])
def cadastro():
	if request.method == 'GET':
		return render_template('cadastro.html')
	else:
		nome = request.form['nome']
		email = request.form['e-mail']
		senha = request.form['senha']
		cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cur.execute("INSERT INTO usuario (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha))
		g.db.commit()
		return redirect(url_for('login'))

@app.route('/sair')
def sair():
	session.pop('name')
	return redirect(url_for('index'))

@app.route('/perfil')
def perfil():
	if 'name' in session:
		cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cur.execute("SELECT * FROM usuario WHERE email = '{}'".format(session['name']))
		usuario = cur.fetchall()
		cur.execute("SELECT * FROM bolao WHERE email_usuario = '{}'".format(session['name']))
		boloes = cur.fetchall()
		cur.execute("SELECT * FROM bolao")
		boloes = cur.fetchall()
		meus_boloes = []
		for x in boloes:
			print (x[11])
			if x[11] != None:
				if session['name'] in x[11]:
					meus_boloes.append(x)
		print(meus_boloes)
		return render_template('perfil.html', usuario = usuario, boloes = boloes, meus_boloes = meus_boloes)
	else:
		return redirect(url_for('login'))

@app.route('/criar-bolao', methods = ['GET', 'POST'])
def criar_bolao():
	if request.method == 'POST':
		nome = request.form['nome']
		time1 = request.form['time1']
		time2 = request.form['time2']
		valor = request.form['valor']
		datainicio = request.form['datainicio']
		datafim = request.form['datafim']
		descricao = request.form['descricao']
		cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
		query = ("INSERT INTO bolao (time1, time2, email_usuario, data_inicio, data_fim, nome, descricao, valor_minimo) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', {})".format(time1, time2, session['name'], datainicio, datafim, nome, descricao, valor))
		cur.execute(query)
		g.db.commit()
		return redirect(url_for('perfil'))
	return render_template('criarbolao.html')

@app.route('/participar/<int:id_bolao>/<int:tipo>')
def participar(id_bolao, tipo):
	if 'name' in session:
		cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cur.execute("SELECT * FROM bolao WHERE id_bolao = {}".format(id_bolao))
		boloes = cur.fetchall()
		lista = boloes[0][11]
		if tipo == 1:
			if lista == None:
				lista = []
				lista.append(session['name'])
			else:
				lista.append(session['name'])
		else:
			if lista == None:
				lista = []
				part=str('anonimo')
				lista.append(part)
			else:
				lista.append(session['name'])
		cur.execute("UPDATE bolao SET participantes = array{}".format(lista))
		g.db.commit()
		return redirect(url_for('perfil'))
	return redirect(url_for('login'))

@app.route('/lista-participantes/<int:id_bolao>')
def listar(id_bolao):
	cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute("SELECT * FROM bolao WHERE id_bolao = {}".format(id_bolao))
	bolao = cur.fetchone()
	return render_template('listar.html', bolao = bolao)
