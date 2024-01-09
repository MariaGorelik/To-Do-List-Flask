from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'project12345'

notes = []

users_data = {
    'user1': 'password1',
    'user2': 'password2'
}


def check_user(username, password):
    # Здесь можно реализовать проверку данных пользователя на сервере
    # В этом примере мы храним данные пользователей в словаре на сервере
    if username in users_data and users_data[username] == password:
        return True
    return False


@app.route('/main_page', methods=['GET', 'POST'])
def main_page():
    if 'username' in session:
        if request.method == 'POST':
            note = request.form.get('note')
            if note:
                notes.append(note)
                return redirect(url_for('main_page'))
        return render_template('index.html', notes=notes, enumerate=enumerate)
    return redirect(url_for('login'))


@app.route('/delete-note/<int:note_index>/')
def delete_note(note_index):
    if note_index < len(notes):
        del notes[note_index]
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


@app.route('/logout')
# @login_required
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(e):
    return "Page not found", 404


if __name__ == '__main__':
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.run(debug=True)
