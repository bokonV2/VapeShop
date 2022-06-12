from flask import Flask, render_template, request, redirect, url_for, session
from models import *
import flask_login
import utilsDB


app = Flask(__name__)
app.secret_key = 'asda3r3tw423wgtss'  # Change this!

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    print(utilsDB.get_usersId())
    if email not in utilsDB.get_usersId():
        print("Bb"*20)
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in utilsDB.get_usersId():
        print("Aa"*20)
        return

    user = User()
    user.id = email
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if flask_login.current_user.is_authenticated:
            return redirect('/home')
        return render_template('login.html')

    r = request.form.get
    acc = utilsDB.user_login(r("email"), r("password"))
    print(acc)
    if acc:
        print(acc)

        user = User()
        user.id = acc
        flask_login.login_user(user)
        return redirect('/home')
    return render_template('login.html', error=1)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        return render_template('login.html')

    r = request.form.get
    acc = utilsDB.set_accounts(
        fio = r("fio"),
        email = r("email"),
        password = r("password")
    )
    if acc:
        user = User()
        user.id = acc.email
        flask_login.login_user(user)
        return redirect('/home')
    return render_template('login.html', error=2)

@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect("/login")

@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')

@app.route('/')
def index():
    return render_template('basic.html')

@app.route('/admin')
@flask_login.login_required
def admin():
    if flask_login.current_user.id == "admin":
        return render_template('admin.html')
    else:
        return redirect('/login')

@app.route('/shop')
@flask_login.login_required
def shop():
    return render_template('shop.html')

@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/home')
@flask_login.login_required
def home():
    acc = utilsDB.get_user(flask_login.current_user.id)
    return render_template('home.html', acc=acc)

# @app.route('/forAda', methods=['GET', 'POST'])
# def forAda():
#     return render_template('forAda.html')

@app.route('/snews', methods=['POST'])
def set_news():
    r = request.form.get
    utilsDB.set_news(title=r("title"), text=r("text"))

@app.route('/sliquids', methods=['POST'])
def set_liquids():
    r = request.form.get
    utilsDB.et_liquids(
        name = r("name"),
        salt = r("salt"),
        cost = r("cost"),
        count = r("count")
    )

@app.route('/saccounts', methods=['POST'])
def set_accounts():
    pass

@app.before_request
def before_request():
    db.connect()

@app.after_request
def after_request(response):
    db.close()
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
