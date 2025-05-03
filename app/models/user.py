from app import db, bcrypt
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    role = db.Column(db.String(50), nullable=False, default='user')
    accounts = db.relationship('Account', backref='owner', lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = self.generate_password_hash(password)
    
    def check_password(self, password):
        try:
            return bcrypt.check_password_hash(self.password_hash, password)
        except ValueError:
            return False
    
    @staticmethod
    def generate_password_hash(password):
        try:
            return bcrypt.generate_password_hash(password).decode('utf-8')
        except ValueError as e:
            raise ValueError("Error generating password hash") from e
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at.isoformat(),
            'role': self.role,
            'accounts': [account.to_dict() for account in self.accounts]  # Assuming Account has a `to_dict` method
        }