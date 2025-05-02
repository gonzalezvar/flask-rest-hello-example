from .database import db

student_course_association = db.Table(
    'student_course',
    db.Column('student_id', db.Integer, db.ForeignKey(
        'students.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey(
        'courses.id'), primary_key=True)
)