from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit, join_room
from datetime import timedelta, datetime
import flask_login

from models import *
import utilsDB

app = Flask(__name__)
app.secret_key = 'asda3r3tw423wgtss'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

socketio = SocketIO(app)

class User(flask_login.UserMixin):
    pass

############################################################LOGIN@REGISSTRATION
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
        if flask_login.current_user.is_authenticated: return redirect('/home')
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
############################################################LOGIN@REGISSTRATION

@app.route('/') ############################################TEMPLATE
def index():
    return render_template('basic.html')

@app.route('/admin')
@app.route('/admin/<int:id>')
@flask_login.login_required
def admin(id=0): ###########################################ADMIN PAGE
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
def shop(): ################################################SHOP PAGE
    return render_template('shop.html', liqs=utilsDB.get_liquids())

@app.route('/buy/<int:id>')
@flask_login.login_required
def buy_liquids(id): # TODO: TELEGRAMM NOTIFICATION ########BUY LIQUIDS
    acc = utilsDB.get_user(flask_login.current_user.id)
    liq = utilsDB.get_liquid(id)
    if liq.count == 0:
        return redirect('/shop')
    message = f"Куплю {liq.id}:{liq.name},{liq.salt} за {liq.cost}р"
    mess = utilsDB.set_messages(acc.id, acc.id, message)
    utilsDB.set_buy(acc, liq)
    return redirect(f'/messagers/{acc.id}')

@app.route('/news')
def news(): ################################################NEWS PAGE
    return render_template('news.html', news=utilsDB.get_news()) # TODO: TELEGRAMM NOTIFICATION

@app.route('/messagers')
@app.route('/messagers/<int:id>')
@flask_login.login_required
def messagers(id=None): ####################################MESSAGE ROUTER
    acc = utilsDB.get_user(flask_login.current_user.id)
    if id == None:
        if flask_login.current_user.id == "admin":
            return redirect('/chats')
        return redirect(f'/messagers/{acc.id}')
    messages = utilsDB.get_messages(id)
    user = utilsDB.get_userId(id)
    return render_template('messagers.html',
        messages=messages,
        user=user,
        acc=acc
    )

@app.route('/chats')
@flask_login.login_required
def chats(): ###############################################ADMIN CHATS
    return render_template('chats.html', users=utilsDB.get_users())

@app.route('/home')
@flask_login.login_required
def home(): ################################################PROFILE PAGE
    return render_template('home.html',
        acc=utilsDB.get_user(flask_login.current_user.id)
    )

@app.route('/snews', methods=['POST'])
def set_news(): ############################################ADMIN NEWS
    r = request.form.get
    utilsDB.set_news(title=r("title"), text=r("text"))
    return redirect('/news')

###################################################################ADMIN LIQUIDS
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
###################################################################ADMIN LIQUIDS
#########################################################################QUERIES

@app.route('/querries')
def querries():
    return render_template('query.html', querries=utilsDB.get_queries())

@app.route('/qur/<int:id>/<int:state>')
def controlQuerrys(id, state):
    if state:
        utilsDB.accept_queries(id)
    else:
        utilsDB.cancel_queries(id)
    return redirect('/querries')

#########################################################################QUERIES
########################################################################DATABASE
@app.before_request
def before_request():
    db.connect(reuse_if_open=True)

@app.after_request
def after_request(response):
    db.close()
    return response
########################################################################DATABASE

@socketio.on('join')
def on_join(data): #########################################JOIN TO ROOMS CHAT
    join_room(data['channel'])

@socketio.on('Msend')
def on_send(data): # TODO: TELEGRAMM NOTIFICATION ##########RESIVE MESSAGE
    acc = utilsDB.get_user(flask_login.current_user.id)
    id = data['id']
    message = data['message']
    mess = utilsDB.set_messages(id, acc.id, message)
    dta = {
        "mess": message,
        "time": f'{datetime.fromtimestamp(mess.time):%H:%M}',
        "me": f"{acc.id}",
        "channel": id
    }
    emit('Mget', dta, room=id)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8000, debug=True)
    socketio.run(app, host='0.0.0.0', port=8000, debug=True)
