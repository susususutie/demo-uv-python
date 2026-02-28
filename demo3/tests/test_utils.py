"""Demo3 工具函数测试。

测试分页、过滤、排序等功能。
"""

import pytest
from app.utils import get_page_params, to_pagination_dict, apply_filter, apply_sort


class MockParams:
    """模拟查询参数字典。"""

    def __init__(self, data):
        self._data = data

    def get(self, key, default=None):
        return self._data.get(key, default)


def test_get_page_params_defaults():
    """测试分页参数默认值。"""
    params = MockParams({})
    result = get_page_params(params=params)

    assert result["page"] == 1
    assert result["per_page"] == 10


def test_get_page_params_custom():
    """测试自定义分页参数。"""
    params = MockParams({"page": "3", "per_page": "25"})
    result = get_page_params(params=params)

    assert result["page"] == 3
    assert result["per_page"] == 25


def test_get_page_params_invalid():
    """测试无效分页参数。"""
    params = MockParams({"page": "invalid", "per_page": "invalid"})
    result = get_page_params(params=params)

    # 应该使用默认值
    assert result["page"] == 1
    assert result["per_page"] == 10


def test_get_page_params_bounds():
    """测试分页参数边界值。"""
    # 测试 page < 1
    params = MockParams({"page": "0"})
    result = get_page_params(params=params)
    assert result["page"] == 1

    # 测试 per_page > max
    params = MockParams({"per_page": "200"})
    result = get_page_params(max_per_page=100, params=params)
    assert result["per_page"] == 100

    # 测试 per_page < 1
    params = MockParams({"per_page": "0"})
    result = get_page_params(params=params)
    assert result["per_page"] == 1


def test_get_page_params_none_params(app):
    """测试使用 request.args 当 params 为 None。"""
    # 在应用上下文中测试，但不传递params参数
    with app.test_request_context("/?page=2&per_page=15"):
        result = get_page_params(max_per_page=50, default_per_page=5)
        assert result["page"] == 2
        assert result["per_page"] == 15


def test_to_pagination_dict():
    """测试分页元信息转换。"""
    class MockPagination:
        page = 2
        per_page = 10
        total = 50
        pages = 5
        has_prev = True
        has_next = True

    pagination = MockPagination()
    result = to_pagination_dict(pagination)

    assert result["page"] == 2
    assert result["per_page"] == 10
    assert result["total"] == 50
    assert result["pages"] == 5
    assert result["has_prev"] is True
    assert result["has_next"] is True
