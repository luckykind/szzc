from .app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    assets = db.relationship('CodeAsset', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class CodeAsset(db.Model):
    __tablename__ = 'code_assets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.String(50))
    tags = db.Column(db.String(200))
    file_path = db.Column(db.String(200))
    repo_url = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<CodeAsset {self.name}>'


# 确保 User 模型包含密码哈希方法
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    # ...其他字段...
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
