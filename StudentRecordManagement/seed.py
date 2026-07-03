"""
Seed script to populate the database with dummy student records.
Run this script once using: python seed.py
"""

from app import app
from models import db, Student

# Sample student records
sample_students = [
    {
        "name": "Smaran",
        "roll_number": "25eg505q01",
        "department": "Computer Science",
        "year": 4,
        "email": "25eg505q01@anurag.edu.in",
        "phone": "+91 98765 43210",
        "cgpa": 9.25,
        "address": "123 Academic Block, Anurag University, Hyderabad, Telangana, India"
    },
    {
        "name": "Jane Smith",
        "roll_number": "CS202602",
        "department": "Information Technology",
        "year": 3,
        "email": "janesmith@anurag.edu.in",
        "phone": "+91 98480 22338",
        "cgpa": 8.80,
        "address": "Green Meadows Colony, Road No 4, Secunderabad, Telangana, India"
    },
    {
        "name": "John Doe",
        "roll_number": "EE202603",
        "department": "Electrical Engineering",
        "year": 2,
        "email": "johndoe@anurag.edu.in",
        "phone": "+91 91234 56789",
        "cgpa": 7.45,
        "address": "Flat 302, Royal Residency, Uppal, Hyderabad, Telangana, India"
    }
]

def seed_database():
    with app.app_context():
        # Check if we already have records to avoid duplicates
        if Student.query.count() > 0:
            print("Database already contains records. Skipping seed process.")
            return

        print("Seeding database with sample student records...")
        for data in sample_students:
            student = Student(
                name=data["name"],
                roll_number=data["roll_number"],
                department=data["department"],
                year=data["year"],
                email=data["email"],
                phone=data["phone"],
                cgpa=data["cgpa"],
                address=data["address"]
            )
            db.session.add(student)
        
        # Save all records to database
        db.session.commit()
        print("Database successfully seeded with 3 sample students!")

if __name__ == "__main__":
    seed_database()
