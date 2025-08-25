from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the database extension
db = SQLAlchemy()

# Define the Complaint model
class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Complaint {self.title}>'