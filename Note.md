# 第一章 Hello，Flask！

## 创建项目

```bash
$ mkdir microblog
$ cd microblog
```

> 创建虚拟环境并激活

```bash
$ python -m venv venv
$ venv/Scripts/activate
```

> 安装Flask

```bash
$ pip install flask
```

## “Hello, Flask”应用

```py
# 创建app/__init__.py
from flask import Flask

app = Flask(__name__)

from app import routes
```

```python
# 创建app/routes.py
# 第二个app是__init__.py中实例化的对象
from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, Flask!"
```

```py
# 创建microblog.py
from app import app
```

现在整个文件为：

```txt
microblog/
  venv/
  app/
    __init__.py
    routes.py
  microblog.py
```

> 设置环境变量，定义Flask入口

```bash
$ set FLASK_APP=microblog.py
# 启动Flask
$ flask run
```

之后在http://localhost:5000/与http://localhost:5000/index能看到

![image-20240405234203503](Note_asset/image-20240405234203503.png)

## 设置环境变量

> 每次都要设置环境变量太麻烦，使用第三方包简化操作

```bash
$ pip install python-dotenv
```

```
# 创建.flaskenv
FLASK_APP=microblog.py
```

flask将寻找该文件并导入所有的环境变量

# 第二章 模板文件

> 开启debug，这样文件出现修改保存就会刷新

```py
# 修改microblog.py
from app import app

if __name__ == "__main__":
    app.run(debug=True)
```

这样就能通过`microblog.py`启动并开启debug了

## 什么是模板文件

先修改之前的`app/routes.py`文件，让他返回一段完整的HTML

```py
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    return '''
<html>
    <head>
        <title>Home Page - Microblog</title>
    </head>
    <body>
        <h1>Hello, ''' + user['username'] + '''!</h1>
    </body>
</html>'''
```

> 每次都需要返回一大堆字符串太难以管理了，因此需要用到模板文件

首先创建`app/templates`文件夹

然后创建`app/templates/index.html`

```html
<!doctype html>
<html>
    <head>
        <title>{{ title }} - Microblog</title>
    </head>
    <body>
        <h1>Hello, {{ user.username }}!</h1>
    </body>
</html>
```

双花括号代表需要渲染的内容

现在重新修改`*app/routes.py`

```py
from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)
```

## 条件渲染

修改`app/templates/index.html`

```html
<!doctype html>
<html>
    <head>
        {% if title %}
        <title>{{ title }} - Microblog</title>
        {% else %}
        <title>Welcome to Microblog!</title>
        {% endif %}
    </head>
    <body>
        <h1>Hello, {{ user.username }}!</h1>
    </body>
</html>
```

这样如果没有传入**title**就会使用**Welcome to Microblog!**作为标题

## 循环渲染

修改`app/templates/index.html`

```html
<!doctype html>
<html>
    <head>
        {% if title %}
        <title>{{ title }} - Microblog</title>
        {% else %}
        <title>Welcome to Microblog</title>
        {% endif %}
    </head>
    <body>
        <h1>Hi, {{ user.username }}!</h1>
        {% for post in posts %}
        <div><p>{{ post.author.username }} says: <b>{{ post.body }}</b></p></div>
        {% endfor %}
    </body>
</html>
```

修改`*app/routes.py`

```py
from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)
```

## 模板继承

> 对于重复利用的部件，使用模板继承重复利用

对于导航栏，这个部件需要重复利用，创建`app/templates/base.html`

```html
<!doctype html>
<html>
    <head>
      {% if title %}
      <title>{{ title }} - Microblog</title>
      {% else %}
      <title>Welcome to Microblog</title>
      {% endif %}
    </head>
    <body>
        <div>Microblog: <a href="/index">Home</a></div>
        <hr>
        {% block content %}{% endblock %}
    </body>
</html>
```

修改`app/templates/index.html`

```html
{% extends "base.html" %}

{% block content %}
    <h1>Hi, {{ user.username }}!</h1>
    {% for post in posts %}
    <div><p>{{ post.author.username }} says: <b>{{ post.body }}</b></p></div>
    {% endfor %}
{% endblock %}
```

这样就将`index.html`中的内容插入了`base.html`中的块

# 第三章 表单

需要安装**flask-wtf**扩展处理表单

我们可以通过使用字典给**app实例**添加配置

```py
app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
```

但是通常做法是在根目录创建一个`config.py`文件配置

```py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
```

然后在`app/__init__.py`中修改

```py
from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
```

这样就为web应用添加了一个秘钥

## 用户登入表单

首先创建一个`app/forms.py`

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    # DataRequired()只验证填入内容是否为空，当然可以添加其他验证器
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
```

## 表单模板文件

创建`app/templates/login.html`

```html
{% extends "base.html" %}

