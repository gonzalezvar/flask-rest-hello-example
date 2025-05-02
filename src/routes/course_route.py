from flask import Blueprint, jsonify, request

from models import db, Course, Student, Teacher

course_bp = Blueprint('courses', __name__, url_prefix='/courses')


@course_bp.route('/', methods=["GET"])
def get_all_courses():
    list_courses = Course.get_courses(False)
    return jsonify(list_courses)


@course_bp.route('/', methods=["POST"])
def create_course():
    data_request = request.get_json()
    if not 'name' in data_request or not 'credits' in data_request or not 'teacher_id' in data_request:
        return jsonify({"error": "Los siguientes campos son obligatorios: name,credits, teacher_id "}), 400

    teacher_id = data_request["teacher_id"]
    teacher = Teacher.query.get_or_404(teacher_id)

    new_course = Course(
        name=data_request["name"],
        credits=data_request["credits"],
        teacher_id=teacher_id
    )

    try:
        db.session.add(new_course)
        db.session.commit()
        return jsonify({"message": "Curso creado con éxito"})
    except Exception as e:
        db.session.rollback()
        print("Error", e)
        return jsonify({"error": "Error en el servidor"})


@course_bp.route('/register', methods=["POST"])
def register_course():
    data_request = request.get_json()
    if not 'student_id' in data_request or not 'course_id' in data_request:
        return jsonify({"error": "Los siguientes campos son necesario:student_id, course_id"})

    student = Student.query.get_or_404(data_request["student_id"])
    course = Course.query.get_or_404(data_request["course_id"])

    if course in student.courses:
        return jsonify({"error": "Este curso ya se encuentra registrado"}), 409

    student.courses.append(course)

    try:
        db.session.commit()
        return jsonify({"message": f"Se registro el curso correctamente para {student.name}"}), 200
    except Exception as e:
        db.session.rollback()
        print("Error", e)
        return jsonify({"error": "Error en el servidor"})
