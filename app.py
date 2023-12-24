from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

notes = []


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        note = request.form.get('note')
        if note:
            notes.append(note)
            return redirect(url_for('index'))
    return render_template('index.html', notes=notes, enumerate=enumerate)


@app.route('/delete-note/<int:note_index>/')
def delete_note(note_index):
    if note_index < len(notes):
        del notes[note_index]
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

# from flask import Flask, render_template, request, redirect, url_for
#
# app = Flask(__name__)
#
# notes = []
#
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     global notes
#     if request.method == 'POST':
#         note = request.form.get('note')
#         if note:
#             notes.append(note)
#             return redirect(url_for('index'))
#     #notes = ['Заметка 1', 'Заметка 2', 'Заметка 3']
#     return render_template('index.html', notes=notes)
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
