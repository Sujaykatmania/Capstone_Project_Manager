import bcrypt
import mysql.connector

db = mysql.connector.connect(
    host="<host name>",
    user="<user name>",
    password="<your password>",
    database="<db name>"
)
cursor = db.cursor()

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

cursor.execute("SELECT Student_ID, Password FROM Student")
students = cursor.fetchall()

for student_id, password in students:
    hashed_password = hash_password(password)
    cursor.execute("UPDATE Student SET Password = %s WHERE Student_ID = %s", (hashed_password, student_id))

cursor.execute("SELECT Mentor_ID, Password FROM Mentor")
mentors = cursor.fetchall()

for mentor_id, password in mentors:
    hashed_password = hash_password(password)
    cursor.execute("UPDATE Mentor SET Password = %s WHERE Mentor_ID = %s", (hashed_password, mentor_id))

db.commit()

cursor.close()
db.close()
