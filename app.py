from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
from burnout_agent import evaluate_burnout

app = Flask(__name__)

client = MongoClient("mongodb+srv://thrivetrack_db:thrivetrack12345@thrivetrack.jwy3x3m.mongodb.net/?retryWrites=true&w=majority&appName=ThriveTrack")
db = client["thriverack"]
collection = db["responses"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hr-inventory')
def hr_inventory():
    return render_template('hr-inventory.html')

@app.route('/hr-orders')
def hr_orders():
    return render_template('hr-orders.html')

@app.route('/hr-purchase')
def hr_purchase():
    return render_template('hr-purchase.html')

@app.route('/hr-reporting')
def hr_reporting():
    return render_template('hr-reporting.html')

@app.route('/hr-support')
def hr_support():
    return render_template('hr-support.html')

@app.route('/hr-settings')
def hr_settings():
    return render_template('hr-settings.html')

@app.route('/employee-dashboard')
def employee_dashboard():
    return render_template('employee-dashboard.html')

@app.route('/employee-profile')
def employee_profile():
    return render_template('employee-profile.html')

@app.route('/employee-leave')
def employee_leave():
    return render_template('employee-leave.html')

@app.route('/employee-workload')
def employee_workload():
    return render_template('employee-workload.html')

@app.route('/employee-feedback')
def employee_feedback():
    return render_template('employee-feedback.html')

@app.route('/employee-actions')
def employee_actions():
    return render_template('employee-actions.html')

@app.route('/employee-announcements')
def employee_announcements():
    return render_template('employee-announcements.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/redirect')
def redirect_page():
    return render_template('redirect.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.to_dict()
    burnout_score = evaluate_burnout(data)
    data['burnout_score'] = burnout_score
    collection.insert_one(data)
    return jsonify({'message': 'Submitted!', 'burnout_score': burnout_score})

if __name__ == '__main__':
    app.run(debug=True)