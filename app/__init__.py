from flask import Flask
from flask_bootstrap import Bootstrap
from app.models import *
from flask_login import LoginManager, logout_user, login_user, login_required


app = Flask(__name__)
app.debug = True
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'development key'
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader  # 使用user_loader装饰器的回调函数非常重要，他将决定 user 对象是否在登录状态
def user_loader(user_id):  # 这个id参数的值是在 login_user(user)中传入的 user 的 id 属性
    print(user_id)
    return models.User.query.filter(models.User.name == user_id)


with app.app_context():

    db.init_app(app)
    # db.drop_all()
    db.create_all()


# to avoid import the app of views but there is no app in package app.
# so place it there
from app import views

