from datetime import datetime
from app.extentions import db
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Task(db.Model):
    __tablename__ = "tasks"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title: str = db.Column(db.String(255), nullable=False)
    description: str = db.Column(db.Text, nullable=True)
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at: datetime = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    is_completed: bool = db.Column(db.Boolean, default=False)
    user_id: int = db.Column(db.Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", backref="tasks")

    def __repr__(self):
        return f"<Task {self.title} (User: {self.user_id})>"
