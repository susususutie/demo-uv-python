"""Demo3 统一错误处理模块。

提供应用级别的异常处理和标准化错误响应。
"""

from typing import Any
from flask import jsonify, Response
from marshmallow import ValidationError as MarshmallowValidationError
from sqlalchemy.exc import IntegrityError

from app.extensions import db


class APIError(Exception):
    """API 错误基类。

    Attributes:
        code: 错误代码
        message: 错误消息
        status_code: HTTP 状态码
        details: 额外错误详情
    """

    def __init__(
        self,
        message: str,
        code: str = "API_ERROR",
        status_code: int = 400,
        details: dict[str, Any] | None = None,
    ):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}

    def to_dict(self) -> dict[str, Any]:
        """转换为字典格式。"""
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                **({"details": self.details} if self.details else {}),
            }
        }


class NotFoundError(APIError):
    """资源不存在错误。"""

    def __init__(self, resource: str = "资源"):
        super().__init__(
            message=f"{resource}不存在", code="RESOURCE_NOT_FOUND", status_code=404
        )


class ValidationErrorAPI(APIError):
    """数据验证错误。"""

    def __init__(self, message: str, details: dict[str, Any] | None = None):
        super().__init__(
            message=message, code="VALIDATION_ERROR", status_code=400, details=details
        )


class DuplicateError(APIError):
    """数据重复错误。"""

    def __init__(self, field: str):
        super().__init__(
            message=f"{field}已存在", code="DUPLICATE_ERROR", status_code=409
        )


# =============================================================================
# 错误处理器注册
# =============================================================================


def register_error_handlers(app):
    """注册所有错误处理器到 Flask 应用。

    Args:
        app: Flask 应用实例
    """

    @app.errorhandler(APIError)
    def handle_api_error(error: APIError) -> Response:
        """处理自定义 API 错误。"""
        return jsonify(error.to_dict()), error.status_code

    @app.errorhandler(404)
    def handle_not_found(error) -> Response:
        """处理 404 错误。"""
        return (
            jsonify({"error": {"code": "NOT_FOUND", "message": "请求的接口不存在"}}),
            404,
        )

    @app.errorhandler(405)
    def handle_method_not_allowed(error) -> Response:
        """处理 405 错误。"""
        return (
            jsonify(
                {"error": {"code": "METHOD_NOT_ALLOWED", "message": "请求方法不允许"}}
            ),
            405,
        )

    @app.errorhandler(MarshmallowValidationError)
    def handle_validation_error(error: MarshmallowValidationError) -> Response:
        """处理 Marshmallow 验证错误。"""
        return (
            jsonify(
                {
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "数据验证失败",
                        "details": error.messages,
                    }
                }
            ),
            400,
        )

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error: IntegrityError) -> Response:
        """处理数据库完整性错误。"""
        db.session.rollback()

        # 分析错误信息，返回更友好的提示
        error_str = str(error.orig).lower()

        if "unique" in error_str or "duplicate" in error_str:
            return (
                jsonify(
                    {
                        "error": {
                            "code": "DUPLICATE_ERROR",
                            "message": "数据已存在，违反唯一性约束",
                        }
                    }
                ),
                409,
            )

        if "foreign key" in error_str:
            return (
                jsonify(
                    {
                        "error": {
                            "code": "FOREIGN_KEY_ERROR",
                            "message": "关联的资源不存在",
                        }
                    }
                ),
                400,
            )

        return (
            jsonify({"error": {"code": "DATABASE_ERROR", "message": "数据库操作失败"}}),
            500,
        )

    @app.errorhandler(Exception)
    def handle_generic_error(error: Exception) -> Response:
        """处理未捕获的异常。"""
        db.session.rollback()

        # 生产环境不应暴露详细错误信息
        if app.config.get("DEBUG"):
            return (
                jsonify(
                    {
                        "error": {
                            "code": "INTERNAL_ERROR",
                            "message": str(error),
                            "type": type(error).__name__,
                        }
                    }
                ),
                500,
            )

        return (
            jsonify({"error": {"code": "INTERNAL_ERROR", "message": "服务器内部错误"}}),
            500,
        )
