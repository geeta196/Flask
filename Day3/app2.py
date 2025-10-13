from flask import Flask, request, jsonify

app = Flask(__name__)

students = []

@app.route('/')
def home ():
    return jsonify({"message:" "Welcome to student Info API"})


@app.route('/add_student', methods=['POST'])
def add_student():
    data = request.get_json()

    name = data.get('name')
    age = int(data.get('age'))
    grade = data.get('grade')
    student = {"name": name, "age": age, "grade": grade}
    students.append(student)

    return jsonify({
        "message": "student added successfully",
        "student": student

    }), 201

@app.route('/get_students', methods=['GET'])

def get_students():
    return jsonify({
        "total_students": len(students),
        "data": students
    })


@app.route('/get_student', methods=['GET'])
def get_student_by_name():
    name = request.args.get('name', '').lower()
    for s in students:
        if s['name'].lower() == name:
            return jsonify(s)
    return jsonify({"message": "student not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
