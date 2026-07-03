import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Student

app = Flask(__name__)

# ----------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------
# The Secret Key is required for keeping client-side sessions secure and enabling Flash messages.
app.config['SECRET_KEY'] = 'student_record_secret_key_12345'

# SQLAlchemy configuration. We use SQLite.
# Flask-SQLAlchemy 3.x stores the SQLite database in the 'instance' directory by default.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Bind the db object from models.py to our Flask application
db.init_app(app)

# ----------------------------------------------------
# DATABASE INITIALIZATION
# ----------------------------------------------------
# This block runs when the app starts. It checks if the database exists,
# and if not, creates the necessary tables based on the models.py definition.
with app.app_context():
    db.create_all()

# ----------------------------------------------------
# ROUTES IMPLEMENTATION
# ----------------------------------------------------

@app.route('/')
def home():
    """
    Route: Home Page
    HTTP Method: GET
    Template Rendered: home.html
    Database Operation: Query count of total students to display on the dashboard.
    """
    # Query database for the total number of students
    total_students = Student.query.count()
    return render_template('home.html', total_students=total_students)

@app.route('/about')
def about():
    """
    Route: About Page
    HTTP Method: GET
    Template Rendered: about.html
    Database Operation: None
    """
    return render_template('about.html')

@app.route('/contact')
def contact():
    """
    Route: Contact Page
    HTTP Method: GET
    Template Rendered: contact.html
    Database Operation: None
    """
    return render_template('contact.html')

@app.route('/students')
def students_list():
    """
    Route: View Student Directory
    HTTP Method: GET
    Template Rendered: students.html
    Database Operation: Fetch all students from the 'students' table, optionally sorting by name or department.
    """
    # Read the sorting option from query parameters (e.g. ?sort=name)
    sort_by = request.args.get('sort')
    
    if sort_by == 'name':
        # Query all students and sort alphabetically by name (A-Z)
        students = Student.query.order_by(Student.name.asc()).all()
    elif sort_by == 'department':
        # Query all students and sort alphabetically by department name (A-Z)
        students = Student.query.order_by(Student.department.asc()).all()
    else:
        # Default: Fetch students in the order they were created (by ID)
        students = Student.query.all()
        
    return render_template('students.html', students=students, current_sort=sort_by)

