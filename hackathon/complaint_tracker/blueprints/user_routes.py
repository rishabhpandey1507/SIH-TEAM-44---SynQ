from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import db, Complaint

# Create a Blueprint
user_bp = Blueprint('user_bp', __name__,
                    template_folder='../templates',
                    static_folder='../static')

@user_bp.route('/')
def index():
    return render_template('index.html')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Placeholder for login logic
        flash('Login functionality is not yet implemented.', 'info')
        return redirect(url_for('user_bp.login'))
    return render_template('login.html')

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Placeholder for registration logic
        flash('Registration functionality is not yet implemented.', 'info')
        return redirect(url_for('user_bp.register'))
    return render_template('register.html')

@user_bp.route('/dashboard')
def dashboard():
    # Fetch all complaints and order by most recent
    complaints = Complaint.query.order_by(Complaint.created_at.desc()).all()
    return render_template('user/dashboard.html', complaints=complaints)

@user_bp.route('/submit_complaint', methods=['GET', 'POST'])
def submit_complaint():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')

        if not title or not description:
            flash('Title and description are required!', 'danger')
            return redirect(url_for('user_bp.submit_complaint'))

        new_complaint = Complaint(title=title, description=description)
        db.session.add(new_complaint)
        db.session.commit()
        
        flash('Your complaint has been submitted successfully!', 'success')
        return redirect(url_for('user_bp.dashboard'))

    return render_template('user/submit_complaint.html')

@user_bp.route('/history')
def complaint_history():
    complaints = Complaint.query.order_by(Complaint.created_at.desc()).all()
    return render_template('user/complaint_history.html', complaints=complaints)