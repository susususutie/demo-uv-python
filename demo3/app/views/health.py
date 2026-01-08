# app/views/health.py
from flask import Blueprint, jsonify
from app.extensions import db

bp = Blueprint("health", __name__, url_prefix="")


@bp.get("/health")
def health():
    # 顺手验证 DB 连通
    # db.session.execute("SELECT 1")
    return jsonify({"status": "UP"})
