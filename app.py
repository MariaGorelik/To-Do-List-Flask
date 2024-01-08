from flask import Flask, render_template, request, redirect, url_for
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'project12345'

notes = []

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.username = username
        self.password = password


@login_required
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        note = request.form.get('note')
        if note:
            notes.append(note)
            return redirect(url_for('index'))
    return render_template('index.html', notes=notes, enumerate=enumerate)


@login_required
@app.route('/delete-note/<int:note_index>/')
def delete_note(note_index):
    if note_index < len(notes):
        del notes[note_index]
    return redirect(url_for('index'))


users = {
    'user1': User('user1', 'password1'),
    'user2': User('user2', 'password2')
}


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = users.get(username)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(e):
    return "Page not found", 404


@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)


if __name__ == '__main__':
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.run(debug=True)