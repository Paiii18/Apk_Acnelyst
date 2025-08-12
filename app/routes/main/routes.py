from flask import render_template
from flask_login import login_required, current_user
from . import main_bp
from flask import send_from_directory, abort
from pathlib import Path

@main_bp.route("/")
def index():
    return render_template("main/index.html", title="Home")

@main_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("main/dashboard.html", title="Dashboard")

@main_bp.route("/uploads/<path:filename>")
@login_required
def uploaded_file(filename):
    upload_folder = Path(__file__).resolve().parents[2] / "uploads"
    # Optional: validasi path sederhana
    if ".." in filename or filename.startswith("/"):
        abort(400)
    return send_from_directory(upload_folder, filename)