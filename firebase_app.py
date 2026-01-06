"""
Firebase-Integrated Interview System
Features:
- Google & Email/Password Authentication (via Firebase)
- Realtime Database storage
- Backend Token Verification
"""

from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db, auth
import os
import json
from datetime import datetime, timedelta
from train_model import InterviewModel
import secrets

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = secrets.token_hex(32)
CORS(app)

# Initialize Firebase Admin SDK
# You must download 'serviceAccountKey.json' from Firebase Console -> Project Settings -> Service Accounts
SERVICE_ACCOUNT_KEY = 'serviceAccountKey.json'

try:
    if not firebase_admin._apps:
        if os.path.exists(SERVICE_ACCOUNT_KEY):
            cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://YOU-MUST-REPLACE-THIS-WITH-YOUR-DB-URL.firebaseio.com/' 
            })
            print("✅ Firebase Admin SDK initialized successfully!")
            
            # Using environment variable for DB URL if available, otherwise placeholder
            # You should update this!
            ref = db.reference('/')
        else:
            print(f"⚠️  {SERVICE_ACCOUNT_KEY} not found. Please follow FIREBASE_SETUP.md")
except Exception as e:
    print(f"❌ Error initializing Firebase: {e}")

# Initialize model
model = InterviewModel()
try:
    model.load_model('model')
    print("✅ ML Model loaded successfully!")
except Exception as e:
    print(f"⚠️  Model not found: {e}")

# Helper to checking/getting DB reference
def get_db_ref(path):
    if not firebase_admin._apps:
        return None
    return db.reference(path)

@app.route('/')
def index():
    """Main page"""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('auth_interview.html')

@app.route('/login')
def login_page():
    """Login page"""
    return render_template('firebase_login.html')

