from flask_restful import Resource, reqparse
from models.student import StudentModel

class Student(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('first_name',
                        required=True,
                        help="Student must have a firts name!"
                        )
    parser.add_argument('last_name',
                        required=True,
                        help="Student must have a last name!"
                        )
    parser.add_argument('email',
                        required=True,
                        help="Student must have an email!"
                        )
    
    def get(self, id):
        student = StudentModel.query.get(id)
        if student:
            return student.json()
        return {'message': 'Student not found'}, 404
    
    def put(self, id):
        data = self.parser.parse_args()
        student = StudentModel.query.get(id)

        if student:
            student.first_name = data['first_name']
            student.last_name = data['last_name']
            student.email = data['email']
        else:
            return {"message": "Student with id {} not exists".format(id)}

        student.save_to_db()

        return student.json()

    def delete(self, id):
        student = StudentModel.query.get(id)
        if student:
            student.delete_from_db()
            return {'message': "Student with Id: {} deleted.".format(id)}
        return {'message': "Student with a Id: {} not exists".format(id)}, 404

class StudentList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('first_name',
                        required=True,
                        help="Student must have a firts name!"
                        )
    parser.add_argument('last_name',
                        required=True,
                        help="Student must have a last name!"
                        )
    parser.add_argument('email',
                        required=True,
                        help="Student must have an email!"
                        )

    def get(self):
        students = [student.json() for student in StudentModel.find_all()]
        return {'students': students}, 200
    
    def post(self):
        data = self.parser.parse_args()

        if StudentModel.query.filter_by(first_name=data['first_name']).first() and StudentModel.query.filter_by(last_name=data['last_name']).first():
            return {'message': "Student with this first name ans last already exists."}, 400

        student = StudentModel(**data)

        try:
            student.save_to_db()
        except:
            return {"message": "An error occurred while inserting the student."}, 500

        return student.json(), 201