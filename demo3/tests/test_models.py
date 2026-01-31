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

def test_tag_creation(db):
    tag = Tag(name="python")
    db.session.add(tag)
    db.session.commit()
    
    assert tag.id is not None
    assert tag.name == "python"

def test_post_creation(db):
    user = User(username="author", email="author@example.com")
    db.session.add(user)
    db.session.commit()
    
    post = Post(title="My Post", content="Content", user_id=user.id)
    db.session.add(post)
    db.session.commit()
    
    assert post.id is not None
    assert post.author == user
