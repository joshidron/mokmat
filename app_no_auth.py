"""
Interview System Backend API
Flask server that serves the AI interview system
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import sys
from train_model import InterviewModel
import json
from datetime import datetime

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Initialize model
model = InterviewModel()

# Load trained model
try:
    model.load_model('model')
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"⚠️  Model not found. Please run 'python train_model.py' first.")
    print(f"   Error: {e}")

# Store interview sessions
interview_sessions = {}

@app.route('/')
def index():
    """Serve the main interview interface"""
    return render_template('interview.html')

@app.route('/api/start-interview', methods=['POST'])
def start_interview():
    """Start a new interview session"""
    data = request.json
    role = data.get('role', 'Software Engineer')
    category = data.get('category', 'Technical')
    difficulty = data.get('difficulty', None)
    num_questions = data.get('num_questions', 5)
    
    # Generate session ID
    session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Get questions
    questions = model.get_questions(
        role=role,
        category=category,
        difficulty=difficulty,
        num_questions=num_questions
    )
    
    # Store session
    interview_sessions[session_id] = {
        'role': role,
        'category': category,
        'difficulty': difficulty,
        'questions': questions,
        'current_index': 0,
        'answers': [],
        'start_time': datetime.now().isoformat()
    }
    
    return jsonify({
        'session_id': session_id,
        'total_questions': len(questions),
        'first_question': questions[0] if questions else None
    })

@app.route('/api/get-question/<session_id>', methods=['GET'])
def get_question(session_id):
    """Get the current question for a session"""
    if session_id not in interview_sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    session = interview_sessions[session_id]
    idx = session['current_index']
    
    if idx >= len(session['questions']):
        return jsonify({
            'completed': True,
            'message': 'Interview completed!'
        })
    
    return jsonify({
        'question': session['questions'][idx],
        'question_number': idx + 1,
        'total_questions': len(session['questions']),
        'completed': False
    })

@app.route('/api/submit-answer/<session_id>', methods=['POST'])
def submit_answer(session_id):
    """Submit an answer and get the next question"""
    if session_id not in interview_sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    data = request.json
    answer = data.get('answer', '')
    
    session = interview_sessions[session_id]
    idx = session['current_index']
    
    # Store answer
    session['answers'].append({
        'question': session['questions'][idx],
        'answer': answer,
        'timestamp': datetime.now().isoformat()
    })
    
    # Move to next question
    session['current_index'] += 1
    
    # Check if interview is complete
    if session['current_index'] >= len(session['questions']):
        return jsonify({
            'completed': True,
            'message': 'Interview completed!',
            'total_answered': len(session['answers'])
        })
    
    # Return next question
    next_question = session['questions'][session['current_index']]
    
    return jsonify({
        'completed': False,
        'next_question': next_question,
        'question_number': session['current_index'] + 1,
        'total_questions': len(session['questions'])
    })

@app.route('/api/get-results/<session_id>', methods=['GET'])
def get_results(session_id):
    """Get interview results"""
    if session_id not in interview_sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    session = interview_sessions[session_id]
    
    return jsonify({
        'role': session['role'],
        'category': session['category'],
        'difficulty': session['difficulty'],
        'total_questions': len(session['questions']),
        'total_answered': len(session['answers']),
        'answers': session['answers'],
        'start_time': session['start_time']
    })

@app.route('/api/predict-difficulty', methods=['POST'])
def predict_difficulty():
    """Predict difficulty of a custom question"""
    data = request.json
    question = data.get('question', '')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    difficulty = model.predict_difficulty(question)
    category = model.predict_category(question)
    
    return jsonify({
        'question': question,
        'predicted_difficulty': difficulty,
        'predicted_category': category
    })

@app.route('/api/generate-follow-up', methods=['POST'])
def generate_follow_up():
    """Generate a follow-up question"""
    data = request.json
    question = data.get('question', '')
    answer_quality = data.get('answer_quality', 'medium')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    follow_up = model.generate_follow_up(question, answer_quality)
    
    if follow_up:
        return jsonify({
            'follow_up_question': follow_up,
            'original_question': question
        })
    else:
        return jsonify({
            'error': 'Could not generate follow-up question'
        }), 404

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get overall statistics"""
    return jsonify({
        'total_questions': len(model.questions_db),
        'categories': model.questions_db['category'].unique().tolist(),
        'roles': model.questions_db['role'].unique().tolist(),
        'difficulty_levels': model.questions_db['difficulty'].unique().tolist(),
        'active_sessions': len(interview_sessions)
    })

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 INTERVIEW SYSTEM SERVER")
    print("=" * 60)
    print("\n📡 Server starting on http://localhost:5000")
    print("   Open this URL in your browser to start interviewing!")
    print("\n" + "=" * 60 + "\n")
    
    app.run(debug=True, port=5000, host='0.0.0.0')
