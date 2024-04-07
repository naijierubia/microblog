from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

# 初始化数据库连接
db = SQLAlchemy(app)
# 将数据库迁移与app关联
migrate = Migrate(app, db)

# 初始化用户登录管理
login = LoginManager(app)
# 设置登录视图
login.login_view = 'login'

# 从app中导入路由和模型
from app import routes, models