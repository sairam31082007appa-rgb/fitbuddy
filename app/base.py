from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import DATABASE_URL


# SQLite needs this option when used with FastAPI
connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {
        "check_same_thread": False
    }


engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)


SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        String(100),
        unique=True,
        index=True,
        nullable=False
    )

    username = Column(
        String(100),
        nullable=False
    )

    age = Column(
        Integer,
        nullable=False
    )

    weight = Column(
        Float,
        nullable=False
    )

    goal = Column(
        String(100),
        nullable=False
    )

    intensity = Column(
        String(50),
        nullable=False
    )

    original_plan = Column(
        Text,
        nullable=False
    )

    updated_plan = Column(
        Text,
        nullable=True
    )

    nutrition_tip = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


def init_db():
    """
    Create database tables if they do not exist.
    """
    Base.metadata.create_all(
        bind=engine
    )


def save_user(data):
    """
    Save a new user.

    If user_id already exists, return the existing user.
    """

    db = SessionLocal()

    try:
        existing_user = (
            db.query(User)
            .filter(User.user_id == data["user_id"])
            .first()
        )

        if existing_user:
            return existing_user

        user = User(**data)

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    finally:
        db.close()


def get_user(user_id):
    """
    Get one user by user_id.
    """

    db = SessionLocal()

    try:
        return (
            db.query(User)
            .filter(User.user_id == user_id)
            .first()
        )

    finally:
        db.close()


def update_plan(
    user_id,
    updated_plan
):
    """
    Store the revised AI-generated plan.
    """

    db = SessionLocal()

    try:
        user = (
            db.query(User)
            .filter(User.user_id == user_id)
            .first()
        )

        if not user:
            return None

        user.updated_plan = updated_plan

        db.commit()
        db.refresh(user)

        return user

    finally:
        db.close()


def get_all_users():
    """
    Return all users.
    """

    db = SessionLocal()

    try:
        return (
            db.query(User)
            .order_by(User.created_at.desc())
            .all()
        )

    finally:
        db.close()


def delete_user(user_id):
    """
    Delete a user.
    """

    db = SessionLocal()

    try:
        user = (
            db.query(User)
            .filter(User.user_id == user_id)
            .first()
        )

        if user:
            db.delete(user)
            db.commit()
            return True

        return False

    finally:
        db.close()