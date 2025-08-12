from datetime import datetime
from ..extensions import db

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    filename = db.Column(db.String(255), nullable=False)
    label = db.Column(db.String(64), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    meta = db.Column(db.Text, nullable=True)  # opsional (simpen info tambahan)
