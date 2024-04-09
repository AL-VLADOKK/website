from flask import Flask
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():

    db_session.global_init("db/blogs.db")
    user = User()
    user.name = "Пользователь 3"
    user.about = "биография пользователя 3"
    user.email = "email3@email.ru"
    db_sess = db_session.create_session()
    user = db_sess.query(User).first()
    print(user.name)
    for user in db_sess.query(User).all():
        print(user)
    for user in db_sess.query(User).filter(User.id > 1, User.email.notilike("%1%")):
        print(user)
    # app.run()
#dfsfs

if __name__ == '__main__':
    main()
