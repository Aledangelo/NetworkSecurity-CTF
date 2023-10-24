import os

from flask import render_template
from flask import Flask, redirect, url_for
from flask import request, jsonify, session, make_response
import sys

from db_modules.connector import dbSql

sys.path.insert(1, '/Users/alessandro/Documents/Università/NetworkSecurity/progettino')

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'mUcKhRX2OrcfRvtH_oe5QHnowvIfA_JYih-5QcpZmd8'


@app.route('/manage', methods=["GET"])
def manage_system():
    if not session.get("nome"):
        return redirect(url_for('home'))
    elif session.get("nome") != 'admin':
        return redirect(url_for('home'))
    dir = request.args.get("dir_form")
    result = os.popen('ls -l ' + str(dir))
    return render_template("admin.html", dir=result.readlines())


@app.route('/admin', methods=["GET"])
def admin_page():
    if not session.get("nome"):
        return redirect(url_for('home'))
    elif session.get("nome") != 'admin':
        return redirect(url_for('home'))
    return render_template("admin.html")


@app.route('/search', methods=['GET'])
def search():
    args = request.args
    if not session.get("nome"):
        return redirect(url_for('home'))
    res = dbSql.selectRowByParam('name', args.get("name"), 'products')
    return render_template('res.html', res=res)


@app.route('/logout', methods=['GET'])
def logout():
    session.pop("nome", None)
    return redirect(url_for('home'))


@app.route('/login', methods=['POST'])
def login():
    nome = request.form['nome']
    passw = request.form['pass']

    if nome and passw:
        res = dbSql.selectRowByParam('username', nome, 'account')
        if res[0]['pass'] == passw:
            session["nome"] = nome
            return redirect(url_for('home'))
        else:
            return make_response('Utente non trovato', 403,
                                 {'WWW-Authenticate': 'Basic realm: "Authentication Failed"'})
    else:
        return make_response('Utente non trovato', 403,
                             {'WWW-Authenticate': 'Basic realm: "Authentication Failed"'})


@app.route('/', methods=['GET'])
def home():
    if not session.get("nome"):
        return render_template('index.html')
    if session.get("nome") == "admin":
        return redirect(url_for("admin_page"))
    return redirect(url_for('sboard'))


@app.route('/dashboard', methods=['GET'])
def sboard():
    if not session.get("nome"):
        return redirect(url_for('home'))
    return render_template('dasboard.html')


if __name__ == '__main__':
    app.run()
