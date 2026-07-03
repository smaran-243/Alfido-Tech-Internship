from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy object. 
# This object will be used to interact with the database.
db = SQLAlchemy()

class Student(db.Model):
    """
    Student model representing the 'students' table in the database.
    This stores all the details of a student.
    """
    __tablename__ = 'students'

    # 1. Primary Key: Unique ID for each student (automatically incremented)
    id = db.Column(db.Integer, primary_key=True)

    # 2. Student's Full Name (cannot be empty)
    name = db.Column(db.String(100), nullable=False)

    # 3. Roll Number: Must be unique for every student (cannot be empty)
    roll_number = db.Column(db.String(50), unique=True, nullable=False)

    # 4. Department: e.g., Computer Science, Electrical Engineering, etc.
    department = db.Column(db.String(100), nullable=False)

    # 5. Academic Year: e.g., 1, 2, 3, 4 (cannot be empty)
    year = db.Column(db.Integer, nullable=False)

    # 6. Email Address: Used to contact the student
    email = db.Column(db.String(100), nullable=False)

    # 7. Phone Number: Student's contact number
    phone = db.Column(db.String(20), nullable=False)

    # 8. Cumulative Grade Point Average (CGPA): Must be a float between 0.0 and 10.0
    cgpa = db.Column(db.Float, nullable=False)

    # 9. Address: Student's residential address
    address = db.Column(db.Text, nullable=False)

    # 10. Registration Time: Automatically set to the date and time when the record is created
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        # A helper method to print a student object nicely (useful for debugging)
        return f"<Student {self.name} - {self.roll_number}>"
