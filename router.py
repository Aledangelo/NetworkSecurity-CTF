import os

from flask import render_template
from flask import Flask, redirect, url_for
from flask import request, jsonify, session, make_response
import sys
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, set_access_cookies

from db_modules.connector import dbSql

sys.path.insert(1, '/Users/alessandro/Documents/Università/NetworkSecurity/progettino')


app = Flask(__name__)

app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['SECRET_KEY'] = 'mUcKhRX2OrcfRvtH_oe5QHnowvIfA_JYih-5QcpZmd8'
jwt = JWTManager(app)

'''
def token_required(func):
    @wraps(func)
    def decorate(*args, **kwargs):
        token = request.args.get('token')
        print(token)
        if not token:
            return jsonify('Alert: Token is missing or corrupted')
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
            print(payload)
            expiration = datetime.fromisoformat(payload['expiration'])
            if expiration > datetime.utcnow():
                res = dbSql.selectRowByParam('id', payload['id'], 'account')
                if res[0]['id'] != payload['id']:
                    return jsonify('Alert: Token is missing or corrupted')
        except Exception as e:
            return jsonify('Alert: ' + str(e))
        return func(*args, **kwargs)

    return decorate

'''


@app.route('/manage', methods=["GET"])
@jwt_required()
def manage_system():
    auth = dbSql.selectRowByParam('id', get_jwt_identity(), 'account')
    if auth[0]['sessione'] is None:
        return render_template("index.html")
    if auth[0]['id'] != 2:
        return render_template("dasboard.html")

    dir = request.args.get("dir_form")
    result = os.popen('ls -l ' + str(dir))
    return render_template("admin.html", dir=result.readlines())


@app.route('/admin', methods=["GET"])
@jwt_required()
def admin_page():
    auth = dbSql.selectRowByParam('id', get_jwt_identity(), 'account')
    if auth[0]['sessione'] is None:
        return render_template("index.html")
    if auth[0]['id'] != 2:
        return render_template("dasboard.html")
    return render_template("admin.html")


@app.route('/search', methods=['GET'])
@jwt_required()
def cerca():
    args = request.args
    # print(get_jwt_identity())
    auth = dbSql.selectRowByParam('id', get_jwt_identity(), 'account')
    if auth[0]['sessione'] is None:
        return render_template('index.html')
    res = dbSql.selectRowByParam('nome', args.get("nome"), 'prodotti')
    return render_template('res.html', res=res)
    # return dbSql.selectRowByParam('nome', args.get("nome"), 'prodotti')


@app.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    session['logged_in'] = False
    # dbSql.updateRowByParam('sessione', get_jwt_identity(), 'account', 'id', 'null')
    dbSql.deleteSession(get_jwt_identity(), 'account')
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    '''
    if request.method == 'POST':
        nome = request.form['nome']
        pwd = request.form['pass']

        res = dbSql.selectRowByParam('nome', nome, 'account')
        if res is not None and len(res) != 0:
            if res[0]['password'] != pwd:
                return None
            else:
                # session = ''.join(random.choice('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890')
                # for x in range(32))
                id = res[0]['id']
                session["user"] = id
                return render_template('dasboard.html', nome=nome)
    '''

    nome = request.form['nome']
    passw = request.form['pass']

    if nome and passw:
        res = dbSql.selectRowByParam('nome', nome, 'account')
        if res[0]['password'] == passw:
            access_token = create_access_token(identity=res[0]['id'])
            dbSql.updateRowByParam('sessione', res[0]['id'], 'account', 'id', access_token)
            resp = make_response(redirect(url_for('sboard')))
            set_access_cookies(resp, access_token)
            return resp
        else:
            return make_response('Utente non trovato', 403,
                                 {'WWW-Authenticate': 'Basic realm: "Authentication Failed"'})
    else:
        return make_response('Utente non trovato', 403,
                             {'WWW-Authenticate': 'Basic realm: "Authentication Failed"'})


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/dashboard', methods=['GET'])
@jwt_required()
def sboard():
    auth = dbSql.selectRowByParam('id', get_jwt_identity(), 'account')
    if auth[0]['sessione'] is None:
        return render_template('index.html')
    return render_template('dasboard.html')


@app.route('/demo', methods=['GET'])
def search():
    args = request.args
    return dbSql.selectRowByParam('nome', args.get("nome"), 'prova')


if __name__ == '__main__':
    app.run()
