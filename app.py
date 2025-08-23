from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
from burnout_agent import evaluate_burnout
from datetime import datetime
import hashlib

app = Flask(__name__)

client = MongoClient("mongodb+srv://thrivetrack_db:thrivetrack12345@thrivetrack.jwy3x3m.mongodb.net/?retryWrites=true&w=majority&appName=ThriveTrack")
db = client["thriverack"]
responses_collection = db["responses"]
feedback_collection = db["feedback"]
workload_collection = db["workload"]
wellness_collection = db["wellness"]
announcements_collection = db["announcements"]

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

@app.route('/employee-inventory')
def employee_inventory():
    return render_template('employee-inventory.html')

@app.route('/employee-orders')
def employee_orders():
    return render_template('employee-orders.html')

@app.route('/employee-purchase')
def employee_purchase():
    return render_template('employee-purchase.html')

@app.route('/employee-reporting')
def employee_reporting():
    return render_template('employee-reporting.html')

@app.route('/employee-support')
def employee_support():
    return render_template('employee-support.html')

@app.route('/employee-settings')
def employee_settings():
    return render_template('employee-settings.html')

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
    data['timestamp'] = datetime.now()
    responses_collection.insert_one(data)
    return jsonify({'message': 'Submitted!', 'burnout_score': burnout_score})

