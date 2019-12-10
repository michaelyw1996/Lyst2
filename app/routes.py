from flask import render_template, flash, redirect, url_for
from . import db
from .forms import LoginForm
from .forms import RegistrationForm
from .models import User, Todo, Forum
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from .forms import CreateListForm, HomeForm
from flask import current_app as app
from . import login_manager


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
        todos = Todo.query.filter_by(user_id=current_user.id,complete=False)
        red = request.form.get('red')
        important = Todo.query.filter_by(user_id=current_user.id, importantItem = True)

        return render_template('createlist.html', title='Create Lyst', form=form, todos=todos, red = red, important = important)


@app.route('/Lindex')
def testing():
        #todos = Todo.query.all()
        #changed todos =todos

        return render_template('testing.html')

@app.route('/add', methods=['Post'])
def add():
    todo = Todo(text=request.form['todoitem'], complete=False, importantItem=False, user_id=current_user.id)
    db.session.add(todo)
    db.session.commit()
    #was orginally directing to testing
    return redirect(url_for('createlist'))

@app.route('/viewlist')
def viewlist():
    todos = Todo.query.filter_by(user_id=current_user.id, complete=False)
    important = Todo.query.filter_by(importantItem=True, user_id=current_user.id)
    red = request.form.get('red')
    return render_template('viewlist.html', title='View Lyst', todos=todos, important = important, red = red)


@app.route('/complete/<id>')
def complete(id):
    todo = Todo.query.filter_by(id = int(id)).first()
    todo.complete = True
    todo.importantItem = False
    db.session.commit()
    return redirect(url_for('viewlist'))


@app.route('/important/<id>')
def important(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.importantItem = True
    db.session.commit()
    return redirect(url_for('viewlist'))


@app.route('/view_complete/<id>')
def view_complete(id):
    todo = Todo.query.filter_by(user_id=current_user.id)
    todo.complete = True
    db.session.commit()
    return redirect(url_for('viewlist'))

@app.route('/viewcalender')
def viewcalender():
    return render_template('viewcalender.html')


@app.route('/forum')
def showBooks():
    forums = db.session.query(Forum).all()
    return render_template('forum.html', forums=forums)

@app.route('/newforumpost', methods=['GET', 'POST'])
def newPost():
    if request.method == 'POST':
        newPost = Forum(title=request.form['name'], author=request.form['author'])
        db.session.add(newPost)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('newforumpost.html')

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None
