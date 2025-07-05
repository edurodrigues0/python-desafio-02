from repository.database import db

class Diet(db.Model):
    __tablename__ = 'diets'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    on_diet = db.Column(db.Boolean, default=True, nullable=False)
    date_hour = db.Column(db.DateTime, nullable=False)
    # Foreign key to the User model
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('diets', lazy=True))

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'on_diet': self.on_diet,
            'user_id': self.user_id,
            'date_hour': self.date_hour.isoformat(),
            'created_at': self.created_at.isoformat(),
        }

    def __repr__(self):
        return f'<Diet {self.name}>'