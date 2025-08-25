from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from database import db, Complaint

admin_bp = Blueprint('admin_bp', __name__,
                     template_folder='../templates')

# --- SIMPLE ADMIN CREDENTIALS ---
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password123'

# --- DECORATOR TO PROTECT ADMIN ROUTES ---
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash('You must be logged in as an admin to view this page.', 'warning')
            return redirect(url_for('admin_bp.admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# --- LOGIN AND LOGOUT ROUTES ---
@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['is_admin'] = True
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_bp.admin_dashboard'))
        else:
            flash('Invalid admin credentials.', 'danger')
    return render_template('admin/admin_login.html')

@admin_bp.route('/logout')
def admin_logout():
    session.pop('is_admin', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin_bp.admin_login'))

# --- PROTECTED ADMIN PAGES ---
@admin_bp.route('/dashboard')
@admin_required
def admin_dashboard():
    all_complaints = Complaint.query.order_by(Complaint.created_at.desc()).all()
    return render_template('admin/admin_dashboard.html', complaints=all_complaints)

@admin_bp.route('/update_status/<int:complaint_id>', methods=['POST'])
@admin_required
def update_status(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    new_status = request.form.get('status')
    if new_status in ['Pending', 'In Progress', 'Resolved']:
        complaint.status = new_status
        db.session.commit()
        flash(f'Complaint #{complaint.id} status updated to {new_status}.', 'success')
    else:
        flash('Invalid status selected.', 'danger')
    return redirect(url_for('admin_bp.admin_dashboard'))

@admin_bp.route('/analytics')
@admin_required
def analytics():
    stats = {
        'total': Complaint.query.count(),
        'pending': Complaint.query.filter_by(status='Pending').count(),
        'in_progress': Complaint.query.filter_by(status='In Progress').count(),
        'resolved': Complaint.query.filter_by(status='Resolved').count()
    }
    return render_template('admin/analytics.html', stats=stats)