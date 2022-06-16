from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
import flask_login
from models import *
import utilsDB

app = Flask(__name__)
app.secret_key = 'asda3r3tw423wgtss'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in utilsDB.get_usersId():
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in utilsDB.get_usersId():
        return

    user = User()
    user.id = email
    return user

@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect("/login")

@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if flask_login.current_user.is_authenticated:
            return redirect('/home')
        return render_template('login.html')

    r = request.form.get
    acc = utilsDB.user_login(r("email"), r("password"))
    if acc:
        user = User()
        user.id = acc
        flask_login.login_user(user, remember=True, duration=timedelta(days=365))
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

@app.route('/')
def index():
    return render_template('basic.html')

@app.route('/admin')
@app.route('/admin/<int:id>')
@flask_login.login_required
def admin(id=0):
    if flask_login.current_user.id == "admin":
        if id == 1:
            acc = utilsDB.get_liquids()
        elif id == 2:
            acc = utilsDB.get_users()
        else:
            acc = None
        return render_template('admin.html', id=id, acc=acc)
    else:
        return redirect('/login')

@app.route('/shop')
@flask_login.login_required
def shop():
    liqs = utilsDB.get_liquids()
    return render_template('shop.html', liqs=liqs)

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
    utilsDB.set_liquids(
        name = r("name"),
        salt = r("salt"),
        cost = r("cost"),
        count = r("count")
    )
    return redirect('/shop')

@app.route('/eliquids', methods=['POST'])
def edit_liquids():
    r = request.form.get
    utilsDB.edit_liquids(r("id"),r("price"),r("count"))
    return redirect('/admin/1')

@app.route('/admin/del/<int:id>')
def del_liquids(id):
    utilsDB.del_liquids(id)
    return redirect('/admin/1')

@app.before_request
def before_request():
    db.connect()

@app.after_request
def after_request(response):
    db.close()
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