{% block content %}
    <h1>Sign In</h1>
    <form action="" method="post" novalidate>
        {{ form.hidden_tag() }}
        <p>
            {{ form.username.label }}<br>
            {{ form.username(size=32) }}
        </p>
        <p>
            {{ form.password.label }}<br>
            {{ form.password(size=32) }}
        </p>
        <p>{{ form.remember_me() }} {{ form.remember_me.label }}</p>
        <p>{{ form.submit() }}</p>
    </form>
{% endblock %}
```

由于验证由后端完成，因此无需让前端验证

**form.hidden_tag（）**生成一个隐藏字段，其中包含一个用于保护表单免受CSRF攻击的令牌。要保护表单，只需包含此隐藏字段，并在Flask配置中定义SECRET_KEY变量。如果你处理好这两件事，Flask WTF会为你做剩下的事情。

## 表单界面

在`app/routes.py`添加下面的内容

```py
from flask import render_template
from app import app
from app.forms import LoginForm

# ...

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)
```

这样在http://localhost:5000/login就能看到

![image-20240406133623825](Note_asset/image-20240406133623825.png)

## 接收表单数据

当前如果点击提交按钮会显示方式 **"Method Not Allowed"**，是因为还没编写接收表单的逻辑

```python
from flask import render_template, flash, redirect

# 接收GET和POST请求，默认值接收GET
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # 当浏览器发送GET请求获取表单页面时返回False，这样就跳过了if逻辑，返回了表单界面
    # form.validate_on_submit()会对用户提交的表单进行收集验证，如果全部符合则返回True并重定向index界面
    # 如果有不符合则返回False并刷新界面
    if form.validate_on_submit():
        # flash()方法会储存这条信息
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)
```

修改`app/templates/base.html`显示flash消息

```html
<html>
    <head>
        {% if title %}
        <title>{{ title }} - microblog</title>
        {% else %}
        <title>microblog</title>
        {% endif %}
    </head>
    <body>
        <div>
            Microblog:
            <a href="/index">Home</a>
            <a href="/login">Login</a>
        </div>
        <hr>
        <!-- 获取flash消息 -->
        {% with messages = get_flashed_messages() %}
        {% if messages %}
        <ul>
            {% for message in messages %}
            <li>{{ message }}</li>
            {% endfor %}
        </ul>
        {% endif %}
        {% endwith %}
        {% block content %}{% endblock %}
    </body>
</html>
```

这样登入后就会在主页面看到

![image-20240406140934396](Note_asset/image-20240406140934396.png)

当使用**get_flashed_messages()**请求一次后，消息就会被删除

## 改进表单验证

首先对页面`app/templates/login.html`进行修改，让用户知道自己输入了错误的数据

```html
{% extends "base.html" %}

{% block content %}
    <h1>Sign In</h1>
    <form action="" method="post" novalidate>
        {{ form.hidden_tag() }}
        <p>
            {{ form.username.label }}<br>
            {{ form.username(size=32) }}<br>
            {% for error in form.username.errors %}
            <span style="color: red;">[{{ error }}]</span>
            {% endfor %}
        </p>
        <p>
            {{ form.password.label }}<br>
            {{ form.password(size=32) }}<br>
            {% for error in form.password.errors %}
            <span style="color: red;">[{{ error }}]</span>
            {% endfor %}
        </p>
        <p>{{ form.remember_me() }} {{ form.remember_me.label }}</p>
        <p>{{ form.submit() }}</p>
    </form>
{% endblock %}
```

这样在出错时就会显示

![image-20240406141845642](Note_asset/image-20240406141845642.png)

对于导航栏和重定向功能，目前虽然效果完美，但是目前是直接编写的链接，对于后期维护不利，因此替换`app/templates/base.html`中的

```html
        <div>
            Microblog:
            <a href="{{ url_for('index') }}">Home</a>
            <a href="{{ url_for('login') }}">Login</a>
        </div>
```

修改`app/routes.py`

```python
from flask import render_template, flash, redirect, url_for

# ...

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # ...
        return redirect(url_for('index'))
    # ...
```

# 第四章 数据库

这里选择无服务的简单**sqlite**搭建数据库，首先安装扩展：

```bash
$ pip install flask-sqlalchemy
```

为了方便数据迁移，安装：

```bash
$ pip install flask-migrate
```

## Flask SQLAlchemy配置

对`config.py`文件添加一项

```python
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or /
        'sqlite:///' + os.path.join(basedir, 'app.db')
```

设置**SQLALCHEMY_DATABASE_URI**参数，用于指定数据库的URL。如果**DATABASE_URL**环境变量已设置，则使用该值；否则，使用默认值**"sqlite:///app.db"**，表示使用SQLite数据库，并将数据库文件存储在**basedir**目录下。

然后在`app/__init__.py`中建立数据库和数据迁移的实例：

```python
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
```

## 数据库模块

之后要创建如下图所示的数据库，其中id作为主键使用

![ch04-users](Note_asset/ch04-users.png)

使用代码创建数据库`app/models.py`

```python
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return "<User {}>".format(self.username)
```

**sqlalchemy**和**sqlalchemy.orm**模块，它们提供了使用数据库所需的大部分元素。

为了定义允许为空或可为 **null** 的列，使用**Optional**

## 数据迁移

创建迁移存储库

```bash
 $ flask db init
