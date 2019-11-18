from flask import render_template, flash, redirect, url_for
from app import app
from app import db
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.models import User, Todo
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app.forms import CreateListForm

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Homepage')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        # look at first result first()
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # return to page before user got asked to login
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)
    return render_template('login.html', title='Sign in', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/createlist')
def createlist():
        form = CreateListForm()
        todos = Todo.query.filter_by(complete=False).all()
        red = request.form.get('red')
        important = Todo.query.filter_by(importantItem = True).all()

        return render_template('createlist.html', title='Create Lyst', form=form, todos=todos, red = red, important= important)


@app.route('/Lindex')
def testing():
        #todos = Todo.query.all()
        #changed todos =todos

        return render_template('testing.html')

@app.route('/add', methods=['Post'])
def add():
    todo = Todo(text=request.form['todoitem'], complete=False, importantItem=False)
    db.session.add(todo)
    db.session.commit()
    #was orginally directing to testing
    return redirect(url_for('createlist'))

@app.route('/viewlist')
def viewlist():
    todos = Todo.query.filter_by(complete=False).all()
    return render_template('viewlist.html', title='View Lyst', todos=todos)


@app.route('/complete/<id>')
def complete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = True
    todo.importantItem = False
    db.session.commit()
    return redirect(url_for('createlist'))


@app.route('/important/<id>')
def important(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.importantItem = True
    db.session.commit()
    return redirect(url_for('createlist'))


@app.route('/view_complete/<id>')
def view_complete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()
    return redirect(url_for('viewlist'))