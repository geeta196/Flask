from pymongo import MongoClient

# 1️⃣ Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")

# 2️⃣ Create / connect to database
db = client['student_db']

# 3️⃣ Create / connect to collection
collection = db['students']

# ----------------------------
#  INSERT (Add Data)
# ----------------------------
students_data = [
    {'name': "Geeta", 'age': 20, 'course': "Python"},
    {'name': "Radha", 'age': 21, 'course': "Python"},
    {'name': "Sita",  'age': 22, 'course': "Java"}
]

insert_result = collection.insert_many(students_data)
print("✅ Data inserted successfully! IDs:", insert_result.inserted_ids)

# ----------------------------
#  READ (Display All Data)
# ----------------------------
print("\n📘 All Students:")
for student in collection.find():
    print(student)

# ----------------------------
#  FIND (Particular Student)
# ----------------------------
print("\n Finding student where name = 'Geeta'")
student = collection.find_one({'name': 'Geeta'})
print(student)

# ----------------------------
#  DELETE (Remove a Student)
# ----------------------------
delete_result = collection.delete_one({'name': 'Radha'})
print(f"\n Deleted Count: {delete_result.deleted_count}")

# ----------------------------
#  DISPLAY AFTER DELETE
# ----------------------------
print("\n Data after Delete:")
for student in collection.find():
    print(student)
