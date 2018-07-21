from wtforms import Form 
from wtforms import StringField, TextField
from wtforms.fields.html5 import EmailField
from wtforms import validators
from wtforms import HiddenField
from wtforms import PasswordField
from models import User


def length_honeypot(form, field):
	if len(field.data) >0:
		raise validators.ValidationError('Si lo ves, es que sos Juaker')


class CommentForm(Form):
	pass

class LoginForm(Form):
	username = StringField('Nombre de Usuario', 
			[
				validators.length(min=4,max=25, message='La cagaste pibe'),
				validators.Required(message="No te pases y pone tu mierdinombre")	
			]
		)
	password =  PasswordField('Password', 
			[
				validators.Required(message="Sin la pass no entras 'Macho'")
			])

class CreateForm(Form):
	username = TextField('Username',
						   [
							   validators.length(min=4, max=50, message='La cagaste pibe'),
							   validators.Required(message="No te pases y pone tu mierdinombre")
						   ]
						   )
	email  = TextField('Correo Electronico',
						   [
							   validators.length(min=4, max=50, message='La cagaste pibe'),
							   validators.Email(message='Esto es un mail?'),
							   validators.Required(message="No te pases y pone tu mierdinombre")
						   ]
						   )
	password = PasswordField('Password',
							 [
								 validators.Required(message="Sin la pass no entras 'Macho'")
							 ])

	def validate_username(form, field):
		username = field.data
		user = User.query.filter_by(username = username).first()
		if user is not None:
			raise validators.ValidationError('El username ya existe')

class CommentForm(Form):

	comment = StringField('Ingrese su cometario:',
						   [
							   validators.length(min=4, max=25, message='La cagaste pibe'),
							   validators.Required(message="No te pases y pone tu mierda")
						   ]
						   )

	honeypot = HiddenField('', [length_honeypot])