@app.route('/student/<int:id>')
def student_details(id):
    """
    Route: View Specific Student Details
    HTTP Method: GET
    Template Rendered: student_details.html
    Database Operation: Fetch one student by ID or return 404 (Not Found).
    """
    student = Student.query.get_or_404(id)
    return render_template('student_details.html', student=student)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    """
    Route: Add New Student Record
    HTTP Method: GET (displays form) and POST (handles form submission)
    Template Rendered: add_student.html (GET)
    Database Operation: Insert new Student object into 'students' table on POST.
    """
    if request.method == 'POST':
        # Retrieve form data submitted by user
        name = request.form.get('name', '').strip()
        roll_number = request.form.get('roll_number', '').strip()
        department = request.form.get('department', '').strip()
        year = request.form.get('year', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        cgpa = request.form.get('cgpa', '').strip()
        address = request.form.get('address', '').strip()

        # ----------------------------------------------------
        # BACKEND FORM VALIDATION
        # ----------------------------------------------------
        # 1. Check if any fields are empty
        if not name or not roll_number or not department or not year or not email or not phone or not cgpa or not address:
            flash("All fields are required.", "danger")
            return render_template('add_student.html')

        # 2. Check email structure (must contain @ and .)
        if "@" not in email or "." not in email:
            flash("Please enter a valid email address.", "danger")
            return render_template('add_student.html')

        # 3. Validate Year integer parsing
        try:
            year_val = int(year)
            if year_val < 1 or year_val > 4:
                flash("Year must be between 1 and 4.", "danger")
                return render_template('add_student.html')
        except ValueError:
            flash("Year must be a valid number.", "danger")
            return render_template('add_student.html')

        # 4. Validate CGPA range
        try:
            cgpa_val = float(cgpa)
            if cgpa_val < 0.0 or cgpa_val > 10.0:
                flash("CGPA must be between 0.0 and 10.0.", "danger")
                return render_template('add_student.html')
        except ValueError:
            flash("CGPA must be a valid decimal number.", "danger")
            return render_template('add_student.html')

        # 5. Check if roll number already exists in database
        existing_student = Student.query.filter_by(roll_number=roll_number).first()
        if existing_student:
            flash("Roll Number already exists. Please enter a unique one.", "danger")
            return render_template('add_student.html')

        # ----------------------------------------------------
        # DATABASE OPERATION: CREATE
        # ----------------------------------------------------
        # Create a new Student model instance
        new_student = Student(
            name=name,
            roll_number=roll_number,
            department=department,
            year=year_val,
            email=email,
            phone=phone,
            cgpa=cgpa_val,
            address=address
        )
        
        # Add to database session and commit
        db.session.add(new_student)
        db.session.commit()

        # Display success message and redirect
        flash("Student added successfully.", "success")
        return redirect(url_for('students_list'))

    # If HTTP Method is GET, simply render the form template
    return render_template('add_student.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    """
    Route: Edit/Update Existing Student Record
    HTTP Method: GET (displays form with current data) and POST (saves updated data)
    Template Rendered: edit_student.html (GET)
    Database Operation: Fetch student by ID on GET, update fields and commit on POST.
    """
    student = Student.query.get_or_404(id)

    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('name', '').strip()
        roll_number = request.form.get('roll_number', '').strip()
        department = request.form.get('department', '').strip()
        year = request.form.get('year', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        cgpa = request.form.get('cgpa', '').strip()
        address = request.form.get('address', '').strip()

        # ----------------------------------------------------
        # BACKEND FORM VALIDATION
        # ----------------------------------------------------
        if not name or not roll_number or not department or not year or not email or not phone or not cgpa or not address:
            flash("All fields are required.", "danger")
            return render_template('edit_student.html', student=student)

        if "@" not in email or "." not in email:
            flash("Please enter a valid email address.", "danger")
            return render_template('edit_student.html', student=student)

        try:
            year_val = int(year)
            if year_val < 1 or year_val > 4:
                flash("Year must be between 1 and 4.", "danger")
                return render_template('edit_student.html', student=student)
        except ValueError:
            flash("Year must be a valid number.", "danger")
            return render_template('edit_student.html', student=student)

        try:
            cgpa_val = float(cgpa)
            if cgpa_val < 0.0 or cgpa_val > 10.0:
                flash("CGPA must be between 0.0 and 10.0.", "danger")
                return render_template('edit_student.html', student=student)
        except ValueError:
            flash("CGPA must be a valid decimal number.", "danger")
            return render_template('edit_student.html', student=student)

        # Check if roll number conflicts with ANOTHER student's roll number
        existing_student = Student.query.filter_by(roll_number=roll_number).first()
        if existing_student and existing_student.id != id:
            flash("Roll Number already exists. Please enter a unique one.", "danger")
            return render_template('edit_student.html', student=student)

        # ----------------------------------------------------
        # DATABASE OPERATION: UPDATE
        # ----------------------------------------------------
        # Update existing student instance variables
        student.name = name
        student.roll_number = roll_number
        student.department = department
        student.year = year_val
        student.email = email
        student.phone = phone
        student.cgpa = cgpa_val
        student.address = address

        # Commit changes to database
        db.session.commit()

        # Display success message and redirect
        flash("Student updated successfully.", "success")
        return redirect(url_for('student_details', id=student.id))

    # If HTTP Method is GET, render form pre-populated with student data
    return render_template('edit_student.html', student=student)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_student(id):
    """
    Route: Delete Student Record
    HTTP Method: GET (shows confirmation page) and POST (deletes from database)
    Template Rendered: delete_confirm.html (GET)
    Database Operation: Fetch student by ID on GET, delete record and commit on POST.
    """
    student = Student.query.get_or_404(id)

    if request.method == 'POST':
        # ----------------------------------------------------
        # DATABASE OPERATION: DELETE
        # ----------------------------------------------------
        db.session.delete(student)
        db.session.commit()

        # Display confirmation message and redirect
        flash("Student deleted successfully.", "success")
        return redirect(url_for('students_list'))

    # If HTTP Method is GET, render confirmation question page
    return render_template('delete_confirm.html', student=student)

@app.route('/search')
def search():
    """
    Route: Search Student Records
    HTTP Method: GET
    Template Rendered: students.html (shows matching results in table)
    Database Operation: Query database using filters (search by name, roll number, or department).
    """
    # Get the search query from the URL request (e.g. /search?query=Computer)
    query = request.args.get('query', '').strip()
    
    if query:
        # Construct search patterns with wildcards (%)
        search_pattern = f"%{query}%"
        # Filter students checking name, roll number, or department
        students = Student.query.filter(
            (Student.name.like(search_pattern)) |
            (Student.roll_number.like(search_pattern)) |
            (Student.department.like(search_pattern))
        ).all()
    else:
        # If query is empty, return empty list
        students = []

    # Render students table page passing search results and search query string
    return render_template('students.html', students=students, search_query=query)

# ----------------------------------------------------
# APP EXECUTION
# ----------------------------------------------------
if __name__ == '__main__':
    # Start the Flask development server on port 5000 in debug mode.
    # Debug mode allows code reload and interactive debugger.
    app.run(debug=True)
