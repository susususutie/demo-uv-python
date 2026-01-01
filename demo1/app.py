from flask import Flask, jsonify, request

app = Flask(__name__)

# 配置JSON编码，支持中文显示
app.json.ensure_ascii = False

# 内存中的数据存储
users = [
    {"id": 1, "name": "张三", "email": "zhangsan@example.com"},
    {"id": 2, "name": "李四", "email": "lisi@example.com"},
]


@app.route("/")
def hello():
    return jsonify({"message": "Hello, Flask API!", "version": "1.0"})


@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((user for user in users if user["id"] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "用户不存在"}), 404


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "缺少必要字段: name 和 email"}), 400

    new_user = {"id": len(users) + 1, "name": data["name"], "email": data["email"]}
    users.append(new_user)
    return jsonify(new_user), 200


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = next((user for user in users if user["id"] == user_id), None)
    if not user:
        return jsonify({"error": "用户不存在"}), 404

    data = request.get_json()
    if "name" in data:
        user["name"] = data["name"]
    if "email" in data:
        user["email"] = data["email"]

    return jsonify(user)


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    global users
    user = next((user for user in users if user["id"] == user_id), None)
    if not user:
        return jsonify({"error": "用户不存在"}), 404

    users = [user for user in users if user["id"] != user_id]
    return jsonify({"message": "用户删除成功"}), 200


if __name__ == "__main__":
    app.run(debug=True)
