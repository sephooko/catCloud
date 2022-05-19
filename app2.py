import email

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '6b4e162fafe974'
app.config['MAIL_PASSWORD'] = 'bbca71a7fc7f07'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)


@app.route("/homepage")
@app.route("/")
def index2():
    return render_template("index2.html")


# @app.route('/create/', methods=('GET', 'POST'))
# def create():
#     if request.method == 'POST':
#         email = request.form['email']
#         msgText = request.form['msgtext']
#         if not email:
#             flash('Email is required!')
#         elif not msgText:
#             flash('Content is required!')
#         else:
#             return redirect(url_for(index2))
#     render_template()


@app.route("/msgsent", methods=('GET', 'POST'))
def msgSent():
    if request.method == 'POST':
        msg = Message('Hello from the other side!', sender=request.form.get('email'), recipients=['mischief@mailtrap.io'])
        msg.body = request.form.get('msgtext')
        mail.send(msg)
    elif request.form.get('email') is None:
        flash('Email is required!')
    elif request.form.get('msgtext') is None:
        flash('Content is required!')
    else:
        return redirect(url_for('index2'))
    return "Message sent!"


if __name__ == '__main__':
    app.run(debug=True)
