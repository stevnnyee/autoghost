from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.orm import declarative_base
from configs.config import DATABASE_PATH

Base = declarative_base()


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    platform = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    niche = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class Trend(Base):
    __tablename__ = "trends"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    source = Column(String, nullable=False)
    niche = Column(String, nullable=False)
    score = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False)


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    trend_id = Column(Integer, ForeignKey("trends.id"), nullable=True)
    script = Column(Text, nullable=False)
    file_type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    audio_path = Column(String)
    video_path = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    uploaded_at = Column(DateTime)


class Analytics(Base):
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)
    views = Column(Integer, nullable=False, default=0)
    likes = Column(Integer, nullable=False, default=0)
    comments = Column(Integer, nullable=False, default=0)
    shares = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False)


class TrendingSound(Base):
    __tablename__ = "trending_sounds"

    id = Column(Integer, primary_key=True)
    sound_id = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False)
    vibe = Column(String, nullable=False)
    usage_count = Column(Integer, nullable=False)
    file_path = Column(String)
    created_at = Column(DateTime, nullable=False)


def init_db():
    engine = create_engine(f"sqlite:///{DATABASE_PATH}")
    Base.metadata.create_all(engine)