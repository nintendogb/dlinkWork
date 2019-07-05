#!/usr/bin/python3
import json
import hashlib
from flask import Flask
from flask import Blueprint
from flask import request
from flask import redirect
from flask import render_template
from flask import flash
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import login_user
from flask_login import logout_user
import redis
from log import log_bp
import agent.config.parameter as parameter


auth_bp = Blueprint('auth', __name__)
app = Flask(__name__, template_folder='./templates')
app.secret_key = 'sjgl4YUKHU34'
login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Unauthorized User'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def user_loader(user_id):
    user = User()
    user.id = user_id
    return user


class User(UserMixin):
    pass


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth.html')
    r = redis.Redis(
        host=parameter.REDIS_SERVER(),
        port=parameter.REDIS_PORT(),
        decode_responses=True
    )
    user_id = request.form['userId']

    if r.hexists('users', user_id):
        hash_pw = hashlib.md5(request.form['password'].encode()).hexdigest()
        store_pw = json.loads(r.hget('users', user_id))['password']
        if hash_pw == store_pw:
            user = User()
            user.id = user_id
            login_user(user)
            return redirect('/log/newest')

    flash('Input wrong User ID or PASSWORD', 'warning')
    return render_template('auth.html')


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('sign out')
    return render_template('auth.html')


app.register_blueprint(log_bp, url_prefix='/log')
app.register_blueprint(auth_bp, url_prefix='/auth')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
