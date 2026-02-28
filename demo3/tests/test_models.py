from app.models import User, Post, Tag
from sqlalchemy.exc import IntegrityError
import pytest


def test_user_creation(db):
    user = User(username="testuser", email="test@example.com")
    db.session.add(user)
    db.session.commit()

    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"


def test_user_unique_constraints(db):
    user1 = User(username="user1", email="u1@example.com")
    db.session.add(user1)
    db.session.commit()

    # Duplicate username
    user2 = User(username="user1", email="u2@example.com")
    db.session.add(user2)
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()

    # Duplicate email
    user3 = User(username="user2", email="u1@example.com")
    db.session.add(user3)
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()


def test_user_repr(db):
    """测试User模型的字符串表示。"""
    user = User(username="testrepr", email="repr@example.com")
    db.session.add(user)
    db.session.commit()

    repr_str = repr(user)
    assert "User" in repr_str
    assert "testrepr" in repr_str


def test_user_to_dict(db):
    """测试User模型的to_dict方法。"""
    user = User(username="dictuser", email="dict@example.com")
    db.session.add(user)
    db.session.commit()

    user_dict = user.to_dict()
    assert user_dict["id"] == user.id
    assert user_dict["username"] == "dictuser"
    assert user_dict["email"] == "dict@example.com"
    assert "created_at" in user_dict
    assert "updated_at" in user_dict


def test_user_get_post_count(db):
    """测试User模型的get_post_count方法。"""
    user = User(username="countuser", email="count@example.com")
    db.session.add(user)
    db.session.commit()

    # 初始文章数应为0
    assert user.get_post_count() == 0

    # 创建文章
    post1 = Post(title="Post 1", content="Content 1", user_id=user.id)
    post2 = Post(title="Post 2", content="Content 2", user_id=user.id)
    db.session.add(post1)
    db.session.add(post2)
    db.session.commit()

    # 刷新用户对象以获取最新计数
    db.session.refresh(user)
    assert user.get_post_count() == 2


def test_tag_creation(db):
    tag = Tag(name="python")
    db.session.add(tag)
    db.session.commit()

    assert tag.id is not None
    assert tag.name == "python"


def test_tag_repr(db):
    """测试Tag模型的字符串表示。"""
    tag = Tag(name="testtag")
    db.session.add(tag)
    db.session.commit()

    repr_str = repr(tag)
    assert "Tag" in repr_str
    assert "testtag" in repr_str


def test_tag_to_dict(db):
    """测试Tag模型的to_dict方法。"""
    tag = Tag(name="dicttag")
    db.session.add(tag)
    db.session.commit()

    tag_dict = tag.to_dict()
    assert tag_dict["id"] == tag.id
    assert tag_dict["name"] == "dicttag"
    assert "created_at" in tag_dict
    assert "updated_at" in tag_dict


def test_post_creation(db):
    user = User(username="author", email="author@example.com")
    db.session.add(user)
    db.session.commit()

    post = Post(title="My Post", content="Content", user_id=user.id)
    db.session.add(post)
    db.session.commit()

    assert post.id is not None
    assert post.author == user


def test_post_repr(db):
    """测试Post模型的字符串表示。"""
    user = User(username="postauthor", email="post@example.com")
    db.session.add(user)
    db.session.commit()

    post = Post(title="Test Post", content="Content", user_id=user.id)
    db.session.add(post)
    db.session.commit()

    repr_str = repr(post)
    assert "Post" in repr_str
    assert "Test Post" in repr_str


def test_post_to_dict(db):
    """测试Post模型的to_dict方法。"""
    user = User(username="postdictuser", email="postdict@example.com")
    db.session.add(user)
    db.session.commit()

    post = Post(title="Dict Post", content="Content", user_id=user.id)
    db.session.add(post)
    db.session.commit()

    post_dict = post.to_dict()
    assert post_dict["id"] == post.id
    assert post_dict["title"] == "Dict Post"
    assert post_dict["content"] == "Content"
    assert post_dict["user_id"] == user.id
    assert "created_at" in post_dict
    assert "updated_at" in post_dict


def test_post_publish_unpublish(db):
    """测试Post模型的publish和unpublish方法。"""
    user = User(username="pubuser", email="pub@example.com")
    db.session.add(user)
    db.session.commit()

    post = Post(title="Publish Test", content="Content", user_id=user.id, published=False)
    db.session.add(post)
    db.session.commit()

    assert post.published is False

    post.publish()
    assert post.published is True

    post.unpublish()
    assert post.published is False
