from flask import Flask, render_template, request
from flask_mail import Mail, Message
import smtplib

app = Flask('__name__')

# =============================================================================
# SET YOUR GMAIL APP AND PASSWD
# =============================================================================
gmail_user = 'GMAIL APP'
gmail_app_password = 'PASSWD'


class Inscription():
	def __init__(self, name, nickname, phone, email, labname, address):
		self.name = name
		self.nickname = nickname
		self.phone = phone
		self.email = email
		self.labname = labname
		self.address = address

@app.route('/')
@app.route('/index', methods=["post"])
def index():
	submit = request.form.get('submit')

	user = Inscription(	request.form.get('name'),
						request.form.get('nick'),
						request.form.get('phone'),
						request.form.get('email'),
						request.form.get('lab'),
						request.form.get('address'))

# =============================================================================
# CHECK IF THE USER FILL ALL INPUTS
# =============================================================================
	error = ''
	if (submit and (not user.name or not user.nickname or not user.phone or not user.email or not user.labname or not user.address)):
		error = 'Something went wrong !!'
		return render_template('index.html', error=error)
	elif (submit):

		# =============================================================================
		# E-mail configuration
		# =============================================================================

		sent_from = gmail_user
		sent_to = ['tisatop198@agilekz.com', 'tisatop198@agilekz.com']
		sent_subject = "User informations"
		sent_body = ("Hey, what's up?\n\n"
					"Name : %s\n"
					"Nickname : %s\n"
					"Phone : %s\n"
					"E-mail : %s\n"
					"Labname : %s\n"
					"Address : %s\n"%(user.name, user.nickname, user.phone, user.email, user.labname, user.address))

		email_text = """\
					From: %s
					To: %s
					Subject: %s
					%s
					""" % (sent_from, ", ".join(sent_to), sent_subject, sent_body)

		try:
			server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
			server.ehlo()
			server.login(gmail_user, gmail_app_password)
			server.sendmail(sent_from, sent_to, email_text)
			server.close()

			print('Email sent!')
		except Exception as exception:
			print("Error: %s\n" % exception)
				
		error = 'Well done !!'
	return render_template('index.html', error=error)
