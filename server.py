from flask import Flask, render_template
from werkzeug.utils import redirect
from data.users import User
from data import db_session
from forms.user import RegisterForm
from forms.login_form import LoginForm
from flask_login import login_user, LoginManager, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abobaABOBAaboba'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def root():
    if current_user.is_authenticated:
        return render_template('main.html')
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if (db_sess.query(User).filter(User.email == form.email.data).first()) or \
                (db_sess.query(User).filter(User.name == form.name.data).first()):
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            choose_area=False
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    db_session.global_init("db/warkrasnogorsk.db")
    app.run(host='0.0.0.0', port=8080)
