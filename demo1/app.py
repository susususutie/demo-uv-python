"""
Demo1: 基础 Flask API 示例

本模块演示一个最简化的 Flask REST API 实现，使用内存存储数据。
适合初学者理解 Flask 的基本概念：路由、请求处理和 JSON 响应。

主要特性：
    - 单文件应用结构
    - 内存数据存储（无数据库依赖）
    - 基础 CRUD 操作
    - RESTful API 设计

运行方式：
    uv run demo1/app.py

访问地址：
    http://127.0.0.1:3000
"""

from typing import Any, Optional
from flask import Flask, jsonify, request, Response

# 创建 Flask 应用实例
app = Flask(__name__)

# 配置 JSON 编码，确保中文字符正确显示
app.json.ensure_ascii = False

# =============================================================================
# 数据存储（内存中）
# =============================================================================

# 初始化用户数据
_users: list[dict[str, Any]] = [
    {"id": 1, "name": "张三", "email": "zhangsan@example.com"},
    {"id": 2, "name": "李四", "email": "lisi@example.com"},
]

# 用户 ID 计数器，用于创建新用户时生成唯一 ID
_user_id_counter: int = len(_users)


# =============================================================================
# 辅助函数
# =============================================================================


def _find_user_by_id(user_id: int) -> Optional[dict[str, Any]]:
    """根据 ID 查找用户。

    Args:
        user_id: 用户唯一标识符

    Returns:
        找到的用户数据字典，未找到则返回 None
    """
    return next((user for user in _users if user["id"] == user_id), None)


def _generate_user_id() -> int:
    """生成新的用户 ID。

    Returns:
        新的唯一用户 ID
    """
    global _user_id_counter
    _user_id_counter += 1
    return _user_id_counter


# =============================================================================
# 路由定义
# =============================================================================


@app.route("/")
def hello() -> Response:
    """API 首页，返回基本信息。

    Returns:
        JSON 格式的 API 信息
    """
    return jsonify(
        {"message": "Hello, Flask API!", "version": "1.0", "demo": "基础内存存储版 API"}
    )


@app.route("/users", methods=["GET"])
def get_users() -> Response:
    """获取所有用户列表。

    Returns:
        包含所有用户数据的 JSON 数组
    """
    return jsonify(_users)


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id: int) -> Response:
    """获取指定 ID 的用户详情。

    Args:
        user_id: 用户唯一标识符（URL 参数）

    Returns:
        用户详情数据，未找到时返回 404 错误
    """
    user = _find_user_by_id(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "用户不存在"}), 404


@app.route("/users", methods=["POST"])
def create_user() -> Response:
    """创建新用户。

    请求体格式：
        {
            "name": "用户名",
            "email": "邮箱地址"
        }

    Returns:
        201: 创建成功，返回新用户数据
        400: 请求数据无效或缺少必填字段
    """
    data: Optional[dict[str, Any]] = request.get_json()

    # 验证请求数据
    if not data:
        return jsonify({"error": "请求体不能为空，需要提供 JSON 数据"}), 400

    if "name" not in data or "email" not in data:
        return jsonify({"error": "缺少必要字段: name 和 email"}), 400

    # 创建新用户
    new_user = {"id": _generate_user_id(), "name": data["name"], "email": data["email"]}
    _users.append(new_user)

    return jsonify(new_user), 201


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id: int) -> Response:
    """更新指定用户的信息。

    Args:
        user_id: 要更新的用户 ID

    请求体格式：
        {
            "name": "新用户名（可选）",
            "email": "新邮箱（可选）"
        }

    Returns:
        200: 更新成功，返回更新后的用户数据
        404: 用户不存在
        400: 请求数据无效
    """
    user = _find_user_by_id(user_id)
    if not user:
        return jsonify({"error": "用户不存在"}), 404

    data: Optional[dict[str, Any]] = request.get_json()
    if not data:
        return jsonify({"error": "请求体不能为空"}), 400

    # 更新提供的字段
    if "name" in data:
        user["name"] = data["name"]
    if "email" in data:
        user["email"] = data["email"]

    return jsonify(user)


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int) -> Response:
    """删除指定用户。

    Args:
        user_id: 要删除的用户 ID

    Returns:
        200: 删除成功
        404: 用户不存在
    """
    global _users

    user = _find_user_by_id(user_id)
    if not user:
        return jsonify({"error": "用户不存在"}), 404

    # 过滤掉要删除的用户
    _users = [u for u in _users if u["id"] != user_id]

    return jsonify({"message": "用户删除成功"}), 200


# =============================================================================
# 错误处理
# =============================================================================


@app.errorhandler(404)
def not_found(error) -> Response:
    """处理 404 错误。

    Returns:
        JSON 格式的错误信息
    """
    return jsonify({"error": "请求的接口不存在"}), 404


@app.errorhandler(405)
def method_not_allowed(error) -> Response:
    """处理 405 错误（请求方法不允许）。

    Returns:
        JSON 格式的错误信息
    """
    return jsonify({"error": "请求方法不允许"}), 405


@app.errorhandler(500)
def internal_error(error) -> Response:
    """处理 500 服务器内部错误。

    Returns:
        JSON 格式的错误信息
    """
    return jsonify({"error": "服务器内部错误"}), 500


# =============================================================================
# 应用入口
# =============================================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
