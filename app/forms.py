from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
import sqlalchemy as sa
from app import db
from app.models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    #   定义一个注册表单类，继承自FlaskForm
    username = StringField("Username", validators=[DataRequired()])
    #   定义一个用户名字段，并添加数据必需的验证器
    email = StringField("Email", validators=[DataRequired(), Email()])
    #   定义一个邮箱字段，并添加数据必需的验证器和电子邮件的验证器
    password = PasswordField("Password", validators=[DataRequired()])
    #   定义一个密码字段，并添加数据必需的验证器
    password2 = PasswordField(
        #   定义一个重复密码字段，并添加数据必需的验证器和EqualTo验证器，用于验证密码和重复密码是否一致
        "Repeat Password",
        validators=[DataRequired(), EqualTo("password")],
    )
    submit = SubmitField("Register")
    #   定义一个提交字段

    def validate_username(self, username):
        #   定义一个验证用户名的函数，用于检查数据库中是否存在同名的用户
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            #   如果存在同名用户，则抛出异常
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        #   定义一个验证邮箱的函数，用于检查数据库中是否存在同名的用户
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            #   如果存在同名用户，则抛出异常
            raise ValidationError("Please use a different email address.")


class EditProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    about_me = TextAreaField("About me", validators=[Length(min=0, max=140)])
    submit = SubmitField("Submit")
