from flask import Flask, render_template, redirect, url_for, jsonify

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
import os
from urllib.parse import urlparse

app = Flask(__name__)

here = os.getcwd()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////{}/db/xddddd.db'.format(here)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = ':)'

db = SQLAlchemy(app)
login_manager = LoginManager(app)


# Main

@app.route('/')
def index():

    # Question.
    questions = Question.query.all()
    if questions:
        question = random.sample(questions, 1)
    else:
        question = {}

    return render_template("index.html", question=question)


@app.route('/czytaj_dokumentacje_bo_madre_sa_i_przydatne', methods=['GET', 'POST'])
def libraries_mapping():
    '''
    To be developed.
    '''
    
    mapping = {

        # Most important libraries:
        'Aktualizowana kolekcja bibliotek i linków dokumentacji.' : True,

        # System libraries:
        'os' : 'https://docs.python.org/3/library/os.html',
        'sys' : 'https://docs.python.org/3/library/sys.html',
 
        # Flask libraries:
        'flask' : 'https://flask.palletsprojects.com',
        'flask_login' : 'https://flask-login.readthedocs.io',
        'werkzeug' : 'https://werkzeug.palletsprojects.com/en/2.1.x/',
        'flask_wtf' : 'https://flask-wtf.readthedocs.io',
        'wtforms' : 'https://wtforms.readthedocs.io',
        'flask_sqlalchemy' : 'https://flask-sqlalchemy.palletsprojects.com',
        
        # Time libraries:
        'time' : 'https://docs.python.org/3/library/datetime.html',
        'datetime' : 'https://docs.python.org/3/library/datetime.html',
        'calendar' : 'https://docs.python.org/3/library/calendar.html',
        'pytz' : '',

        # Data science libraries:
        'pandas' : 'https://pandas.pydata.org/docs/index.html',
        'matplotlib' : 'https://matplotlib.org/stable/index.html',
        'seaborn' : 'https://seaborn.pydata.org/',
        'numpy' : 'https://numpy.org/',
        'scipy' : 'https://scipy.org/',
        'sklearn' : 'https://scikit-learn.org/stable/',
        'keras' : 'https://keras.io/',
        'textblob' : '', 
        'nltk' : '',

        # Other usefull libraries:
        'random' : 'https://docs.python.org/3/library/random.html',
        'requests' : 'https://docs.python-requests.org',
        'json' : '',
        'pprint' : '',
        'tweepy' : '',
        'webbrowser' : '',
        'configparser' : '',

        # NEXT: add more and remap all by more accurate categories.

    }
    return mapping


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
        approved = False # TBD
        question = Question(question=question, answer=answer, source=source, result=result, category=category, level=level, approved=approved)
        db.session.add(question)
        db.session.commit()
        return redirect( url_for('index'))
    return render_template("add_question.html", form=form)

@app.route('/dodaj_kolekcje_pytan', methods=["GET", "POST"])
def add_questions_collection():
    form = QuestionCollectionForm()
    if form.validate_on_submit():
        link = form.link.data
        title = form.title.data
        comment = form.comment.data
        category = form.category.data
        level = form.level.data
        approved = False
        source = urlparse(link).netloc
        questionslinks = QuestionCollection(link=link, title=title, comment=comment, category=category, approved=approved, source=source)
        db.session.add(questionslinks)
        db.session.commit()
    return render_template("add_questions_collection.html", form=form)

@app.route('/kolekcje_pytan', methods=["GET", "POST"])
def question_collections():
    question_collections = QuestionCollection.query.all()
    form = GoToCollection()
    if form.validate_on_submit():
        return redirect( url_for('add_questions_collection'))
    return render_template("question_collections_list.html", form=form, question_collections=question_collections)

@app.route('/pytania', methods=["GET", "POST"])
def questions():
    questions = Question.query.all()
    form = GoToAddQuestion()
    if form.validate_on_submit():
        return redirect( url_for('add_question'))
    return render_template("questions.html", form=form, questions=questions)

@app.route('/pytania/<int:question_id>', methods=["GET", "POST"])
def question(question_id):
    question = Question.query.filter_by(id=question_id).first()
    return render_template("question.html", question=question)


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
def user_profile(name):
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
    if not 'db' in os.listdir():
        os.mkdir('db')
    db.create_all()
    

class Question(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String())
    answer = db.Column(db.String())
    source = db.Column(db.String())
    result = db.Column(db.String())
    category = db.Column(db.String())
    level = db.Column(db.String())
    approved = db.Column(db.String())

    def __repr__(self):
        return '<Question {}>'.format(self.question)

class QuestionCollection(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String())
    title = db.Column(db.String())
    comment = db.Column(db.String())
    category = db.Column(db.String())
    level = db.Column(db.String())
    approved = db.Column(db.String())
    source = db.Column(db.String())
   
    def __repr__(self):
        return '<QuestionLink {}>'.format(self.link)

# Forms

class QuestionForm(FlaskForm):
    question = TextAreaField(validators=[DataRequired()])
    answer = TextAreaField(validators=[DataRequired()])
    source = StringField(validators=[DataRequired()])
    result = StringField(validators=[DataRequired()])

    category_choices = [
        (1, 'Backend'),
        (2, 'Frontend'),
        (3, 'Data Science'),
        (4, 'Testing'),
        (5, 'Cybersecurity'),
        (6, 'DevOps'),
        (7, 'AI'),
        (8, 'Networking'),
    ]

    level_choices = [
        (1, 'Junior'),
        (2, 'Mid'),
        (3, 'Senior'),
        (4, 'Ogólne'),
    ]

    category = SelectField(choices=category_choices)
    level = SelectField(choices=level_choices)
    button = SubmitField("Dodaj pytanie.")

class GoToAddQuestion(FlaskForm):
    button = SubmitField("Dodaj pytanie")

class GoToCollection(FlaskForm):
    button = SubmitField("Dodaj kolekcję pytań")

class QuestionCollectionForm(FlaskForm):
    link = StringField(validators=[DataRequired()])
    title = StringField(validators=[DataRequired()], render_kw={"placeholder": "50 pytań z 2022 roku dla początkującego programisty"})
    comment = TextAreaField(validators=[DataRequired()])

    category_choices = [
        (1, 'Backend'),
        (2, 'Frontend'),
        (3, 'Data Science'),
        (4, 'Testing'),
        (5, 'Cybersecurity'),
        (6, 'DevOps'),
        (7, 'AI'),
        (8, 'Networking'),
    ]

    level_choices = [
        (1, 'Junior'),
        (2, 'Mid'),
        (3, 'Senior'),
        (4, 'Ogólne'),
    ]

    category = SelectField(choices=category_choices)
    level = SelectField(choices=level_choices)
    button = SubmitField('Dodaj pytanie.')

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = StringField('hasło', validators=[DataRequired()])
    button = SubmitField('zaloguj się')

class SignupForm(FlaskForm):
    name = StringField('nazwa użytkownika', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = StringField('hasło', validators=[DataRequired()])
    confirm_password = StringField('powtórz hasło', validators=[DataRequired()])
    
    button = SubmitField('załóż konto')


# Errors

@app.errorhandler(404)
def handle_404(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def handle_500(e):
    return render_template('500.html'), 500


if __name__=="__main__":
    app.run(debug=True)