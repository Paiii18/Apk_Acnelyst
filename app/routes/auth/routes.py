from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import auth_bp
from .forms import LoginForm, RegisterForm
from ...extensions import db
from ...models.user import User

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next") or url_for("main.dashboard")
            flash("Login berhasil.", "success")
            return redirect(next_page)
        flash("Email atau password salah.", "danger")
    return render_template("auth/login.html", form=form, title="Login")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data.lower()).first():
            flash("Email sudah terdaftar.", "warning")
        else:
            user = User(
                name=form.name.data,
                email=form.email.data.lower(),
                is_admin=False
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Registrasi berhasil. Silakan login.", "success")
            return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form, title="Registrasi")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Anda telah logout.", "info")
    return redirect(url_for("auth.login"))

