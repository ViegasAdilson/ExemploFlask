
from flask import Flask, render_template
from flask import redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import models
from forms import RegisterForm, LoginForm
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/market')
def market_page():
    items = models.Item.query.all()
    return render_template('market.html', items=items)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = models.User(username=form.username.data,
                                     email_address=form.email_address.data,
                                     password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))

    if form.errors != {}:  # if there are not errosa from the validation
        for err_msg in form.errors.values():
            flash(
                f'There was an error with creaing a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = models.User.query.filter_by(
            username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(
                f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password are not match! Please try again',
                  category='danger')

    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
