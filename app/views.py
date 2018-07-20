# -*- coding: utf-8 -*-

from flask import render_template

from app import app

@app.route('/')

def index ():
	return render_template('base.html')

@app.route('/filme')

def filme():
	lista=['star wars', 'de volta para o futuro', 'senhor dos aneis']
	return render_template('filme/index.html', filmes = lista)
