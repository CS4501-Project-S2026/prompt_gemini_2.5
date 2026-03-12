import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, g
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    cur = get_db().cursor()
    cur.execute("SELECT * FROM prompts")
    prompts = cur.fetchall()
    return render_template('index.html', prompts=prompts)

@app.route('/prompt/<int:prompt_id>', methods=['GET', 'POST'])
def prompt(prompt_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cur = get_db().cursor()

    if request.method == 'POST':
        text_response = request.form['text_response']
        file = request.files['file_response']
        filename = ''
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cur.execute("INSERT INTO responses (prompt_id, user_id, text_response, file_path) VALUES (?, ?, ?, ?)",
                    (prompt_id, session['user_id'], text_response, filename))
        get_db().commit()
        return redirect(url_for('prompt', prompt_id=prompt_id))

    cur.execute("SELECT * FROM prompts WHERE id = ?", (prompt_id,))
    prompt = cur.fetchone()

    cur.execute("""
        SELECT r.text_response, r.file_path, u.username
        FROM responses r
        JOIN users u ON r.user_id = u.id
        WHERE r.prompt_id = ?
    """, (prompt_id,))
    responses = cur.fetchall()

    return render_template('prompt.html', prompt=prompt, responses=responses)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = get_db().cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cur.fetchone()
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        try:
            cur = get_db().cursor()
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            get_db().commit()
        except sqlite3.IntegrityError:
            return "Username already exists."
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)