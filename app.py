from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index():
    user = { 'nickname': 'Miguel' } # выдуманный пользователь
    posts = [ # список выдуманных постов
        {
            'author': { 'nickname': 'John' },
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': { 'nickname': 'Susan' },
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",
        title = 'Home',
        user = user,
        posts = posts)


if __name__ == '__main__':
    app.run()
