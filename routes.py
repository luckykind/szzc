from .app import app, db
from flask import render_template, url_for, redirect, flash, request, send_from_directory
from .forms import RegistrationForm, LoginForm, CodeAssetForm
from .models import User, CodeAsset
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import bcrypt
import os
from werkzeug.utils import secure_filename


from flask import render_template
from flask import url_for
from flask import redirect
from flask import flash
from flask import request
from flask import send_from_directory

from .app import app, db
from flask import render_template

@app.route('/')
def index():
    return render_template('index.html')

from flask import send_from_directory
import os

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

# ... 其他路由 ...
