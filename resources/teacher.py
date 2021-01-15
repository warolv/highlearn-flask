from flask_restful import Resource, reqparse
from models.teacher import TeacherModel

class Teacher(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('first_name',
                        required=True,
                        help="Teacher must have a firts name!"
                        )
    parser.add_argument('last_name',
                        required=True,
                        help="Teacher must have a last name!"
                        )
    parser.add_argument('email',
                        required=True,
                        help="Teacher must have an email!"
                        )

    def get(self, id):
        teacher = TeacherModel.query.get(id)
        if teacher:
            return teacher.json()
        return {'message': 'Teacher not found'}, 404
    
    def put(self, id):
        data = self.parser.parse_args()
        teacher = TeacherModel.query.get(id)

        if teacher:
            teacher.first_name = data['first_name']
            teacher.last_name = data['last_name']
            teacher.email = data['email']
        else:
            return {"message": "Teacher with id {} not exists".format(id)}

        teacher.save_to_db()

        return teacher.json()

    def delete(self, id):
        teacher = TeacherModel.query.get(id)
        if teacher:
            teacher.delete_from_db()
            return {'message': "Teacher with Id: {} deleted.".format(id)}
        return {'message': "Teacher with a Id: {} not exists".format(id)}, 404

class TeacherList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('first_name',
                        required=True,
                        help="Teacher must have a firts name!"
                        )
    parser.add_argument('last_name',
                        required=True,
                        help="Teacher must have a last name!"
                        )
    parser.add_argument('email',
                        required=True,
                        help="Teacher must have an email!"
                        )

    def get(self):
        teachers = [teacher.json() for teacher in TeacherModel.find_all()]
        return {'teachers': teachers}, 200
    
    def post(self):
        data = self.parser.parse_args()

        if TeacherModel.query.filter_by(first_name=data['first_name']).first() and TeacherModel.query.filter_by(last_name=data['last_name']).first():
            return {'message': "Teacher with this name already exists."}, 400

        teacher = TeacherModel(**data)

        try:
            teacher.save_to_db()
        except:
            return {"message": "An error occurred while inserting the teacher."}, 500

        return teacher.json(), 201