import uuid

from repository.database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
  __tablename__ = 'users'

  id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
  name = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(), nullable=False)
  created_at = db.Column(db.DateTime, server_default=db.func.now())
  updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

  def to_dict(self):
    return {
      'id': self.id,
      'name': self.name,
      'email': self.email,
      'created_at': self.created_at.isoformat(),
      'updated_at': self.updated_at.isoformat()
    }