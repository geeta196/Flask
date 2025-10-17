# 🐍 Flask + PostgreSQL + File Upload API

A simple Flask REST API project that manages Employee information — including personal, job, and document details — using **PostgreSQL** and **Flask SQLAlchemy**.

---

## 🚀 Features
- Add Employee Personal Information  
- Add Employee Job Information  
- Upload Employee Documents (Profile Image & Resume)  
- Fetch Employee Details (Single / All)  
- Delete Employee Record  
- File validation and secure upload handling

---

## 🧩 Technologies Used
- Python 3.x  
- Flask  
- Flask-SQLAlchemy  
- PostgreSQL  
- Werkzeug (for secure file uploads)

---

## 🛠️ Setup Instructions

### 1️⃣ Clone this Repository
```bash
git clone https://github.com/yourusername/flask-employee-api.git
cd flask-employee-api


2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate     # (Windows)
# OR
source venv/bin/activate  # (Mac/Linux)

3️⃣ Install Dependencies
pip install flask flask_sqlalchemy psycopg2 werkzeug

4️⃣ Configure PostgreSQL Database

Open pgAdmin 4

Create a database named: Employee_db

Update your database credentials in the Flask app file:

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/Employee_db'


(Change root to your actual PostgreSQL password)

5️⃣ Run the Application
python app.py


Flask will start at:

http://127.0.0.1:5000/

