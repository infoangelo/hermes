from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import app

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    xp = db.relationship('Exp', backref='users', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username


class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    content = db.Column(db.String(1200), nullable=False)
    exercise = db.Column(db.String(120))
    input_exercise = db.Column(db.String(120))
    output_exercise = db.Column(db.String(120))
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    exp_value = db.Column(db.String(15))

    def __repr__(self):
        return '<Lesson %r>' % self.title


class Exp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    exec_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    lesson_value = db.Column(db.Integer, nullable=False)
    lesson_title = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Exp %r>' % self.lesson_value

