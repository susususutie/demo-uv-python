#!/usr/bin/env uv run
# /// script
# dependencies = ["httpx"]
# ///
"""
批量给本地 3000 端口服务灌数据
用法：
    uv run batch-insert.py --users 20 --posts 100
"""
import argparse, random, sys
import httpx

BASE = "http://127.0.0.1:3000"
USER_ENDPOINT = f"{BASE}/api/users"
POST_ENDPOINT = f"{BASE}/api/posts"


def create_user(client: httpx.Client, idx: int):
    payload = {"username": f"用户{idx}", "email": f"user{idx}@example.com"}
    r = client.post(USER_ENDPOINT, json=payload)
    r.raise_for_status()
    return r.json()["id"]  # 返回 {"id": 1}


def create_post(client: httpx.Client, user_id: int, idx: int):
    payload = {
        "user_id": user_id,
        "title": f"文章标题-{user_id}-{idx}",
        "content": f"这是用户 {user_id} 的第 {idx} 篇测试文章内容。",
    }
    r = client.post(POST_ENDPOINT, json=payload)
    r.raise_for_status()


def main():
    parser = argparse.ArgumentParser(description="批量插入用户和文章")
    parser.add_argument("--users", type=int, default=23, help="用户数量")
    parser.add_argument("--posts", type=int, default=45, help="每个用户的文章数量")
    args = parser.parse_args()

    with httpx.Client(timeout=30) as client:
        # 1. 创建用户
        print("开始创建用户 …")
        user_ids = []
        for i in range(1, args.users + 1):
            uid = create_user(client, i)
            user_ids.append(uid)
        print(f"已创建 {len(user_ids)} 个用户")

        # 2. 为每个用户创建文章
        total_posts = 0
        for uid in user_ids:
            for j in range(1, args.posts + 1):
                create_post(client, uid, j)
                total_posts += 1
            print(f"用户 {uid} 已插入 {args.posts} 篇文章")
        print(f"全部完成！共 {args.users} 用户，{total_posts} 篇文章。")


if __name__ == "__main__":
    try:
        main()
    except httpx.HTTPError as e:
        print("接口调用失败：", e, file=sys.stderr)
        sys.exit(1)
