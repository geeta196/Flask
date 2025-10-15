from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# -------------------- DATABASE CONFIGURATION -------------------- #

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/Employee_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# -------------------- UPLOAD CONFIGURATION -------------------- #
UPLOAD_FOLDER = "emp_uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'pdf', 'docx'}


# -------------------- MODELS -------------------- #
class Employee(db.Model):
    __tablename__ = 'employees'  # ✅ दुरुस्ती
    emp_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    age = db.Column(db.Integer)

    job = db.relationship("JobInfo", backref="employee", uselist=False, cascade="all, delete")
    document = db.relationship("DocumentInfo", backref="employee", uselist=False, cascade="all, delete")


class JobInfo(db.Model):
    __tablename__ = 'job_info'  # ✅ दुरुस्ती
    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.String, db.ForeignKey('employees.emp_id'))
    designation = db.Column(db.String(100))
    department = db.Column(db.String(100))
    salary = db.Column(db.Float)


class DocumentInfo(db.Model):
    __tablename__ = 'document_info'  # ✅ दुरुस्ती
    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.String, db.ForeignKey('employees.emp_id'))
    profile_img = db.Column(db.String(200))
    resume = db.Column(db.String(200))


# -------------------- CREATE DATABASE TABLES -------------------- #
with app.app_context():
    db.create_all()


# -------------------- HELPER FUNCTION -------------------- #
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# -------------------- ROUTES -------------------- #

@app.route('/employee/personal', methods=['POST'])
def add_personal_info():
    emp_id = request.form.get('emp_id')
    name = request.form.get('name')
    email = request.form.get('email')
    age = request.form.get('age')

    if not all([emp_id, name, email, age]):
        return jsonify({'error': 'Missing required fields'}), 400

    emp = Employee(emp_id=emp_id, name=name, email=email, age=int(age))
    db.session.add(emp)
    db.session.commit()

    return jsonify({'message': 'Personal info saved', 'employee': emp_id}), 201


@app.route('/employee/job', methods=['POST'])
def add_job_info():
    emp_id = request.form.get('emp_id')
    designation = request.form.get('designation')
    department = request.form.get('department')
    salary = request.form.get('salary')

    emp = Employee.query.get(emp_id)
    if not emp:
        return jsonify({'error': 'Employee not found'}), 404

    job = JobInfo(emp_id=emp_id, designation=designation, department=department, salary=float(salary))
    db.session.add(job)
    db.session.commit()

    return jsonify({'message': 'Job info saved for employee', 'emp_id': emp_id}), 201


@app.route('/employee/documents', methods=['POST'])
def upload_documents():
    emp_id = request.form.get('emp_id')
    emp = Employee.query.get(emp_id)
    if not emp:
        return jsonify({'error': 'Employee not found'}), 404

    profile_img = request.files.get('profile_img')
    resume = request.files.get('resume')

    if not (profile_img and resume):
        return jsonify({'error': 'Both profile_img and resume required'}), 400

    if not (allowed_file(profile_img.filename) and allowed_file(resume.filename)):
        return jsonify({'error': 'Invalid file type'}), 400

    image_filename = secure_filename(profile_img.filename)
    resume_filename = secure_filename(resume.filename)

    profile_img.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
    resume.save(os.path.join(app.config['UPLOAD_FOLDER'], resume_filename))

    doc = DocumentInfo(emp_id=emp_id, profile_img=image_filename, resume=resume_filename)
    db.session.add(doc)
    db.session.commit()

    return jsonify({'message': 'Documents uploaded successfully', 'emp_id': emp_id}), 201


@app.route('/employee/<emp_id>', methods=['GET'])
def get_employee(emp_id):
    emp = Employee.query.get(emp_id)
    if not emp:
        return jsonify({'error': 'Employee not found'}), 404

    data = {
        'emp_id': emp.emp_id,
        'name': emp.name,
        'email': emp.email,
        'age': emp.age,
        'job': {
            'designation': emp.job.designation if emp.job else None,
            'department': emp.job.department if emp.job else None,
            'salary': emp.job.salary if emp.job else None
        },
        'documents': {
            'profile_img': emp.document.profile_img if emp.document else None,
            'resume': emp.document.resume if emp.document else None
        }
    }

    return jsonify(data)


@app.route('/employee/<emp_id>', methods=['DELETE'])
def delete_employee(emp_id):
    emp = Employee.query.get(emp_id)
    if not emp:
        return jsonify({'error': 'Employee not found'}), 404

    db.session.delete(emp)
    db.session.commit()

    return jsonify({'message': f'Employee {emp_id} deleted successfully'}), 200


@app.route('/employee', methods=['GET'])
def get_all_employees():
    employees = Employee.query.all()
    result = []

    for emp in employees:
        result.append({
            'emp_id': emp.emp_id,
            'name': emp.name,
            'email': emp.email,
            'age': emp.age,
            'designation': emp.job.designation if emp.job else None,
            'department': emp.job.department if emp.job else None,
            'salary': emp.job.salary if emp.job else None,
            'profile_img': emp.document.profile_img if emp.document else None,
            'resume': emp.document.resume if emp.document else None
        })

    return jsonify({'employees': result})


# ✅ योग्य main entry point
if __name__ == '__main__':
    app.run(debug=True)
