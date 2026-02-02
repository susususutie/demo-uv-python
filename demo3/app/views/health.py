"""Demo3 健康检查视图模块。

提供服务健康状态监控接口。
"""

from datetime import datetime, timezone
from flask import Blueprint
from sqlalchemy import text

from app.extensions import db
from app.responses import success
from app.errors import APIError

bp = Blueprint("health", __name__, url_prefix="")


@bp.get("/health")
def health():
    """健康检查端点。

    检查服务状态和数据库连接。

    Returns:
        200: 服务正常
        500: 数据库连接异常
    """
    try:
        # 验证数据库连接
        db.session.execute(text("SELECT 1"))
        return success(
            {
                "status": "UP",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "database": "connected",
            }
        )
    except Exception as e:
        raise APIError(
            message=f"数据库连接失败: {str(e)}", code="DATABASE_ERROR", status_code=500
        )