@app.route('/api/auth/verify', methods=['POST'])
def verify_token():
    """Verify Firebase ID Token sent from client and create session"""
    token = request.json.get('token')
    
    if not token:
        return jsonify({'error': 'No token provided'}), 400
        
    try:
        # Verify token with Firebase Admin
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        email = decoded_token.get('email', '')
        name = decoded_token.get('name', email.split('@')[0])
        picture = decoded_token.get('picture', '')
        
        # Create session
        session['user_id'] = uid
        session['username'] = name
        session['email'] = email
        session['profile_picture'] = picture
        
        # Create/Update user in Realtime DB
        user_ref = get_db_ref(f'users/{uid}')
        if user_ref:
            user_data = user_ref.get()
            if not user_data:
                user_ref.set({
                    'username': name,
                    'email': email,
                    'created_at': datetime.now().isoformat(),
                    'total_interviews': 0
                })
        
        return jsonify({'success': True, 'user': {'uid': uid, 'name': name}})
        
    except Exception as e:
        print(f"Auth Error: {e}")
        return jsonify({'error': 'Invalid token'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

def can_start_interview(user_id):
    """Check limits using Firebase DB"""
    if not firebase_admin._apps:
        return {'can_start': True, 'error': 'Firebase not connected'} # Allow if offline for now logic

    user_ref = get_db_ref(f'users/{user_id}')
    sessions_ref = get_db_ref('interview_sessions')
    
    user_data = user_ref.get() or {}
    total = user_data.get('total_interviews', 0)
    
    # Check 24h limit
    yesterday = (datetime.now() - timedelta(hours=24)).isoformat()
    
    # Query sessions for this user (inefficient in NoSQL without index, but okay for small scale)
    # Using python filtering for simplicity
    sessions_snapshot = sessions_ref.order_by_child('user_id').equal_to(user_id).get()
    
    recent_count = 0
    if sessions_snapshot:
        for k, v in sessions_snapshot.items():
            if v.get('start_time') > yesterday:
                recent_count += 1
                
    return {
        'can_start': recent_count < 2 and total < 5,
        'interviews_last_24h': recent_count,
        'total_interviews': total,
        'remaining_24h': max(0, 2 - recent_count),
        'remaining_total': max(0, 5 - total)
    }

@app.route('/api/user-stats', methods=['GET'])
def user_stats():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    limits = can_start_interview(session['user_id'])
    return jsonify({
        'username': session['username'],
        'can_start': limits.get('can_start', False),
        'remaining_24h': limits.get('remaining_24h', 0),
        'remaining_total': limits.get('remaining_total', 0)
    })

@app.route('/api/start-interview', methods=['POST'])
def start_interview():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    limits = can_start_interview(user_id)
    
    if not limits['can_start']:
        return jsonify({'error': 'Limit reached', 'limits': limits}), 403
        
    data = request.json
    role = data.get('role', 'Software Engineer')
    category = data.get('category', 'Technical')
    difficulty = data.get('difficulty', None)
    num_questions = int(data.get('num_questions', 5))
    
    # Get questions from ML model
    questions = model.get_questions(role, category, difficulty, num_questions)
    
    session_id = secrets.token_hex(8)
    
    # Save to Firebase
    new_session = {
        'user_id': user_id,
        'role': role,
        'category': category,
        'difficulty': difficulty or 'mixed',
        'questions': questions,
        'current_index': 0,
        'answers': [],
        'start_time': datetime.now().isoformat(),
        'completed': False,
        'tab_switches': 0
    }
    
    get_db_ref(f'interview_sessions/{session_id}').set(new_session)
    
    # Increment user total
    user_ref = get_db_ref(f'users/{user_id}')
    current_total = user_ref.get().get('total_interviews', 0)
    user_ref.update({'total_interviews': current_total + 1})
    
    return jsonify({
        'session_id': session_id,
        'total_questions': len(questions),
        'first_question': questions[0]
    })

@app.route('/api/get-question/<session_id>', methods=['GET'])
def get_question(session_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
        
    sess_ref = get_db_ref(f'interview_sessions/{session_id}')
    sess = sess_ref.get()
    
    if not sess:
        return jsonify({'error': 'Session not found'}), 404
        
    if sess['user_id'] != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
        
    idx = sess['current_index']
    questions = sess['questions']
    
    if idx >= len(questions):
        return jsonify({'completed': True})
        
    return jsonify({
        'question': questions[idx],
        'question_number': idx + 1,
        'total_questions': len(questions),
        'completed': False
    })

@app.route('/api/submit-answer/<session_id>', methods=['POST'])
def submit_answer(session_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
        
    data = request.json
    answer = data.get('answer', '')
    
    sess_ref = get_db_ref(f'interview_sessions/{session_id}')
    sess = sess_ref.get()
    
    idx = sess['current_index']
    questions = sess['questions']
    
    # Update local list and push to DB
    answers = sess.get('answers', [])
    answers.append({
        'question': questions[idx],
        'answer': answer,
        'timestamp': datetime.now().isoformat()
    })
    
    idx += 1
    completed = idx >= len(questions)
    
    updates = {
        'answers': answers,
        'current_index': idx,
        'completed': completed
    }
    
    if completed:
        updates['end_time'] = datetime.now().isoformat()
        
    sess_ref.update(updates)
    
    if completed:
        return jsonify({'completed': True})
        
    return jsonify({
        'completed': False,
        'next_question': questions[idx],
        'question_number': idx + 1
    })

@app.route('/api/report-tab-switch/<session_id>', methods=['POST'])
def report_tab_switch(session_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
        
    sess_ref = get_db_ref(f'interview_sessions/{session_id}')
    sess_ref.transaction(lambda current_stmt: (current_stmt or {}) | {'tab_switches': (current_stmt.get('tab_switches', 0) + 1)} if current_stmt else None)
    
    return jsonify({'success': True})

@app.route('/api/get-results/<session_id>', methods=['GET'])
def get_results(session_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
        
    sess = get_db_ref(f'interview_sessions/{session_id}').get()
    
    # Generate simple report for now (same logic as before can be imported)
    return jsonify({
        'role': sess['role'],
        'answers': sess.get('answers', []),
        'total_questions': len(sess['questions']),
        'total_answered': len(sess.get('answers', [])),
        'tab_switches': sess.get('tab_switches', 0),
        'report': generate_report_logic(sess) # We'll define this briefly
    })

def generate_report_logic(sess):
    # Simplified version of the detailed report
    answers = sess.get('answers', [])
    total = len(sess['questions'])
    answered = len([a for a in answers if a['answer'] != '[Skipped]'])
    
    return {
        'performance': 'Good' if answered/total > 0.7 else 'Fair',
        'completion_rate': round((answered/total)*100, 1),
        'feedback': 'Good effort!',
        'avg_answer_length': 0, # Placeholder
        'strengths': ['Participant'], 
        'recommendations': ['Practice more']
    }

if __name__ == '__main__':
    print("🔥 FIREBASE BACKEND STARTING...")
    print("Please ensure you have:")
    print("1. serviceAccountKey.json in root")
    print("2. Correct databaseURL in initialize_app")
    app.run(debug=True, port=5000)
