"""Demo3 统一响应格式模块。

提供标准化的 API 响应格式。
"""

from typing import Any
from flask import jsonify, Response


def success(
    data: Any = None, message: str = "操作成功", status_code: int = 200
) -> Response:
    """返回成功响应。

    Args:
        data: 响应数据
        message: 成功消息
        status_code: HTTP 状态码

    Returns:
        JSON 格式的成功响应
    """
    response = {"message": message}
    if data is not None:
        response["data"] = data
    return jsonify(response), status_code


def created(data: Any, message: str = "创建成功") -> Response:
    """返回创建成功响应。

    Args:
        data: 创建的资源数据
        message: 成功消息

    Returns:
        201 状态码的成功响应
    """
    return success(data, message, 201)


def paginated(
    items: list[Any], pagination: dict[str, Any], message: str = "获取成功"
) -> Response:
    """返回分页列表响应。

    Args:
        items: 数据列表
        pagination: 分页元信息
        message: 成功消息

    Returns:
        标准化的分页响应
    """
    return jsonify({"message": message, "list": items, "pagination": pagination})


def deleted(message: str = "删除成功") -> Response:
    """返回删除成功响应。

    Args:
        message: 删除成功消息

    Returns:
        200 状态码的删除成功响应
    """
    return success(message=message)


def no_content() -> Response:
    """返回无内容响应。

    Returns:
        204 状态码的空响应
    """
    return "", 204


def error(
    message: str,
    code: str = "ERROR",
    status_code: int = 400,
    details: dict[str, Any] | None = None,
) -> Response:
    """返回错误响应。

    Args:
        message: 错误消息
        code: 错误代码
        status_code: HTTP 状态码
        details: 额外错误详情

    Returns:
        JSON 格式的错误响应
    """
    response = {"error": {"code": code, "message": message}}
    if details:
        response["error"]["details"] = details
    return jsonify(response), status_code
