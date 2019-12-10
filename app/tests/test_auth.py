import pytest
from app.models import User
from app.models import Forum
from app.models import Todo



def test_get_login_page(client):
    response = client.get('/login')
    print (response.data)
    assert response.status_code == 200

    #assert b'Email' in response.data
    #assert b'Password' in response.data

def test_get_main_page(client):
    response = client.get('/forum')
    assert response.status_code == 200

def test_add_user_to_db(db):
    user1 = User(username='john', email='test@test.com', password_hash='test')
    db.session.add(user1)
    db.session.commit()
    assert len(User.query.all()) == 1

def test_add_item_to_forum(db):
    forum1 = Forum(author='john', title='hello')
    db.session.add(forum1)
    db.session.commit()
    assert len(Forum.query.all()) == 1

def test_add_item_to_list(db):
    todo1 = Todo(text='apple', complete=False, importantItem=True)
    db.session.add(todo1)
    db.session.commit()
    assert len(Todo.query.all()) == 1

def test_valid_register(client, db):
    response = client.post('/register',
                                data=dict(username='testing', email='testing@testing.com', password_hash='testing', confirm='testing'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"You are now logged in!" in response.data
    assert b'Hi !' in response.data
    assert b'Log out' in response.data
