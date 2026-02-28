"""Demo3 响应函数测试。

测试各种响应辅助函数。
"""

import pytest
from app.responses import success, created, paginated, deleted, no_content, error


def test_success_basic(app):
    """测试基础成功响应。"""
    with app.app_context():
        response = success(data={"id": 1})
        assert response[1] == 200
        data = response[0].get_json()
        assert data["message"] == "操作成功"
        assert data["data"]["id"] == 1


def test_success_with_message(app):
    """测试带自定义消息的成功响应。"""
    with app.app_context():
        response = success(data={"id": 1}, message="Custom message")
        data = response[0].get_json()
        assert data["message"] == "Custom message"


def test_success_no_data(app):
    """测试无数据的成功响应。"""
    with app.app_context():
        response = success()
        data = response[0].get_json()
        assert "data" not in data


def test_created(app):
    """测试创建成功响应。"""
    with app.app_context():
        response = created({"id": 1, "name": "Test"})
        assert response[1] == 201
        data = response[0].get_json()
        assert data["data"]["name"] == "Test"
        assert data["message"] == "创建成功"


def test_paginated(app):
    """测试分页响应。"""
    with app.app_context():
        items = [{"id": 1}, {"id": 2}]
        pagination = {"page": 1, "per_page": 10, "total": 2, "pages": 1, "has_prev": False, "has_next": False}
        response = paginated(items, pagination)

        # paginated 返回单个 Response 对象
        data = response.get_json()
        assert data["message"] == "获取成功"
        assert data["list"] == items
        assert data["pagination"] == pagination


def test_deleted(app):
    """测试删除成功响应。"""
    with app.app_context():
        response = deleted()
        assert response[1] == 200
        data = response[0].get_json()
        assert data["message"] == "删除成功"


def test_deleted_custom_message(app):
    """测试带自定义消息的删除响应。"""
    with app.app_context():
        response = deleted("User deleted")
        data = response[0].get_json()
        assert data["message"] == "User deleted"


def test_no_content(app):
    """测试无内容响应。"""
    with app.app_context():
        response = no_content()
        assert response[1] == 204
        assert response[0] == ""


def test_error_basic(app):
    """测试基础错误响应。"""
    with app.app_context():
        response = error("Something went wrong")
        assert response[1] == 400
        data = response[0].get_json()
        assert data["error"]["message"] == "Something went wrong"
        assert data["error"]["code"] == "ERROR"


def test_error_with_details(app):
    """测试带详情的错误响应。"""
    with app.app_context():
        response = error(
            "Validation failed",
            code="VALIDATION_ERROR",
            status_code=422,
            details={"field": "email"},
        )
        assert response[1] == 422
        data = response[0].get_json()
        assert data["error"]["code"] == "VALIDATION_ERROR"
        assert data["error"]["details"]["field"] == "email"
