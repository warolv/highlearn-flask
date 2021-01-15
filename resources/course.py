from flask_restful import Resource, reqparse
from models.course import CourseModel

class Course(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        required=True,
                        help="Course must have a name!"
                        )
    parser.add_argument('teacher_id',
                        type=int,
                        required=True,
                        help="Course must belong to a teacher!"
                        )

    def get(self, id):
        course = CourseModel.query.get(id)
        if course:
            return course.json()
        return {'message': 'Course not found'}, 404
    
    def put(self, id):
        data = self.parser.parse_args()
        course = CourseModel.query.get(id)

        if course:
            course.name = data['name']
            course.teacher_id = data['teacher_id']
        else:
            return {"message": "Course with a id {} not exists".format(id)}

        course.save_to_db()

        return course.json()

    def delete(self, id):
        course = CourseModel.query.get(id)
        if course:
            course.delete_from_db()
            return {'message': "Course with Id: {} deleted.".format(id)}
        return {'message': "Course with a Id: {} not exists".format(id)}, 404

class CourseList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        required=True,
                        help="Course must have a name!"
                        )
    parser.add_argument('teacher_id',
                        type=int,
                        required=True,
                        help="Course must belong to a teacher!"
                        )

    def get(self):
        courses = [course.json() for course in CourseModel.find_all()]
        return {'courses': courses}, 200
    
    def post(self):
        data = self.parser.parse_args()

        if CourseModel.query.filter_by(name=data['name']).first():
            return {'message': "Course with name '{}' already exists.".format(data['name'])}, 400

        course = CourseModel(**data)

        try:
            course.save_to_db()
        except:
            return {"message": "An error occurred while inserting the course."}, 500

        return course.json(), 201
