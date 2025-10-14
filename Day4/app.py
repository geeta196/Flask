from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Upload folders
UPLOAD_FOLDER = "upload"
IMAGE_FOLDER = os.path.join(UPLOAD_FOLDER, 'images')
RESUME_FOLDER = os.path.join(UPLOAD_FOLDER, 'resume')

os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(RESUME_FOLDER, exist_ok=True)

# Configuration
app.config['IMAGE_UPLOADS'] = IMAGE_FOLDER
app.config['RESUME_FOLDER'] = RESUME_FOLDER
app.config['ALLOWED_IMAGE_EXTENSIONS'] = {'png','jpg','jpeg'}
app.config['ALLOWED_RESUME_EXTENSIONS'] = {'pdf','doc','docx'}

# Sample database
students = []
student_id_counter = 1

# Check allowed file
def allowed_file(filename, allowed_set):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in allowed_set

# Add student
@app.route("/student", methods=['POST'])
def add_student():
    global student_id_counter

    name = request.form.get('name')
    email = request.form.get('email')
    age = request.form.get('age')

    if not all([name, email, age]):
        return jsonify({'error':'Missing required field'}), 400

    profile_img = request.files.get('profile_img')
    resume = request.files.get('resume')

    if not profile_img or not resume:
        return jsonify({'error':'Profile image and resume required'}), 400

    if not allowed_file(profile_img.filename, app.config['ALLOWED_IMAGE_EXTENSIONS']):
        return jsonify({'error':'Invalid image format (allowed: jpg, jpeg, png)'}), 400

    if not allowed_file(resume.filename, app.config['ALLOWED_RESUME_EXTENSIONS']):
        return jsonify({'error':'Invalid resume format (allowed: pdf, doc, docx)'}), 400

    # Save files securely
    image_filename = secure_filename(profile_img.filename)
    resume_filename = secure_filename(resume.filename)

    image_path = os.path.join(app.config['IMAGE_UPLOADS'], image_filename)
    resume_path = os.path.join(app.config['RESUME_FOLDER'], resume_filename)

    profile_img.save(image_path)
    resume.save(resume_path)

    # Create student record
    student = {
        'id': student_id_counter,
        'name': name,
        'email': email,
        'age': age,
        'profile_img': image_filename,
        'resume': resume_filename
    }
    students.append(student)
    student_id_counter += 1

    return jsonify({'message':'Student added successfully', 'student': student}), 201

# Update Student
@app.route('/student/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    for student in students:
        if student['id'] == student_id:
            name = request.form.get('name')
            email = request.form.get('email')
            age = request.form.get('age')

            if name: student['name'] = name
            if email: student['email'] = email
            if age: student['age'] = age

            return jsonify({'message':'Student updated successfully', 'student':student}),200
    return jsonify({'error':'Student not found'}),404

# Delete Student
@app.route('/student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    global students
    students = [s for s in students if s['id'] != student_id]
    return jsonify({'message':'Student deleted successfully'}),200

# Get all students
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify({'students': students}),200

# Run App
if __name__ == '__main__':
    app.run(debug=True)
