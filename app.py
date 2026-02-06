from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from models import db, Package, Lead

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
