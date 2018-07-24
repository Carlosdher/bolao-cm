# -*- coding: utf-8 -*-
import psycopg2, psycopg2.extras

from flask import g, session, request, redirect, url_for, render_template

from app import app

@app.before_request
def before_request():
   g.db = psycopg2.connect("dbname=bolao user=postgres password=maria123")

# Disconnect database
@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/')
def index():
		if 'name' in session:
			return render_template('index.html', usuario = session['name'])
		else:
			return render_template('index.html')

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
			if usuario [1] == email and usuario[2] == senha:
				session['name'] = usuario[0] 
				session['e-mail'] = usuario[1]
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
	cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute("SELECT * FROM usuario WHERE email = '{}'".format(session['email']))
	usuario = cur.fetchall()
	return render_template('perfil.html', usuario = usuario)

@app.route('/criar-bolao', methods = ['GET', 'POST'])
def criar_bolao():
	if request.method == 'POST':
		nome = request.form['nome-do-bolao']
		time1 = request.form['time1']
		time2 = request.form['time2']
		valor = request.form['valor']
		datainicio = request.form['datainicio']
		datafim = request.form['datafim']
		descricao = request.form['descricao']
		cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cur.execute("INSERT INTO usuario (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha))
		g.db.commit()
				
	return render_template('criarbolao.html')