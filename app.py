from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from helpers import login_required, connect_db, generate_short_id, error

app = Flask(__name__)

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    user_id = session['user_id']
    conn = connect_db()
    cursor = conn.cursor()
    rows = cursor.execute('SELECT * FROM urls WHERE user_id = ?', (user_id,)).fetchall()
    conn.commit()
    conn.close()

    return render_template('index.html', rows=rows, logged_in=session.get('logged_in'))


@app.route('/<short>')
def navigate_to_link(short):
    if not short:
        return redirect('/')
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE urls SET clicks = clicks + 1 WHERE short = ?', (short,))
    conn.commit()
    url = cursor.execute('SELECT original FROM urls WHERE short = ?', (short,)).fetchone()
    conn.close()

    if not url:
        return error('URL not found', 404)
    
    return redirect(url[0])


@app.route('/create', methods=['POST'])
@login_required
def create():
    original_url = request.form.get('original')

    if not original_url:
        return error('must provide url')

    short_url = generate_short_id()
    user_id = session['user_id']
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO urls (original, short, user_id) VALUES (?, ?, ?)',
        (original_url, short_url, user_id)
    )
    conn.commit()
    conn.close()

    return redirect('/')


@app.route('/delete/<id>')
@login_required
def delete(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM urls WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username:
            return error('must provide username')
        
        if not password:
            return error('must provide password')

        conn = connect_db()
        cursor = conn.cursor()
        user = cursor.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if not user or not check_password_hash(user['hash'], password):
            return error('username or password incorrect', 401)
        
        session['user_id'] = user['id']
        session['logged_in'] = True

        return redirect('/')
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username:
            return error('must provide username')
        
        if not password:
            return error('must provide password')

        conn = connect_db()
        cursor = conn.cursor()
        user = cursor.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if user:
            conn.close()
            return error('user already exists')
        
        password_hash = generate_password_hash(password)

        cursor.execute('INSERT INTO users (username, hash) VALUES (?, ?)', (username, password_hash))
        conn.commit()
        conn.close()

        return redirect('/login')
    else:
        return render_template('register.html')
