from flask import Flask, render_template, request
import smtplib

app = Flask('__name__')

# =============================================================================
# SET YOUR GMAIL APP AND PASSWD
# =============================================================================
gmail_user = 'soufiane.ougouammou@gmail.com'
gmail_app_password = 'mfslpqlorscqatdw'
sent_from = gmail_user
sent_to = ['kepay40496@tmauv.com', 'kepay40496@tmauv.com']

class Inscription():
	def __init__(self, name, nickname, phone, email, labname, address):
		self.name = name
		self.nickname = nickname
		self.phone = phone
		self.email = email
		self.labname = labname
		self.address = address

class contact():
    def __init__(self, sujet, nom, prénom, mail, nomlab, message):
        self.sujet = sujet
        self.nom = nom
        self.prénom = prénom
        self.mail = mail
        self.nomlab = nomlab
        self.message = message

def sendMail(gmail_user, gmail_app_password, sent_from, sent_to, email_text):
	try:
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.ehlo()
		server.login(gmail_user, gmail_app_password)
		server.sendmail(sent_from, sent_to, email_text)
		server.close()

		print('Email sent!')
	except Exception as exception:
		print("Error: %s\n" % exception)

def sendUserInfos(user, submit_subscript):
	error = ''
	if (submit_subscript and (not user.name or not user.nickname or not user.phone or not user.email or not user.labname or not user.address)):
		error = 'Something went wrong !!'
		return (error)
	elif (submit_subscript):

		# =============================================================================
		# E-mail configuration
		# =============================================================================

		sent_subject = "New User informations"
		sent_body = ("New user information:\n\n"
					"Name : %s\n"
					"Nickname : %s\n"
					"Phone : %s\n"
					"E-mail : %s\n"
					"Labname : %s\n"
					"Address : %s\n" % (user.name, user.nickname, user.phone, user.email, user.labname, user.address))

		email_text = """\
					From: %s
					To: %s
					Subject: %s
					%s
					""" % (sent_from, ", ".join(sent_to), sent_subject, sent_body)

		sendMail(gmail_user, gmail_app_password, sent_from, sent_to, email_text)
		error = 'Well done !!'
	return (error)

def sendContactInfos(contacts, submit_contact):
	error = ''
	if (submit_contact and (not contacts.sujet or not contacts.nom or not contacts.prénom or not contacts.mail or not contacts.nomlab or not contacts.message)):
		error = 'Something went wrong !!'
		return (error)
	elif (submit_contact):
		# =============================================================================
		# E-mail configuration
		# =============================================================================
		sent_subject = "New User contact"
		sent_body = ("Contact information:\n\n"
					"Sujet : %s\n"
					"Nom : %s\n"
					"prenom : %s\n"
					"E-mail : %s\n"
					"Labname : %s\n"
					"Message : %s\n" % (contacts.sujet, contacts.nom, contacts.prénom, contacts.mail, contacts.nomlab, contacts.message))

		email_text = """\
					From: %s
					To: %s
					Subject: %s
					%s
					""" % (sent_from, ", ".join(sent_to), sent_subject, sent_body)

		sendMail(gmail_user, gmail_app_password, sent_from, sent_to, email_text)
		error = 'Well done !!'
	return (error)


@app.route('/')
@app.route('/index', methods=["post"])
def index():
	submit_subscript = request.form.get('submit')
	submit_contact = request.form.get('send')

	user = Inscription(	request.form.get('name'),
						request.form.get('nick'),
						request.form.get('phone'),
						request.form.get('email'),
						request.form.get('lab'),
						request.form.get('address'))
	
	contacts = contact(request.form.get('sujet'),
					request.form.get('nom'),
					request.form.get('prénom'),
					request.form.get('mail'),
					request.form.get('nomlab'),
					request.form.get('message'))

# =============================================================================
# CHECK IF THE USER FILL ALL INPUTS
# =============================================================================
	contactError = ''
	inscError = ''
	if (submit_subscript):
		inscError = sendUserInfos(user, submit_subscript)
	elif (submit_contact):
		contactError = sendContactInfos(contacts, submit_contact)
	
	return render_template('index.html', inscError=inscError, contactError=contactError)
