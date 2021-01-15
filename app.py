from flask import Flask
from flask_restful import Api

from db import db
from resources.course import Course, CourseList
from resources.grade import Grade, GradeList
from resources.student import Student, StudentList
from resources.teacher import Teacher, TeacherList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'kjfwkaj98ehriewubrewo78yr32iuyb'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Student, '/students/<int:id>')
api.add_resource(StudentList, '/students')
api.add_resource(Teacher, '/teachers/<int:id>')
api.add_resource(TeacherList, '/teachers')
api.add_resource(Grade, '/grades/<int:id>')
api.add_resource(GradeList, '/grades')
api.add_resource(Course, '/courses/<int:id>')
api.add_resource(CourseList, '/courses')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)