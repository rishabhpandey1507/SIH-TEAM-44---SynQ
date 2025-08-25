from flask import Flask, render_template

# We are not using Blueprints here for simplicity, just for testing templates.
app = Flask(__name__)

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route for the login page
@app.route('/login')
def login():
    return render_template('login.html')

# Route for the register page
@app.route('/register')
def register():
    return render_template('register.html')

# Route for the user dashboard
@app.route('/dashboard')
def dashboard():
    # We pass an empty list for now, just so the template doesn't error.
    return render_template('user/dashboard.html')

# Route for the complaint submission form
@app.route('/submit-complaint')
def submit_complaint():
    return render_template('user/submit_complaint.html')

# Route for the complaint history page
@app.route('/history')
def history():
    # Pass a dummy list of complaints to simulate real data
    dummy_complaints = [
        {'id': '003', 'title': 'Faulty street light', 'status': 'Pending', 'created_at': '2025-08-25', 'updated_at': '2025-08-25'},
        {'id': '002', 'title': 'Internet not working', 'status': 'In Progress', 'created_at': '2025-08-24', 'updated_at': '2025-08-24'},
        {'id': '001', 'title': 'Leaky faucet in kitchen', 'status': 'Resolved', 'created_at': '2025-08-22', 'updated_at': '2025-08-23'},
    ]
    return render_template('user/complaint_history.html', complaints=dummy_complaints)

if __name__ == '__main__':
    app.run(debug=True)