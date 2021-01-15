from db import db

class CourseModel(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    grades = db.relationship("GradeModel", lazy='dynamic')

    def __init__(self, name, teacher_id):
        self.name = name
        self.teacher_id = teacher_id

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'teacher_id': self.teacher_id
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