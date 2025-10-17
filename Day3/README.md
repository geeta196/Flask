# Employee Management API (Flask + PostgreSQL)

This project is a **REST API** for Employee Management built using **Flask** and **PostgreSQL**.  
It allows users to manage personal info, job info, and upload documents (profile image + resume).  

---

## 🛠️ Technologies Used
- Python 3.12
- Flask
- Flask SQLAlchemy
- PostgreSQL
- psycopg2
- Werkzeug (for secure file uploads)

---

## 📁 Project Structure
project/
│
├── app.py # Main Flask application
├── emp_uploads/ # Folder for uploaded files (profile images, resumes)
├── requirements.txt # Python dependencies
└── README.md


---

## ⚙️ Installation

1. Install Python (>=3.10)
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

Install dependencies:

pip install Flask Flask_SQLAlchemy psycopg2-binary Werkzeug


Install PostgreSQL and create a database (via pgAdmin or CLI):

CREATE DATABASE Employee_db;


Configure database URI in app.py:

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:YOUR_PASSWORD@localhost:5432/Employee_db'
