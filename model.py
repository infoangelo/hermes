from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import PrimaryKeyConstraint

from app import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    register_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    exec_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    lesson_title = db.Column(db.String(120), nullable=False)
    lesson_value = db.Column(db.String(15), nullable=False)
    __table_args__ = (PrimaryKeyConstraint(user_id, lesson_id),
                      {})


class Attempts(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    exec_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)

