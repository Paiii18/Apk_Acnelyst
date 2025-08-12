# app/routes/admin/routes.py
from flask import render_template, redirect, url_for, flash
from flask_login import current_user
from . import admin_bp
from .forms import EmptyForm
from app.decorators import admin_required
from app.extensions import db
from app.models.user import User
from app.models.prediction import Prediction

@admin_bp.route("/")
@admin_required
def index():
    return redirect(url_for("admin.users_list"))

@admin_bp.route("/users")
@admin_required
def users_list():
    users = User.query.order_by(User.id.asc()).all()
    form = EmptyForm()
    return render_template("admin/users.html", users=users, form=form, title="Kelola Pengguna")

@admin_bp.route("/users/<int:user_id>/promote", methods=["POST"])
@admin_required
def promote_user(user_id):
    form = EmptyForm()
    if form.validate_on_submit():
        u = User.query.get_or_404(user_id)
        if u.is_admin:
            flash("Pengguna ini sudah admin.", "warning")
        else:
            u.is_admin = True
            db.session.commit()
            flash(f"{u.email} sekarang admin.", "success")
    return redirect(url_for("admin.users_list"))

@admin_bp.route("/users/<int:user_id>/demote", methods=["POST"])
@admin_required
def demote_user(user_id):
    form = EmptyForm()
    if form.validate_on_submit():
        u = User.query.get_or_404(user_id)
        if u.id == current_user.id:
            flash("Tidak bisa menurunkan role diri sendiri.", "warning")
        elif not u.is_admin:
            flash("Pengguna ini bukan admin.", "warning")
        else:
            u.is_admin = False
            db.session.commit()
            flash(f"{u.email} bukan admin lagi.", "info")
    return redirect(url_for("admin.users_list"))

@admin_bp.route("/users/<int:user_id>/delete", methods=["POST"])
@admin_required
def delete_user(user_id):
    form = EmptyForm()
    if form.validate_on_submit():
        u = User.query.get_or_404(user_id)
        if u.id == current_user.id:
            flash("Tidak bisa menghapus akun sendiri.", "warning")
        else:
            db.session.delete(u)
            db.session.commit()
            flash(f"Pengguna {u.email} dihapus.", "danger")
    return redirect(url_for("admin.users_list"))

@admin_bp.route("/predictions")
@admin_required
def predictions_list():
    preds = Prediction.query.order_by(Prediction.id.desc()).all()
    form = EmptyForm()
    return render_template("admin/predictions.html", preds=preds, form=form, title="Riwayat Prediksi")


@admin_bp.route("/predictions/<int:pid>/delete", methods=["POST"])
@admin_required
def predictions_delete(pid):
    p = Prediction.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    flash("Riwayat dihapus.", "info")
    return redirect(url_for("admin.predictions_list"))

@admin_bp.route("/ping")
def ping():
    return "admin ok"
