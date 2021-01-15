from flask_restful import Resource, reqparse
from models.grade import GradeModel

class Grade(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('grade',
                        type=int,
                        required=True,
                        help="Grade is required!"
                        )
    parser.add_argument('student_id',
                        type=int,
                        required=True,
                        help="Grade must belong to a student!"
                        )
    parser.add_argument('course_id',
                        type=int,
                        required=True,
                        help="Grade must belong to a course!"
                        )

    def get(self, id):
        grade = GradeModel.query.get(id)
        if grade:
            return grade.json()
        
        return {'message': 'Grade not found'}, 404
    
    def put(self, id):
        data = self.parser.parse_args()
        grade = GradeModel.query.get(id)

        if grade:
            grade.grade = data['grade']
            grade.student_id = data['student_id']
            grade.course_id = data['course_id']
        else:
            return {"message": "Grade with id {} not exists".format(id)}

        grade.save_to_db()

        return grade.json()

    def delete(self, id):
        grade = GradeModel.query.get(id)
        
        if grade:
            grade.delete_from_db()
            return {'message': "Grade {} deleted.".format(id)}
        
        return {'message': "Grade with id: {} not exists".format(id)}

class GradeList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('grade',
                        type=int,
                        required=True,
                        help="Grade is required!"
                        )
    parser.add_argument('student_id',
                        type=int,
                        required=True,
                        help="Grade must belong to a student!"
                        )
    parser.add_argument('course_id',
                        type=int,
                        required=True,
                        help="Grade must belong to a course!"
                        )

    def get(self):
        grades = [grade.json() for grade in GradeModel.find_all()]
        return {'grades': grades}, 200

    def post(self):
        data = self.parser.parse_args()
        grade = GradeModel(**data)

        try:
            grade.save_to_db()
        except:
            return {"message": "An error occurred while inserting the grade."}, 500

        return grade.json(), 201