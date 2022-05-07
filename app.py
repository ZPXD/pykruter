from flask import Flask, render_template, redirect, url_for

from flask_wtf import FlaskForm
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, DateField, SelectField
from wtforms.validators import DataRequired

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import LoginManager
from flask_login import login_required, current_user, login_user, logout_user

import pandas as pd
import random


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/xdd.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = ':)'

db = SQLAlchemy(app)
login_manager = LoginManager(app)


# Main

@app.route('/')
def index():

    # Dane
    df = pd.read_csv('data/sample.csv')
    
    # Losowanie pytania
    i = random.choice(range(len(df)))
    this_question = df.loc[i, :]
    question = this_question['question']
    answer = this_question['answer']

    return render_template("index.html", question=question, answer=answer)

@app.route('/dodaj_pytanie', methods=["GET", "POST"])
def add_question():
    form = QuestionForm()
    if form.validate_on_submit():
        question = form.question.data
        answer = form.answer.data
        source = form.source.data
        result = form.result.data
        category = form.category.data
        level = form.level.data

        question = Question(question=question, answer=answer, source=source, result=result, category=category, level=level)
        db.session.add(question)
        db.session.commit()

        return redirect( url_for('index'))
    return render_template("dodaj_pytanie.html", form=form)

@app.route('/dodaj_zbior_pytan', methods=["GET", "POST"])
def add_questions_link():
    form = QuestionLinkForm()
    if form.validate_on_submit():

        link = form.link.data
        comment = form.comment.data
        category = form.category.data

        questionslinks = QuestionLink(link=link, comment=comment)
        db.session.add(questionslinks)
        db.session.commit()

        return redirect( url_for('index'))
    return render_template("dodaj_zbior_pytan.html", form=form)


# Login

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    return user

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user:
            if user.check_password(password):
                login_user(user, force=True)
                return redirect( url_for('index'))
        else:
            return "user not found"

    return render_template("login.html", form=form)

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        if User.query.filter_by(email=email).first():
            return 'taki email już istnieje'

        user = User(name=name, email=email, password=password)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return redirect( url_for('index'))
    return render_template("signup.html", form=form)

@login_required
@app.route('/logout')
def logout():
    logout_user()
    return render_template("logout.html")

@login_required
@app.route('/profile/<name>')
def user(name):
    if name == current_user.name:
        return "ok"
    else:
        return "no"


# DB Models

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def set_password(self,password):
        self.password = generate_password_hash(password)
     
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.name)

@app.before_first_request
def create_all():
    db.create_all()
    

class Question(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String())
    answer = db.Column(db.String())
    source = db.Column(db.String())
    result = db.Column(db.String())
    category = db.Column(db.String())
    level = db.Column(db.String())

    def __repr__(self):
        return '<Question {}>'.format(self.question)

class QuestionLink(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String())
    comment = db.Column(db.String())
   
    def __repr__(self):
        return '<QuestionLink {}>'.format(self.link)

# Forms

class QuestionForm(FlaskForm):
    question = StringField(validators=[DataRequired()])
    answer = StringField(validators=[DataRequired()])
    source = StringField(validators=[DataRequired()])
    result = StringField(validators=[DataRequired()])

    category_choices = [
        ('Backend', 'Backend'),
        ('Frontend', 'Frontend'),
        ('Data Science', 'Data Science'),
        ('Testing', 'Testing'),
        ('Cybersecurity', 'Cybersecurity'),
        ('DevOps', 'DevOps'),
        ('AI', 'AI'),
        ('Networking', 'Networking'),
    ]

    level_choices = [
        ('Junior', 'Junior'),
        ('Mid', 'Mid'),
        ('Senior', 'Senior'),
    ]

    category = SelectField(choices=category_choices)
    level = SelectField(choices=level_choices)
    button = SubmitField('Prześlij pytanie')

class QuestionLinkForm(FlaskForm):
    link = StringField(validators=[DataRequired()])
    comment = StringField(validators=[DataRequired()])

    category_choices = [
        ('Backend', 'Backend'),
        ('Frontend', 'Frontend'),
        ('Data Science', 'Data Science'),
        ('Testing', 'Testing'),
        ('Cybersecurity', 'Cybersecurity'),
        ('DevOps', 'DevOps'),
        ('AI', 'AI'),
        ('Networking', 'Networking'),
    ]

    category = SelectField(choices=category_choices)
    button = SubmitField('zaloguj się')

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = StringField('hasło', validators=[DataRequired()])
    submit = SubmitField('zaloguj się')

class SignupForm(FlaskForm):
    name = StringField('nazwa użytkownika', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = StringField('hasło', validators=[DataRequired()])
    confirm_password = StringField('powtórz hasło', validators=[DataRequired()])
    submit = SubmitField('załóż konto')


# Errors

@app.errorhandler(404)
def handle_404(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def handle_500(e):
    return render_template('500.html'), 500


if __name__=="__main__":
    app.run(debug=True)