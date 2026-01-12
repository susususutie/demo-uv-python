# app/views/health.py
from flask import Blueprint, jsonify
from sqlalchemy import text
from app.extensions import db

bp = Blueprint("health", __name__, url_prefix="")


@bp.get("/health")
def health():
    # 验证 DB 连通, 若失败则抛出异常
    try:
        db.session.execute(text("SELECT 1"))
    except Exception as e:
        return jsonify({"status": "DOWN", "error": str(e)}), 500
    return jsonify({"status": "UP"})
