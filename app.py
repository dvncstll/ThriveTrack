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

@app.route('/employee-dashboard')
def employee_dashboard():
    return render_template('employee-dashboard.html')

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