# Employee feedback submission
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    try:
        data = request.get_json()
        
        # Add timestamp and anonymization
        feedback_data = {
            'category': data.get('category'),
            'content': data.get('content'),
            'is_anonymous': data.get('isAnonymous', True),
            'timestamp': datetime.now(),
            'employee_id': hashlib.md5(data.get('userEmail', '').encode()).hexdigest() if data.get('userEmail') and not data.get('isAnonymous') else 'anonymous'
        }
        
        feedback_collection.insert_one(feedback_data)
        return jsonify({'success': True, 'message': 'Feedback submitted successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Employee workload data submission
@app.route('/submit_workload', methods=['POST'])
def submit_workload():
    try:
        data = request.get_json()
        
        workload_data = {
            'stress_level': data.get('stressLevel'),
            'workload_rating': data.get('workloadRating'),
            'work_hours': data.get('workHours'),
            'task_completion': data.get('taskCompletion'),
            'employee_email': data.get('userEmail'),
            'timestamp': datetime.now()
        }
        
        workload_collection.insert_one(workload_data)
        return jsonify({'success': True, 'message': 'Workload data submitted successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Employee wellness data submission
@app.route('/submit_wellness', methods=['POST'])
def submit_wellness():
    try:
        data = request.get_json()
        
        wellness_data = {
            'mood_rating': data.get('moodRating'),
            'sleep_quality': data.get('sleepQuality'),
            'energy_level': data.get('energyLevel'),
            'stress_factors': data.get('stressFactors', []),
            'employee_email': data.get('userEmail'),
            'timestamp': datetime.now()
        }
        
        wellness_collection.insert_one(wellness_data)
        return jsonify({'success': True, 'message': 'Wellness data submitted successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# HR Dashboard - Get employee feedback
@app.route('/api/hr/feedback', methods=['GET'])
def get_employee_feedback():
    try:
        # Get recent feedback (last 30 days)
        thirty_days_ago = datetime.now().replace(day=datetime.now().day-30) if datetime.now().day > 30 else datetime.now().replace(month=datetime.now().month-1)
        
        feedback = list(feedback_collection.find({
            'timestamp': {'$gte': thirty_days_ago}
        }).sort('timestamp', -1))
        
        # Format for HR dashboard
        feedback_summary = []
        for item in feedback:
            feedback_summary.append({
                'id': str(item['_id']),
                'category': item.get('category', 'Unknown'),
                'content': item.get('content', '')[:100] + '...' if len(item.get('content', '')) > 100 else item.get('content', ''),
                'is_anonymous': item.get('is_anonymous', True),
                'timestamp': item.get('timestamp').strftime('%Y-%m-%d %H:%M') if item.get('timestamp') else 'Unknown',
                'employee_id': item.get('employee_id', 'anonymous')
            })
        
        return jsonify({'success': True, 'feedback': feedback_summary})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# HR Dashboard - Get employee wellness trends
@app.route('/api/hr/wellness', methods=['GET'])
def get_wellness_trends():
    try:
        # Get wellness data from last 30 days
        thirty_days_ago = datetime.now().replace(day=datetime.now().day-30) if datetime.now().day > 30 else datetime.now().replace(month=datetime.now().month-1)
        
        wellness_data = list(wellness_collection.find({
            'timestamp': {'$gte': thirty_days_ago}
        }).sort('timestamp', -1))
        
        # Calculate averages and trends
        if wellness_data:
            avg_mood = sum(item.get('mood_rating', 0) for item in wellness_data) / len(wellness_data)
            avg_sleep = sum(item.get('sleep_quality', 0) for item in wellness_data) / len(wellness_data)
            avg_energy = sum(item.get('energy_level', 0) for item in wellness_data) / len(wellness_data)
        else:
            avg_mood = avg_sleep = avg_energy = 0
        
        return jsonify({
            'success': True,
            'wellness_summary': {
                'average_mood': round(avg_mood, 1),
                'average_sleep': round(avg_sleep, 1),
                'average_energy': round(avg_energy, 1),
                'total_responses': len(wellness_data)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# HR Dashboard - Get workload analysis
@app.route('/api/hr/workload', methods=['GET'])
def get_workload_analysis():
    try:
        # Get workload data from last 30 days
        thirty_days_ago = datetime.now().replace(day=datetime.now().day-30) if datetime.now().day > 30 else datetime.now().replace(month=datetime.now().month-1)
        
        workload_data = list(workload_collection.find({
            'timestamp': {'$gte': thirty_days_ago}
        }).sort('timestamp', -1))
        
        # Calculate stress level distribution
        high_stress_count = sum(1 for item in workload_data if item.get('stress_level', 0) >= 8)
        medium_stress_count = sum(1 for item in workload_data if 5 <= item.get('stress_level', 0) < 8)
        low_stress_count = sum(1 for item in workload_data if item.get('stress_level', 0) < 5)
        
        return jsonify({
            'success': True,
            'workload_summary': {
                'high_stress_employees': high_stress_count,
                'medium_stress_employees': medium_stress_count,
                'low_stress_employees': low_stress_count,
                'total_responses': len(workload_data)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# HR Announcement submission
@app.route('/submit_announcement', methods=['POST'])
def submit_announcement():
    try:
        data = request.get_json()
        
        announcement_data = {
            'title': data.get('title'),
            'content': data.get('content'),
            'urgent': data.get('urgent', False),
            'audience': data.get('audience', 'all'),
            'scheduled_date': data.get('scheduledDate'),
            'scheduled_time': data.get('scheduledTime'),
            'created_by': data.get('createdBy'),
            'timestamp': datetime.now()
        }
        
        announcements_collection.insert_one(announcement_data)
        return jsonify({'success': True, 'message': 'Announcement created successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Initialize sample data route (for testing)
@app.route('/init-sample-data', methods=['GET'])
def init_sample_data_route():
    """Route to manually initialize sample data"""
    try:
        initialize_sample_data()
        return jsonify({'success': True, 'message': 'Sample data initialized successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Clear all sample data route (for testing)
@app.route('/clear-sample-data', methods=['GET'])
def clear_sample_data_route():
    """Route to clear all sample data"""
    try:
        # Clear all collections
        announcements_collection.delete_many({})
        feedback_collection.delete_many({})
        wellness_collection.delete_many({})
        workload_collection.delete_many({})
        
        return jsonify({'success': True, 'message': 'All sample data cleared successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Add more sample data route (for testing)
@app.route('/add-more-sample-data', methods=['GET'])
def add_more_sample_data_route():
    """Route to add more sample data to existing collections"""
    try:
        # Add more feedback
        additional_feedback = [
            {
                'category': 'benefits',
                'content': 'The new parental leave policy is fantastic! Really shows the company cares about families.',
                'is_anonymous': False,
                'timestamp': datetime.now(),
                'employee_id': hashlib.md5('jessica@company.com'.encode()).hexdigest()
            },
            {
                'category': 'workplace',
                'content': 'The new standing desks are great for posture and energy levels throughout the day.',
                'is_anonymous': True,
                'timestamp': datetime.now(),
                'employee_id': 'anonymous'
            },
            {
                'category': 'culture',
                'content': 'Appreciate the monthly recognition program. It really boosts team morale.',
                'is_anonymous': False,
                'timestamp': datetime.now(),
                'employee_id': hashlib.md5('alex@company.com'.encode()).hexdigest()
            }
        ]
        
        for feedback in additional_feedback:
            feedback_collection.insert_one(feedback)
        
        # Add more wellness data
        additional_wellness = [
            {
                'mood_rating': 4,
                'sleep_quality': 6,
                'energy_level': 5,
                'stress_factors': ['project_deadline'],
                'employee_email': 'jessica@company.com',
                'timestamp': datetime.now()
            },
            {
                'mood_rating': 5,
                'sleep_quality': 8,
                'energy_level': 7,
                'stress_factors': [],
                'employee_email': 'alex@company.com',
                'timestamp': datetime.now()
            }
        ]
        
        for wellness in additional_wellness:
            wellness_collection.insert_one(wellness)
        
        # Add more workload data
        additional_workload = [
            {
                'stress_level': 5,
                'workload_rating': 6,
                'work_hours': 43,
                'task_completion': 6,
                'employee_email': 'jessica@company.com',
                'timestamp': datetime.now()
            },
            {
                'stress_level': 3,
                'workload_rating': 4,
                'work_hours': 39,
                'task_completion': 8,
                'employee_email': 'alex@company.com',
                'timestamp': datetime.now()
            }
        ]
        
        for workload in additional_workload:
            workload_collection.insert_one(workload)
        
        return jsonify({'success': True, 'message': 'Additional sample data added successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Get announcements for both HR and employees
@app.route('/api/announcements', methods=['GET'])
def get_announcements():
    try:
        # Get recent announcements (last 30 days)
        thirty_days_ago = datetime.now().replace(day=datetime.now().day-30) if datetime.now().day > 30 else datetime.now().replace(month=datetime.now().month-1)
        
        announcements = list(announcements_collection.find({
            'timestamp': {'$gte': thirty_days_ago}
        }).sort('timestamp', -1))
        
        # Format announcements for display
        formatted_announcements = []
        for item in announcements:
            # Calculate time ago
            time_diff = datetime.now() - item.get('timestamp', datetime.now())
            if time_diff.days > 0:
                time_ago = f"{time_diff.days} day{'s' if time_diff.days > 1 else ''} ago"
            elif time_diff.seconds > 3600:
                hours = time_diff.seconds // 3600
                time_ago = f"{hours} hour{'s' if hours > 1 else ''} ago"
            else:
                minutes = time_diff.seconds // 60
                time_ago = f"{minutes} minute{'s' if minutes > 1 else ''} ago"
            
            formatted_announcements.append({
                'id': str(item['_id']),
                'title': item.get('title', ''),
                'content': item.get('content', ''),
                'urgent': item.get('urgent', False),
                'audience': item.get('audience', 'all'),
                'time_ago': time_ago,
                'timestamp': item.get('timestamp').strftime('%Y-%m-%d %H:%M') if item.get('timestamp') else 'Unknown',
                'created_by': item.get('created_by', 'HR')
            })
        
        return jsonify({'success': True, 'announcements': formatted_announcements})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

def initialize_sample_data():
    """Initialize sample data for all collections if they are empty"""
    try:
        # Initialize sample announcements
        if announcements_collection.count_documents({}) == 0:
            sample_announcements = [
                {
                    'title': '🎉 Welcome to ThriveTrack!',
                    'content': 'We are excited to launch our new employee well-being platform. This tool will help us monitor and improve workplace satisfaction, workload management, and overall team health. Please take some time to explore the features and provide your feedback.',
                    'urgent': False,
                    'audience': 'all',
                    'created_by': 'HR Team',
                    'timestamp': datetime.now()
                },
                {
                    'title': '🚨 Important: Office Safety Guidelines Update',
                    'content': 'Please review the updated safety protocols in the shared drive. New guidelines include updated evacuation procedures and emergency contact information. All employees must complete the safety training module by Friday.',
                    'urgent': True,
                    'audience': 'all',
                    'created_by': 'HR Team',
                    'timestamp': datetime.now()
                },
                {
                    'title': '📅 Team Building Event - Save the Date!',
                    'content': 'Join us for our quarterly team building event on Friday, March 15th from 2-5 PM. We\'ll have team activities, refreshments, and a chance to connect with colleagues. RSVP by Wednesday to confirm your attendance.',
                    'urgent': False,
                    'audience': 'all',
                    'created_by': 'HR Team',
                    'timestamp': datetime.now()
                },
                {
                    'title': '🏥 Health Insurance Open Enrollment',
                    'content': 'Annual health insurance open enrollment begins next Monday. New plans include expanded dental coverage and mental health benefits. Schedule a consultation with HR to review your options and make changes.',
                    'urgent': False,
                    'audience': 'all',
                    'created_by': 'HR Team',
                    'timestamp': datetime.now()
                },
                {
                    'title': '📚 Professional Development Week',
                    'content': 'Next week is Professional Development Week! We\'re offering workshops on leadership, communication, and technical skills. Check the learning portal for the full schedule and register for sessions.',
                    'urgent': False,
                    'audience': 'all',
                    'created_by': 'HR Team',
                    'timestamp': datetime.now()
                },
                {
                    'title': '🎯 Q4 Performance Goals Due',
                    'content': 'Q4 performance goals are due by the end of this week. Please review and update your objectives in the performance management system. Managers will schedule goal-setting meetings.',
                    'urgent': True,
                    'audience': 'all',
                    'created_by': 'HR Team',
                    'timestamp': datetime.now()
                },
                {
                    'title': '☕ Coffee Chat with Leadership',
                    'content': 'Join us for an informal coffee chat with senior leadership this Friday at 10 AM. This is a great opportunity to ask questions, share ideas, and get to know our leadership team better.',
                    'urgent': False,
                    'audience': 'all',
                    'created_by': 'HR Team',
                    'timestamp': datetime.now()
                },
                {
                    'title': '🌱 Sustainability Initiative Launch',
                    'content': 'We\'re launching our new sustainability initiative! This includes recycling programs, energy-saving measures, and eco-friendly office supplies. Look for the detailed email with participation guidelines.',
                    'urgent': False,
                    'audience': 'all',
                    'created_by': 'HR Team',
                    'timestamp': datetime.now()
                }
            ]
            
            # Insert sample announcements
            for announcement in sample_announcements:
                announcements_collection.insert_one(announcement)
            
            print("✅ Sample announcements initialized successfully!")
        else:
            print("ℹ️ Announcements collection already contains data, skipping initialization.")
        
        # Initialize sample feedback data
        if feedback_collection.count_documents({}) == 0:
            sample_feedback = [
                {
                    'category': 'benefits',
                    'content': 'How can I get the benefits?',
                    'is_anonymous': True,
                    'timestamp': datetime.now(),
                    'employee_id': 'anonymous'
                },
                {
                    'category': 'workplace',
                    'content': 'The new office layout is much better for collaboration. Great improvement!',
                    'is_anonymous': False,
                    'timestamp': datetime.now(),
                    'employee_id': hashlib.md5('john@company.com'.encode()).hexdigest()
                },
                {
                    'category': 'management',
                    'content': 'Would appreciate more regular check-ins with my manager',
                    'is_anonymous': True,
                    'timestamp': datetime.now(),
                    'employee_id': 'anonymous'
                },
                {
                    'category': 'processes',
                    'content': 'The new project management tool is confusing. Need better training.',
                    'is_anonymous': False,
                    'timestamp': datetime.now(),
                    'employee_id': hashlib.md5('sarah@company.com'.encode()).hexdigest()
                },
                {
                    'category': 'culture',
                    'content': 'Love the new flexible work policy! It really helps with work-life balance.',
                    'is_anonymous': False,
                    'timestamp': datetime.now(),
                    'employee_id': hashlib.md5('lisa@company.com'.encode()).hexdigest()
                },
                {
                    'category': 'benefits',
                    'content': 'The new gym membership benefit is amazing. Thank you HR!',
                    'is_anonymous': False,
                    'timestamp': datetime.now(),
                    'employee_id': hashlib.md5('mike@company.com'.encode()).hexdigest()
                },
                {
                    'category': 'workplace',
                    'content': 'The new coffee machine in the break room is a game changer!',
                    'is_anonymous': True,
                    'timestamp': datetime.now(),
                    'employee_id': 'anonymous'
                },
                {
                    'category': 'management',
                    'content': 'My manager has been very supportive during this transition period.',
                    'is_anonymous': False,
                    'timestamp': datetime.now(),
                    'employee_id': hashlib.md5('emma@company.com'.encode()).hexdigest()
                }
            ]
            
            # Insert sample feedback
            for feedback in sample_feedback:
                feedback_collection.insert_one(feedback)
            
            print("✅ Sample feedback data initialized successfully!")
        else:
            print("ℹ️ Feedback collection already contains data, skipping initialization.")
        
        # Initialize sample wellness data
        if wellness_collection.count_documents({}) == 0:
            sample_wellness = [
                {
                    'mood_rating': 4,
                    'sleep_quality': 7,
                    'energy_level': 6,
                    'stress_factors': ['deadlines'],
                    'employee_email': 'john@company.com',
                    'timestamp': datetime.now()
                },
                {
                    'mood_rating': 5,
                    'sleep_quality': 8,
                    'energy_level': 7,
                    'stress_factors': [],
                    'employee_email': 'sarah@company.com',
                    'timestamp': datetime.now()
                },
                {
                    'mood_rating': 3,
                    'sleep_quality': 5,
                    'energy_level': 4,
                    'stress_factors': ['workload', 'meetings'],
                    'employee_email': 'mike@company.com',
                    'timestamp': datetime.now()
                },
                {
                    'mood_rating': 4,
                    'sleep_quality': 6,
                    'energy_level': 5,
                    'stress_factors': ['deadlines'],
                    'employee_email': 'lisa@company.com',
                    'timestamp': datetime.now()
                },
                {
                    'mood_rating': 5,
                    'sleep_quality': 9,
                    'energy_level': 8,
                    'stress_factors': [],
                    'employee_email': 'emma@company.com',
                    'timestamp': datetime.now()
                },
                {
                    'mood_rating': 2,
                    'sleep_quality': 4,
                    'energy_level': 3,
                    'stress_factors': ['personal_issues', 'workload'],
                    'employee_email': 'david@company.com',
                    'timestamp': datetime.now()
                },
                {
                    'mood_rating': 4,
                    'sleep_quality': 7,
                    'energy_level': 6,
                    'stress_factors': ['deadlines'],
                    'employee_email': 'anna@company.com',
                    'timestamp': datetime.now()
                },
                {
                    'mood_rating': 5,
                    'sleep_quality': 8,
                    'energy_level': 7,
                    'stress_factors': [],
                    'employee_email': 'tom@company.com',
                    'timestamp': datetime.now()
                }
            ]
            
            # Insert sample wellness data
            for wellness in sample_wellness:
                wellness_collection.insert_one(wellness)
            
            print("✅ Sample wellness data initialized successfully!")
        else:
            print("ℹ️ Wellness collection already contains data, skipping initialization.")
        
        # Initialize sample workload data
        if workload_collection.count_documents({}) == 0:
            sample_workload = [
                {
                    'stress_level': 3,
                    'workload_rating': 4,
                    'work_hours': 40,
                    'task_completion': 8,
                    'employee_email': 'john@company.com',
                    'timestamp': datetime.now()
                },
                {
                    'stress_level': 6,
                    'workload_rating': 7,
                    'work_hours': 45,
                    'task_completion': 6,
                    'employee_email': 'sarah@company.com',
                    'timestamp': datetime.now()
                },
                {
                    'stress_level': 8,
                    'workload_rating': 9,
                    'work_hours': 50,
                    'task_completion': 4,
                    'employee_email': 'mike@company.com',
                    'timestamp': datetime.now()
                },
                {
                    'stress_level': 4,
                    'workload_rating': 5,
                    'work_hours': 42,
                    'task_completion': 7,
                    'employee_email': 'lisa@company.com',
                    'timestamp': datetime.now()
                },
                {
                    'stress_level': 5,
                    'workload_rating': 6,
                    'work_hours': 44,
                    'task_completion': 6,
                    'employee_email': 'emma@company.com',
                    'timestamp': datetime.now()
                },
                {
                    'stress_level': 9,
                    'workload_rating': 10,
                    'work_hours': 55,
                    'task_completion': 3,
                    'employee_email': 'david@company.com',
                    'timestamp': datetime.now()
                },
                {
                    'stress_level': 4,
                    'workload_rating': 5,
                    'work_hours': 41,
                    'task_completion': 7,
                    'employee_email': 'anna@company.com',
                    'timestamp': datetime.now()
                },
                {
                    'stress_level': 2,
                    'workload_rating': 3,
                    'work_hours': 38,
                    'task_completion': 9,
                    'employee_email': 'tom@company.com',
                    'timestamp': datetime.now()
                }
            ]
            
            # Insert sample workload data
            for workload in sample_workload:
                workload_collection.insert_one(workload)
            
            print("✅ Sample workload data initialized successfully!")
        else:
            print("ℹ️ Workload collection already contains data, skipping initialization.")
            
    except Exception as e:
        print(f"❌ Error initializing sample data: {e}")

if __name__ == '__main__':
    # Initialize sample data when app starts
    initialize_sample_data()
    app.run(debug=True)