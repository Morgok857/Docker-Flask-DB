#/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request
#from flask_wtf import CSRFProtect
from flask_wtf.csrf import CSRFProtect
from flask import make_response
from flask import session
from flask import redirect
from flask import url_for
from flask import flash
from config import DevelopmentConfig
from models import db
from models import User, Comment
from helper import date_format
import forms
import json

app = Flask(__name__)
# Prevent CSRF
csrf = CSRFProtect()
app.config.from_object(DevelopmentConfig)


@app.before_request
def before_request():
	if 'username' not in session and request.endpoint in ['comment']:
		return redirect(url_for('login'))
	elif 'username' in session and request.endpoint in ['login','create']:
		return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error_handler):
	return	render_template('404.html'),404

@app.route('/')
def index():
	#custome_cookie = request.cookies.get('ct_ck', 'Undefined')
	#print(custome_cookie)
	if 'username' in session:
		username = session['username']
		print("Nos ve: " + username)
	else:
		#username = "Registrate Forro"
		username = None

	title = "Curso Flask, Super Seguro"
	return render_template('index.html', title=title, guest=username)


@app.route('/login', methods=['GET','POST'])
def login():
	login_form = forms.LoginForm(request.form)
	if request.method == 'POST' and login_form.validate():
		username = login_form.username.data
		password = login_form.password.data

		user = User.query.filter_by(username = username).first()
		if user is not None and user.verify_password(password):
			sussess_message = "Bienvenido {}".format(username)
			flash(sussess_message)
			session['username'] = username
			return redirect(url_for('index'))
		else:
			error_message = "Metiste el dedo mal!!"
			flash(error_message)
	return render_template('login.html', form= login_form)


@app.route('/cookie')
def cookie():
	response = make_response(render_template('cookie.html'))
	response.set_cookie('ct_ck','Entre, soy Juaker')
	return response
	#title = "NO tengo Galletas.."
	#return render_template('index.html', title=title)


@app.route('/comment', methods=['GET','POST'])
def comment():
	comment_form = forms.CommentForm(request.form)
	print(session['username'] + ' Comment')
	if request.method == 'POST' and comment_form.validate():
		full_user = User.query.filter_by(username = session['username']).first()
		if full_user is not None:
			print(full_user.id)
			comment = Comment(user_id = full_user.id, text = comment_form.comment.data)

			db.session.add(comment)
			db.session.commit()
			sussess_message = 'Nuevo comentario creado'

			flash(sussess_message)
	return render_template('comment.html', title = 'Comentarios', form= comment_form)


@app.route('/logout')
def logout():
		if 'username' in session:
			print("Se va: " + session['username'])
			session.pop('username')
			print("Se fue..")
		return redirect(url_for('login'))


@app.route('/ajax-login', methods=['POST'])
def ajax_login():
	print(request.form)
	username = request.form['username']
	response = {'status':200, 'username': username, 'id' : 1}
	return json.dumps(response)


@app.route('/create', methods=['GET','POST'])
def create():
    create_form = forms.CreateForm(request.form)
    if request.method == 'POST' and create_form.validate():
        user = User( create_form.username.data,	create_form.password.data, create_form.email.data )
        db.session.add(user)
        db.session.commit()
        success_message = 'Usuario registrado en la DB'
        flash(success_message)
    return render_template('create.html', form= create_form)


@app.route('/reviews/', methods = ['GET'])
@app.route('/reviews/<int:page>', methods = ['GET'])
def reviews(page = 1):
    per_page = 8
    comment_list = Comment.query.join(User).add_columns(User.username, Comment.text, Comment.created_date).paginate(page,per_page,False)
    page_l = {}
    if page == 1:
        page_l["before"] = 1
    else:
         page_l["before"] = page - 1
    if len(comment_list.items) is not 0:
        page_l["after"] = page + 1
    else:
        page_l["after"] = page

    page_l["current"] = page
    return render_template('reviews.html', comments = comment_list, date_format = date_format, page_l=page_l)

if __name__ == '__main__':
	csrf.init_app(app)
	db.init_app(app)
	with app.app_context():
		db.create_all()
	app.run(host='0.0.0.0')
