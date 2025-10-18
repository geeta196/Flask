from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# -------------------- FLASK APP -------------------- #
app = Flask(__name__)

# -------------------- DATABASE CONFIG -------------------- #
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:root@localhost:5432/interships_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -------------------- MODELS -------------------- #
class Student(db.Model):
    __tablename__ = "students"
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100) )
    email = db.Column(db.String(100), unique=True,)
    course = db.Column(db.String(100))

    interships = db.relationship("Intership", backref="student", lazy=True)


class Intership(db.Model):
    __tablename__ = "intership"
    intership_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100))
    duration_months = db.Column(db.Integer)
    stipend = db.Column(db.Float)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))


# -------------------- CREATE TABLES -------------------- #
with app.app_context():
    db.create_all()

# -------------------- MAIN ROUTE -------------------- #
@app.route('/')
def home():
    return "Welcome to Flask Internship App"

# -------------------- ADD STUDENT -------------------- #
@app.route('/student', methods=['POST'])
def add_student():
    name = request.form.get('name')
    email = request.form.get('email')
    course = request.form.get('course')

    student = Student(name=name, email=email, course=course)
    db.session.add(student)
    db.session.commit()
    return jsonify({"message": "Student added successfully"}), 201

# -------------------- ADD INTERNSHIP -------------------- #
@app.route('/intership', methods=['POST'])
def add_intership():
    student_id = request.form.get('student_id')
    company_name = request.form.get('company_name')
    duration_months = request.form.get('duration_months')
    stipend = request.form.get('stipend')

    # Convert student_id only if provided
    intern = Intership(
        student_id=int(student_id) if student_id else None,
        company_name=company_name,
        duration_months=int(duration_months),
        stipend=float(stipend)
    )
    db.session.add(intern)
    db.session.commit()
    return jsonify({"message": "Internship added successfully!"}), 201

# -------------------- INNER JOIN -------------------- #
@app.route('/join/inner', methods=['GET'])
def inner_join():
    data = db.session.query(Student, Intership).join(Intership).all()
    result = [
        {
            'student_name': s.name,
            'course': s.course,
            'company': i.company_name,
            'duration': i.duration_months,
            'stipend': i.stipend
        } for s, i in data
    ]
    return jsonify(result)

# -------------------- LEFT JOIN -------------------- #
@app.route('/join/left', methods=['GET'])
def left_join():
    data = db.session.query(Student, Intership).outerjoin(Intership).all()
    result = [
        {
            'student_name': s.name,
            'course': s.course,
            'company': i.company_name if i else None,
            'duration': i.duration_months if i else None,
            'stipend': i.stipend if i else None
        } for s, i in data
    ]
    return jsonify(result)

# -------------------- RIGHT JOIN -------------------- #
@app.route('/join/right', methods=['GET'])
def right_join():
    sql = """
    SELECT s.name, s.course, i.company_name, i.duration_months, i.stipend
    FROM students s
    RIGHT JOIN intership i
    ON s.student_id = i.student_id;
    """
    result = db.session.execute(text(sql))
    data = [
        {
            'student_name': row[0],
            'course': row[1],
            'company': row[2],
            'duration': row[3],
            'stipend': row[4]
        } for row in result
    ]
    return jsonify(data)

# -------------------- FULL OUTER JOIN -------------------- #
@app.route('/join/full', methods=['GET'])
def full_join():
    sql = """
    SELECT s.name, s.course, i.company_name, i.duration_months, i.stipend
    FROM students s
    FULL OUTER JOIN intership i
    ON s.student_id = i.student_id;
    """
    result = db.session.execute(text(sql))
    data = [
        {
            'student_name': row[0],
            'course': row[1],
            'company': row[2],
            'duration': row[3],
            'stipend': row[4]
        } for row in result
    ]
    return jsonify(data)

# -------------------- RUN APP -------------------- #
if __name__ == '__main__':
    app.run(debug=True)
