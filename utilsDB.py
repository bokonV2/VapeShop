from models import *
from peewee import IntegrityError

def set_liquids(name, salt, cost, count):
    return Liquids.create(
        name = name,
        salt = salt,
        cost = cost,
        count = count
    )


def set_news(title, text):
    return News.create(
        title = title,
        text = text
    )

def set_accounts(fio, email, password, vk=False, history=None):
    try:
        return Accounts.create(
        fio = fio,
        email = email,
        password = password,
        vk = vk,
        history = history
        )
    except IntegrityError:
        return False

def set_messages(whom, to, message):
    return Messages.create(
        whom = whom,
        to = to,
        message = message
    )

def del_liquids(id):
    Liquids.delete_by_id(id)

def edit_liquids(id, cost, count):
    liq = Liquids.select().where(Liquids.id == id).get()
    liq.cost = cost
    liq.count = count
    liq.save()

def get_liquids():
    return Liquids.select()

def get_usersId():
    return list(map(lambda x: x.email, list(Accounts.select())))

def get_users():
    return Accounts.select()

def get_user(email):
    return Accounts.select().where(Accounts.email == email).get()

def userInBd(email):
    return Accounts.select().where(Accounts.email == email).exists()

def user_login(email=None, password=None):
    if userInBd(email):
        acc = get_user(email)
        if acc.password == password:
            return acc.email
    return False


if __name__ == '__main__':
    pass
    # print(edit_liquids())
    # print(del_liquids())
    # print(user_login())
    # print(userInBd("1"))
    # print(set_liquids("1","2",3,4))
    # print(set_news("1","2"))
    # print(set_accounts("1","2","3",True,"5"))
    # print(set_messages(1,2,"3"))
