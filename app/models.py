# 导入sqlalchemy和sqlalchemy.orm库
import sqlalchemy as sa
import sqlalchemy.orm as so

# 导入login模块，用于用户认证
from app import login

# 导入db模块，用于数据库操作
from app import db

# 导入datetime和timezone模块，用于处理时间
from datetime import datetime, timezone

# 导入Optional模块，用于处理可选参数
from typing import Optional

# 导入generate_password_hash和check_password_hash函数，用于密码加密和验证
from werkzeug.security import generate_password_hash, check_password_hash

# 导入UserMixin类，用于实现用户认证接口
from flask_login import UserMixin
from hashlib import md5


# 定义User类，用于用户信息存储
class User(UserMixin, db.Model):
    # 定义主键，用于用户唯一标识
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    # 定义用户名，用于用户显示
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    # 定义邮箱，用于用户联系
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    # 定义密码hash，用于存储加密密码
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )

    # 定义用户发帖信息，用于实现一对多关系
    posts: so.WriteOnlyMapped["Post"] = so.relationship(back_populates="author")

    # 定义__repr__方法，用于显示用户信息
    def __repr__(self):
        return "<User {}>".format(self.username)

    # 定义set_password方法，用于设置用户密码
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 定义check_password方法，用于验证用户密码
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"


# 定义Post类，用于帖子信息存储
class Post(db.Model):
    # 定义主键，用于帖子唯一标识
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    # 定义帖子内容，用于存储用户发布的帖子
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    # 定义帖子时间，用于存储帖子发布日期
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc)
    )
    # 定义用户id，用于关联用户和帖子
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    # 定义用户，用于实现一对多关系
    author: so.Mapped[User] = so.relationship(back_populates="posts")

    # 定义__repr__方法，用于显示帖子信息
    def __repr__(self):
        return "<Post {}>".format(self.body)


# 定义@login.user_loader装饰器，用于实现用户认证
@login.user_loader
def load_user(id):
    # 返回指定id的用户
    return db.session.get(User, int(id))
