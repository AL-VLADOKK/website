from flask import Flask, url_for, render_template, redirect, abort
from flask_restful import Api
from data.users import User
from data.lots import Lots
from data.paket_users import Paket_Users
from data.tariff import Tariff
from forms.user import RegisterForm
from forms.pay_card import PayCard
from forms.login import LoginForm
from forms.add_lots import AddLotsForm
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
import datetime
from data import db_session
from data.routes import initialize_routes

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/blogs.db")
    initialize_routes(api)
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/", methods=['GET', 'POST'])
def index():
    db_sess = db_session.create_session()
    tarif_flag = True
    if current_user.is_authenticated:
        paket_users = db_sess.query(Paket_Users).filter(Paket_Users.user_id == int(current_user.id)).first()
        tarif_flag = True if paket_users.tariff_id else False
    if current_user.is_authenticated:
        lots = db_sess.query(Lots).filter(
            (Lots.user != current_user) | (Lots.created_date > (datetime.datetime.now() - datetime.timedelta(days=30))))
    else:
        lots = db_sess.query(Lots).filter(Lots.created_date > (datetime.datetime.now() - datetime.timedelta(days=30)))
    return render_template("index.html", lots=lots, title='Лоты', tarif_flag=tarif_flag)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.phone_number == str(form.phone_number.data)).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()

        user.name = form.name.data
        user.surname = form.surname.data
        user.phone_number = form.phone_number.data
        user.money = float(0)
        user.set_password(form.password.data)
        db_sess.add(user)

        paket = Paket_Users()
        paket.tariff_connect = False
        paket.quantity_gb = 0
        paket.quantity_minuts = 0
        paket.quantity_sms = 0
        user.paket_users.append(paket)
        db_sess.add(paket)

        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.phone_number == str(form.phone_number.data)).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/lots', methods=['GET', 'POST'])
@login_required
def add_lots():
    form = AddLotsForm()
    error_gb = [[0, 0], [0, 0]]
    modal = False
    if form.validate_on_submit():
        quantity = form.quantity.data
        price = form.price.data
        if quantity > 120:
            error_gb[0][0], error_gb[1][0] = 1, 1
        elif quantity < 1:
            error_gb[0][0], error_gb[1][0] = 1, 2
        if price > 50:
            error_gb[0][1], error_gb[1][1] = 1, 1
        elif price < 20:
            error_gb[0][1], error_gb[1][1] = 1, 2
        if any(error_gb[0]):
            return render_template('add_lots.html', title='Добавление лота',
                                   form=form, error_gb=error_gb, modal=modal)
        db_sess = db_session.create_session()
        db_sess.expire_on_commit = False

        paket_users = db_sess.query(Paket_Users).filter(Paket_Users.user_id == int(current_user.id)).first()
        if quantity > paket_users.quantity_gb:
            modal = True
            return render_template('add_lots.html', title='Добавление лота',
                                   form=form, error_gb=error_gb, modal=modal)
        paket_users.quantity_gb -= form.quantity.data
        db_sess.commit()
        db_sess.expire_on_commit = False

        lots = Lots()
        lots.quantity = quantity
        lots.price = price

        current_user.lots.append(lots)

        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('add_lots.html', title='Добавление лота',
                           form=form, error_gb=error_gb, modal=modal)


@app.route('/lots/<int:id>', methods=['GET', 'POST'])
@login_required
def buy_lots(id):
    db_sess = db_session.create_session()
    db_sess.expire_on_commit = False
    lots = db_sess.query(Lots).filter(Lots.id == int(id)).first()
    if lots:
        seller = db_sess.query(User).filter(User.id == int(lots.user_id)).first()
        seller.money += lots.quantity * lots.price
        current_user.money -= lots.quantity * lots.price
        current_user_paket = db_sess.query(Paket_Users).filter(Paket_Users.user_id == int(current_user.id)).first()
        current_user_paket.quantity_gb += lots.quantity

        db_sess.delete(lots)
        db_sess.merge(current_user)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/lots_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def lots_delete(id):
    db_sess = db_session.create_session()
    db_sess.expire_on_commit = False
    lots = db_sess.query(Lots).filter(Lots.id == int(id)).first()
    if lots:
        current_user_paket = db_sess.query(Paket_Users).filter(Paket_Users.user_id == int(current_user.id)).first()
        current_user_paket.quantity_gb += lots.quantity
        db_sess.delete(lots)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/pay_card', methods=['GET', 'POST'])
@login_required
def pay_card():
    form = PayCard()
    if form.validate_on_submit():
        money = form.money.data
        db_sess = db_session.create_session()
        current_user.money += money

        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('pay_card.html', title='Добавление лота',
                           form=form)


@app.route("/profiles")
@login_required
def profiles():
    db_sess = db_session.create_session()
    paket_users = db_sess.query(Paket_Users).filter(Paket_Users.user_id == int(current_user.id)).first()
    if paket_users.tariff_id:
        tariff = db_sess.query(Tariff).filter(Tariff.id == int(paket_users.tariff_id)).first()
    else:
        tariff = None
    if current_user.is_authenticated:
        return render_template("profiles.html", title='Профиль', paket_users=paket_users, tariff=tariff)


@app.route("/main")
def main_web():
    return render_template("main.html")
#
#
# @app.route("/tarifs")
# def tarifs():
#     # db_sess = db_session.create_session()
#     # if current_user.is_authenticated:
#     return render_template("tarifs.html")


@app.route("/tarifs")
def tarifs():
    db_sess = db_session.create_session()
    tariffs = db_sess.query(Tariff).all()
    return render_template("tarif.html", tariff=tariffs)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    main()
