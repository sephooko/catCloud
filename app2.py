from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '6b4e162fafe974'
app.config['MAIL_PASSWORD'] = 'bbca71a7fc7f07'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


mail = Mail(app)


@app.route("/")
def index2():
    msg = Message('Hello from the other side!', sender='peter@mailtrap.io', recipients=['paul@mailtrap.io'])
    msg.body = "Hey Paul, sending you this email from my Flask app, lmk if it works"
    mail.send(msg)
    return "Message sent!"


if __name__ == '__main__':
    app.run(debug=True)
