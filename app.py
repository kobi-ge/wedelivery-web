from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from models import db, Package, Lead, User
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Database connection configuration
DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("DB_NAME", "wedelivery")
DB_USER = os.environ.get("DB_USER", "user")
DB_PASS = os.environ.get("DB_PASS", "password")

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables on startup
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/track', methods=['POST'])
def track_package():
    tracking_number = request.form.get('tracking_number')
    package = Package.query.filter_by(tracking_number=tracking_number).first()
    
    if package:
        return render_template('index.html', tracking_result=package)
    else:
        flash('מספר מעקב לא נמצא', 'error')
        return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        company_name = request.form.get('company_name')
        password = request.form.get('password')
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please log in.', 'error')
            return redirect(url_for('login'))
        
        # Create new user with hashed password
        hashed_password = generate_password_hash(password)
        new_user = User(
            email=email,
            company_name=company_name,
            password_hash=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash(f'Welcome back, {user.company_name}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/join-us', methods=['GET', 'POST'])
def join_us():
    if request.method == 'POST':
        business_name = request.form.get('business_name')
        contact_person = request.form.get('contact_person')
        phone = request.form.get('phone')
        monthly_volume = request.form.get('monthly_volume')
        
        new_lead = Lead(
            business_name=business_name,
            contact_person=contact_person,
            phone=phone,
            monthly_volume=monthly_volume
        )
        db.session.add(new_lead)
        db.session.commit()
        
        flash('תודה רבה! נציג יחזור אליך בהקדם לפתיחת חשבון עסקי.', 'success')
        return redirect(url_for('index'))
        
    return render_template('join.html')

@app.route('/api/v1/webhook', methods=['POST'])
def webhook():
    # This endpoint will be used by shops to push orders via JSON in the future.
    # Currently a placeholder.
    data = request.json
    print(f"Received webhook data: {data}")
    return jsonify({"status": "received", "message": "Order processed successfully (Simulation)"}), 200

@app.route('/admin/dashboard')
def admin_dashboard():
    packages = Package.query.order_by(Package.created_at.desc()).all()
    leads = Lead.query.order_by(Lead.created_at.desc()).all()
    return render_template('admin.html', packages=packages, leads=leads)

@app.route('/admin/update_status/<int:package_id>', methods=['POST'])
def update_status(package_id):
    package = Package.query.get_or_404(package_id)
    new_status = request.form.get('status')
    package.status = new_status
    db.session.commit()
    flash('סטטוס חבילה עודכן בהצלחה', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/api/health')
def health_check():
    try:
        db.session.execute('SELECT 1')
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "database": "disconnected", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
