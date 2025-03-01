from app import db


class User(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(64), unique=True, nullable=False)
    password_hash: str = db.Column(db.String(256), nullable=False)

    def __repr__(self) -> str:
        return f"<User {self.username}"
