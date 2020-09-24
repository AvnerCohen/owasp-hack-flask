import sys
import socket
import random
import string
import sqlite3
from flask import Flask, render_template, Response, request, g, redirect
from flask import url_for, make_response

app = Flask(__name__)

DB_PATH = './storage/hackme.db'
PORT = 1337

word_file = "/usr/share/dict/words"
WORDS = open(word_file).read().splitlines()



@app.route("/ping")
def ping():
    resp = Response("More info in Headers.")
    resp.headers['X-Server'] = "Flask"
    return resp


@app.before_request
def before_request():
    if str(request.url_rule) in ['/login', '/ping']:
        return
    if 'user' not in request.cookies:
        print("User not logged in")
        return redirect(url_for('login'))


@app.route('/list')
def list():
    username = request.cookies['user']
    search_by = request.args.get('query', "")
    filter = ""
    if search_by is not "":
        filter = "WHERE PRODUCT like '" + search_by + "%'"
    query_results = run_query('SELECT * FROM STUFF %s' % (filter))
    data = [dict(id=row[0], product=row[1], description=row[2], price=row[3]) for row in query_results.fetchall()]
    sort = {}
    return render_template('index.html', data=data, filter=search_by, username=username)


@app.route('/login', methods=["get"])
def login():
    return render_template('login.html')


@app.route('/login', methods=["post"])
def check_login():
    password = request.form['password']
    username = request.form['name']
    print(username)
    query_results = run_query('SELECT * FROM USERS WHERE password="%s" AND name="%s";' % (password, username))
    if query_results.fetchone():
        response = make_response(redirect('/list'))
        response.set_cookie('user', username)
        return response
    else:
        return render_template('login.html')


@app.route('/profile', methods=["get"])
def profile():
    return render_template('profile.html', username=request.cookies['user'])


@app.route('/profile', methods=["post"])
def profle_update():
    email = request.form['email']
    name = request.form['user']
    query_results = exec_query('UPDATE USERS SET email="%s" WHERE name="%s";' % (email, name))
    return redirect('/list')


#####################################################
def run_query(query):
    print("GOING TO RUN: [%s]" % query)
    g.db = sqlite3.connect(DB_PATH)
    curs = g.db.execute(query)
    return curs


def exec_query(query):
    print("GOING TO EXEC: [%s]" % query)
    g.db = sqlite3.connect(DB_PATH)
    c = g.db.cursor()
    c.execute(query)
    g.db.commit()

@app.before_first_request
def seed_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS USERS
             (name text, password text, email text)''')
    c.execute('''CREATE TABLE IF NOT EXISTS STUFF
             (id integer, product text, description text, price integer)''')
    c.execute('delete from USERS;')
    c.execute('delete from STUFF;')
    users = ['Marko', 'Root', 'Raju', 'Miko']
    for name in users:
        email = name + "@gmail.com"
        c.execute('INSERT INTO USERS VALUES ("%s", "%s", "%s")' % (name, random_string(), email))
    for index in range(50):
        product_no = index
        product = random_word(count=1)
        product_description = random_word(count=8)
        price = random.randrange(10, 100)
        c.execute('INSERT INTO STUFF VALUES (%i, "%s", "%s", %i)' % (product_no, product, product_description, price))
    conn.commit()
    conn.close()
    print("DB SEEDED")


def random_word(count=1):
    return ' '.join(random.choice(WORDS) for _ in range(count))


def random_string(length=12):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
