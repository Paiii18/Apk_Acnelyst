from flask import render_template
from flask_login import login_required, current_user
from . import main_bp

@main_bp.route("/")
def index():
    return render_template("main/index.html", title="Home")

@main_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("main/dashboard.html", title="Dashboard")
