from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    remember = BooleanField("Ingat saya")
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    name = StringField("Nama", validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField("Konfirmasi Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Daftar")
