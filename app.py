from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from flask_login import (
    LoginManager,
    UserMixin,
    login_required,
    login_user,
    logout_user,
    current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegistrationForm
from functools import wraps
import os

from models import Asset

# 初始化扩展
db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    # 应用配置
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-123')
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'asset_manager.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 初始化扩展
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = '请先登录以访问该页面'

    # 用户模型
    class User(UserMixin, db.Model):
        __tablename__ = 'users'  # 明确指定表名
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(50), unique=True, nullable=False)
        password_hash = db.Column(db.String(128), nullable=False)
        role = db.Column(db.String(20), default='user')
        is_admin = db.Column(db.Boolean, default=False)

        def set_password(self, password):
            self.password_hash = generate_password_hash(password)

        def check_password(self, password):
            return check_password_hash(self.password_hash, password)

        def __repr__(self):
            return f'<User {self.username}>'

    # 权限装饰器
    def admin_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.is_admin:
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    # 用户加载器
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # 路由定义
    @app.route('/')
    @login_required
    def index():
        return render_template('index.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('index'))
            flash('用户名或密码错误', 'danger')
        return render_template('login.html', form=form)

    @app.route('/archived_assets')
    @login_required
    def archived_assets():
        # 已归档资产列表逻辑
        return render_template('archived_assets.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('您已成功退出登录', 'success')
        return redirect(url_for('login'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        form = RegistrationForm()
        if form.validate_on_submit():
            if User.query.filter_by(username=form.username.data).first():
                flash('用户名已被使用，请选择其他用户名', 'danger')
                return redirect(url_for('register'))

            user = User(username=form.username.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('注册成功，请登录', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', form=form)

    @app.route('/asset/entry', methods=['GET', 'POST'])
    @login_required
    def asset_entry():
        # 资产录入逻辑
        return render_template('asset_entry.html')

    @app.route('/search')
    @login_required
    def search_assets():
        query = request.args.get('q', '')
        # 添加搜索逻辑（示例）
        results = Asset.query.filter(
            Asset.asset_name.ilike(f'%{query}%')
        ).all()
        return render_template('search_results.html', results=results)

    @app.route('/review')
    @login_required
    @admin_required
    def review_assets():
        # 审核资产逻辑
        return render_template('review_assets.html')

    # 错误处理
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('403.html'), 403

    # 初始化数据库
    with app.app_context():
        db.create_all()
        # 创建默认管理员（如果不存在）
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                is_admin=True,
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)