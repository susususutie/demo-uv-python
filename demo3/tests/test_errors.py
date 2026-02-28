"""Demo3 错误处理模块测试。

测试各种错误类和错误处理器。
"""

import pytest
from app.errors import (
    APIError,
    NotFoundError,
    ValidationErrorAPI,
    DuplicateError,
)


def test_api_error_basic():
    """测试基础API错误。"""
    error = APIError("Test message")
    assert error.message == "Test message"
    assert error.code == "API_ERROR"
    assert error.status_code == 400


def test_api_error_with_details():
    """测试带详情的API错误。"""
    error = APIError(
        "Validation failed",
        code="VALIDATION_FAILED",
        status_code=422,
        details={"field": "username", "reason": "too short"},
    )
    error_dict = error.to_dict()
    assert error_dict["error"]["message"] == "Validation failed"
    assert error_dict["error"]["code"] == "VALIDATION_FAILED"
    assert error_dict["error"]["details"]["field"] == "username"


def test_not_found_error():
    """测试资源不存在错误。"""
    error = NotFoundError("用户")
    assert error.message == "用户不存在"
    assert error.code == "RESOURCE_NOT_FOUND"
    assert error.status_code == 404


def test_not_found_error_default():
    """测试默认资源不存在错误。"""
    error = NotFoundError()
    assert error.message == "资源不存在"


def test_validation_error():
    """测试验证错误。"""
    error = ValidationErrorAPI("Invalid input", details={"email": "Invalid format"})
    assert error.message == "Invalid input"
    assert error.code == "VALIDATION_ERROR"
    assert error.status_code == 400
    assert error.details == {"email": "Invalid format"}


def test_duplicate_error():
    """测试重复错误。"""
    error = DuplicateError("用户名")
    assert error.message == "用户名已存在"
    assert error.code == "DUPLICATE_ERROR"
    assert error.status_code == 409


def test_error_handlers_registered(app):
    """测试错误处理器已注册。"""
    error_handlers = app.error_handler_spec

    # 检查各种错误处理器是否存在
    has_not_found = False
    has_method_not_allowed = False

    for key, spec in error_handlers.items():
        if isinstance(spec, dict):
            if 404 in spec:
                has_not_found = True
            if 405 in spec:
                has_method_not_allowed = True

    assert has_not_found, "404 错误处理器未注册"
    assert has_method_not_allowed, "405 错误处理器未注册"
