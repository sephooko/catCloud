from flask import Flask, abort, make_response, request, redirect, render_template, url_for
from flask_mail import Mail, Message
import os


app = Flask(__name__, template_folder='templates', static_url_path='', static_folder='static')


app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '6b4e162fafe974'
app.config['MAIL_PASSWORD'] = 'bbca71a7fc7f07'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SUBJECT'] = '<Hello from the other side!>'
secretKey = os.urandom(16)
app.config['SECRET_KEY'] = 'secretKey'

mail = Mail(app)


@app.route('/index')
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/gallery')
def gallery():
    return render_template("gallery.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/msgsent', methods=('GET', 'POST'))
def msgSent():
    if request.method == 'POST':
        msg = Message(subject=request.form.get('subject'), sender=request.form.get('email'), recipients=['mischief@mailtrap.io'])
        msg.body = request.form.get('msgtext')
        mail.send(msg)
    return 'Message sent!'


@app.route('/error_denied')
def error_denied():
    abort(401)


@app.route('/error_internal')
def error_internal():
    return render_template('template.html', name='ERROR 505'), 505


@app.route('/error_not_found')
def error_not_found():
    response = make_response(render_template('template.html', name='ERROR 404'), 404)
    response.headers['X-Something'] = 'A value'
    return response


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
