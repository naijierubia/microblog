from app import app
from app import db

import sqlalchemy as sa
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from urllib.parse import urlsplit


@app.route("/")
@app.route("/index")
@login_required
def index():
    return render_template("index.html", title="Home")


# 定义一个路由，当访问/login时，执行下面的login函数
@app.route("/login", methods=["GET", "POST"])
def login():
    # 如果当前用户已经认证，则重定向到index页面
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    # 实例化一个LoginForm对象
    form = LoginForm()
    # 如果表单提交成功，则执行下面的代码
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        # 如果用户不存在或密码不正确，则显示错误提示
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        # 否则，登录用户
        login_user(user, remember=form.remember_me.data)
        # 获取next参数，如果存在，且参数合法，则跳转到next参数指定的页面，否则跳转到index页面
        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    # 否则，渲染login.html页面，并将form对象传递给页面
    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)
