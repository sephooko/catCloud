from flask import Flask, abort, make_response, request, redirect, render_template, url_for
import pypyodbc
import azurecred
from flask_mail import Mail, Message
import os
from flask_dance.contrib.github import make_github_blueprint, github
import secrets

app = Flask(__name__, template_folder='templates', static_url_path='', static_folder='static')

app.secret_key = secrets.token_hex(16)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '00'
github_blueprint = make_github_blueprint(
    client_id="36ad35ed87c8d5622d02",
    client_secret="165d88c658b57c0a00677c986f3b38f6f5287227",
)
app.register_blueprint(github_blueprint, url_prefix='/login')

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


class AzureDB:
    dsn: str = 'DRIVER=' + azurecred.AZDBDRIVER + ';SERVER=' + azurecred.AZDBSERVER + ';PORT=1433;DATABASE=' + azurecred.AZDBNAME + '; UID=' + azurecred.AZDBUSER + ';PWD=' + azurecred.AZDBPW

    def __init__(self):
        self.conn = pypyodbc.connect(self.dsn)
        self.cursor = self.conn.cursor()

    def finalize(self):
        if self.conn:
            self.conn.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.finalize()

    def __enter__(self):
        return self

    def azureGetData(self):
        try:
            self.cursor.execute("SELECT name, text from data")
            data = self.cursor.fetchall()
            return data
        except pypyodbc.DatabaseError as exception:
            print('Failed to execute query')
            print(exception)
            exit(1)

    def azureAddData(self):
        # cname: str = request.form.get('cname')
        # comment: str = request.form.get('comment')
        self.cursor.execute("""INSERT INTO data (name, text) VALUES (?,?)""", (request.form.get('cname'), request.form.get('comment')))
        self.conn.commit()


@app.route('/sand')
def sent():
    AzureDB().azureAddData()
    with AzureDB() as a:
        data = a.azureGetData()
    return render_template("result.html", data=data)


# @app.route('/index')
# @app.route('/')
# def index():
#     return render_template("index.html")


@app.route('/index')
@app.route('/')
def index():
    if not github.authorized:
        return redirect(url_for('github.login'))
    else:
        account_info = github.get('/user')
    if account_info.ok:
        account_info_json = account_info.json()
        return render_template("index.html") + '<h1>Your Github name is {}</h1>'.format(account_info_json['login'])
    return '<h1>Request failed!</h1>'


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
        msg = Message(subject=request.form.get('subject'), sender=request.form.get('email'),
                      recipients=['mischief@mailtrap.io'])
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
