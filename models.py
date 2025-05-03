from extensions import db

from datetime import datetime

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(4), nullable=True)
    added_date = db.Column(db.DateTime, nullable=True, default=None)
    student_teacher_name = db.Column(db.String(100), nullable=True)
    department_name = db.Column(db.String(100), nullable=True)
    college_name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    duration = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"<Book {self.title} by {self.author}>"
