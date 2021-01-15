from db import db

class GradeModel(db.Model):
    __tablename__ = 'grades'

    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.Integer)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))

    def __init__(self, grade, course_id, student_id):
        self.grade = grade
        self.course_id = course_id
        self.student_id = student_id

    def json(self):
        return {
            'id': self.id,
            'grade': self.grade,
            'course_id': self.course_id,
            'student_id': self.student_id
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()