import sqlite3
from flask import Flask, render_template, g, flash, request, session, abort, redirect, url_for

DATABASE = '/tmp/flaskr.db'
ENV = 'development'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

def db_conn():
    return sqlite3.connect(app.config["DATABASE"])

@app.before_request
def before():
    g.conn = db_conn()

@app.teardown_request
def teardown(excpetion):
    g.conn.close()

@app.route("/")
def show_entries():
        cursor = g.conn.execute('SELECT title, text FROM entries ORDER BY id DESC')
        entries = [dict(title=row[0], text=row[1]) for row in cursor.fetchall()]
        return render_template('show_entries.html', entries=entries)

@app.route("/add", methods=["POST"])
def add_entry():
    if not session.get("login"):
        abort(401)
    g.conn.execute('INSERT INTO entries (title, text) VALUES (?, ?)',
        [request.form.get('title'), request.form.get('text')])
    g.conn.commit()
    flash("New post added!")
    return redirect(url_for('show_entries'))


@app.route("/login", methods = ["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form.get("username") != app.config.get("USERNAME"):
            error = "Invalid username"
        elif request.form.get("password") != app.config.get("PASSWORD"):
            error = 'Invalid password'
        else:
            session["login"] = True
            flash("Login successfully.")
            return redirect(url_for('show_entries'))
    
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.pop("login", None)
    flash("logout successfully")
    return redirect(url_for("show_entries"))


if __name__ == "__main__":
    app.run()