```

执行后会创建一个`/migrations`目录



然后生成迁移脚本

```bash
$ flask db migrate -m "users table"
```

该选项给出的注释**-m**是可选的，它只是向迁移添加一个简短的描述性文本。

对于User上面的模型，数据库中对应的表将被命名为user。对于AddressAndPhone模型类，该表将被命名为address_and_phone。如果您更喜欢选择自己的表名称，则可以**\_\_tablename\_\_**向模型类添加一个名为 name 的属性，并将其设置为所需的字符串名称。

将更改应用到数据库

```bash
 $ flask db upgrade
```

执行后会添加一个`app.db`文件，即 SQLite 数据库

## 数据库关系

![ch04-users-posts](Note_asset/ch04-users-posts.png)

修改`app/models.py`

```python
from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    posts: so.WriteOnlyMapped['Post'] = so.relationship(
        back_populates='author')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    # 使用时间戳，这样显示的时间就会因为用户而改变
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)

    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self):
        return '<Post {}>'.format(self.body)
```

这样post中的user_id就和uer中的id连接起来了

然后更新迁移脚本和重新运用

```bash
$ flask db migrate -m "posts table"
$ flask db upgrade
```

## 数据库使用示例

向数据库写入一些数据

```python
>>> from app import app, db
>>> from app.models import User, Post
>>> import sqlalchemy as sa
```

了让 Flask 及其扩展能够访问 Flask 应用程序而不必将其**app**作为参数传递到每个函数中，必须创建并推送*应用程序上下文*

```python
>>> app.app_context().push()
```

然后创建用户

```python
>>> u = User(username='john', email='john@example.com')
>>> db.session.add(u)
>>> db.session.commit()
```

对数据库的更改是在数据库会话的上下文中完成的，可以通过**db.session.**多个更改可以累积在一个会话中，一旦注册了所有更改，您就可以发出一个**db.session.commit()**，它以原子方式写入所有更改。如果在处理会话时的任何时候出现错误，则调用**db.session.rollback()**将中止会话并删除其中存储的任何更改。要记住的重要一点是，仅当使用 发出提交时，更改才会写入数据库**db.session.commit()**。会话保证数据库永远不会处于不一致的状态。  您是否想知道所有这些数据库操作如何知道要使用哪个数据库？上面推送的应用程序上下文允许 **Flask-SQLAlchemy** 访问 Flask 应用程序实例，app而无需将其作为参数接收。该扩展在**app.config**字典中查找**SQLALCHEMY_DATABASE_URI**包含数据库 URL 的条目

继续添加用户

```python
>>> u = User(username='susan', email='susan@example.com')
>>> db.session.add(u)
>>> db.session.commit()
```

查询用户

```python
>>> query = sa.select(User)
>>> users = db.session.scalars(query).all()
>>> users
[<User john>, <User susan>]
```

```python
>>> users = db.session.scalars(query)
>>> for u in users:
...     print(u.id, u.username)
...
1 john
2 susan
```

另一种查询方式

```python
>>> u = db.session.get(User, 1)
>>> u
<User john>
```

添加一篇博客

```python
>>> u = db.session.get(User, 1)
>>> p = Post(body='my first post!', author=u)
>>> db.session.add(p)
>>> db.session.commit()
```

其他一些查询方法

```python
>>> # 获取一个用户所有的博客
>>> u = db.session.get(User, 1)
>>> u
<User john>
>>> query = u.posts.select()
>>> posts = db.session.scalars(query).all()
>>> posts
[<Post my first post!>]

>>> # 获取所有的博客
>>> query = sa.select(Post)
>>> posts = db.session.scalars(query)
>>> for p in posts:
...     print(p.id, p.author.username, p.body)
...
1 john my first post!

# 反字母顺序获取所有用户
>>> query = sa.select(User).order_by(User.username.desc())
>>> db.session.scalars(query).all()
[<User susan>, <User john>]

# 获取所有开头字母含有s的用户
>>> query = sa.select(User).where(User.username.like('s%'))
>>> db.session.scalars(query).all()
[<User susan>]
```

删除测试数据

```bash
$ flask db downgrade base
$ flask db upgrade
```

第一个命令告诉 Flask-Migrate 以相反的顺序应用数据库迁移。当该downgrade命令未指定目标时，它会降级一个修订版。该base目标会导致所有迁移降级，直到数据库保持其初始状态，没有表。  该upgrade命令按正向顺序重新应用所有迁移。升级的默认目标是head，这是最近迁移的快捷方式。该命令有效地恢复了上面降级的表。由于数据库迁移不会保留数据库中存储的数据，因此降级然后升级会快速清空所有表。

## Flask Shell

之前使用了下面的命令传递了app

```python
>>> app.app_context().push()
```

但是这样太麻烦，可以使用flask提供的shell

```bash
(venv) $ flask shell
>>> app
<Flask 'app'>
```

重新配置下入口文件，让实例接收app这样就在开始注册好了这些实例

```bash
$ flask shell
>>> db
<SQLAlchemy sqlite:////home/miguel/microblog/app.db>
>>> User
<class 'app.models.User'>
>>> Post
<class 'app.models.Post'>
```

# 第五章 用户登入

