from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Note

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dsfgj56547jgfkh90gh4ogot'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)


def check_user(username, password):
    user = User.query.filter_by(username=username, password=password).first()
    return user is not None


@app.route('/main_page', methods=['GET', 'POST'])
def main_page():
    if not 'username' in session:
        return redirect(url_for('login'))
    user = User.query.filter_by(username=session['username']).first()
    if request.method == 'GET':
        notes = Note.query.filter_by(user_id=user.id).all()
        return render_template('index.html', notes=notes, enumerate=enumerate)
    # post
    note = request.form.get('note')
    if note:
        new_note = Note(user_id=user.id, content=note)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('main_page'))


@app.route('/delete-note/<int:note_id>/')
def delete_note(note_id):
    note = Note.query.get(note_id)
    if note:
        db.session.delete(note)
        db.session.commit()
    return redirect(url_for('main_page'))


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_user(username, password):
            session['username'] = username
            return redirect(url_for('main_page'))
        return render_template('login.html', error_message='Неверное имя пользователя или пароль')
    return render_template('login.html')


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method != 'POST':
        return render_template('sign_up.html')
    username = request.form['username']
    password = request.form['password']
    if User.query.filter_by(username=username).first() is None:
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect(url_for('main_page'))
    return render_template('sign_up.html', error_message='This username already exists')


@app.route('/logout')
# @login_required
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(e):
    return "Page not found", 404


if __name__ == '__main__':
    db.init_app(app)
    db.create_all()
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.run(debug=True, host='0.0.0.0')
