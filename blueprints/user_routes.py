from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import db, Complaint, User

user_bp = Blueprint('user_bp', __name__,
                    template_folder='../templates',
                    static_folder='../static')

@user_bp.route('/')
def index():
    return render_template('index.html')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('You have successfully logged in.', 'success')
            return redirect(url_for('user_bp.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('user_bp.login'))
    return render_template('login.html')

@user_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('user_bp.login'))

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists.', 'warning')
            return redirect(url_for('user_bp.register'))
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('You have successfully registered! Please log in.', 'success')
        return redirect(url_for('user_bp.login'))
    return render_template('register.html')

@user_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('You need to be logged in to view this page.', 'warning')
        return redirect(url_for('user_bp.login'))
    
    # Filter complaints by the logged-in user's ID
    user_id = session['user_id']
    complaints = Complaint.query.filter_by(user_id=user_id).order_by(Complaint.created_at.desc()).all()
    return render_template('user/dashboard.html', complaints=complaints)

@user_bp.route('/submit_complaint', methods=['GET', 'POST'])
def submit_complaint():
    if 'user_id' not in session:
        flash('You need to be logged in to submit a complaint.', 'warning')
        return redirect(url_for('user_bp.login'))
        
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        user_id = session['user_id'] # Get the current user's ID

        if not title or not description:
            flash('Title and description are required!', 'danger')
            return redirect(url_for('user_bp.submit_complaint'))

        # Create the new complaint and associate it with the user
        new_complaint = Complaint(title=title, description=description, user_id=user_id)
        db.session.add(new_complaint)
        db.session.commit()
        
        flash('Your complaint has been submitted successfully!', 'success')
        return redirect(url_for('user_bp.dashboard'))

    return render_template('user/submit_complaint.html')

@user_bp.route('/history')
def complaint_history():
    if 'user_id' not in session:
        flash('You need to be logged in to view this page.', 'warning')
        return redirect(url_for('user_bp.login'))
    
    # Filter complaints by the logged-in user's ID
    user_id = session['user_id']
    complaints = Complaint.query.filter_by(user_id=user_id).order_by(Complaint.created_at.desc()).all()
    return render_template('user/complaint_history.html', complaints=complaints)
# blueprints/user_routes.py

# ... (keep all the existing routes like dashboard, submit_complaint, etc.)

@user_bp.route('/complaint/<int:complaint_id>')
def complaint_detail(complaint_id):
    # Route Protection Check
    if 'user_id' not in session:
        flash('You need to be logged in to view this page.', 'warning')
        return redirect(url_for('user_bp.login'))

    # Fetch the specific complaint by its ID
    complaint = Complaint.query.get_or_404(complaint_id)
    
    # We will add a check later to ensure a user can only see their own complaint
    
    return render_template('user/complaint_detail.html', complaint=complaint)