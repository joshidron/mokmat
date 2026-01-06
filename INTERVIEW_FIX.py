# Add this function before the start_interview route in auth_app.py

def get_fallback_questions(role, category, num_questions):
    """Generate fallback questions when model is not available"""
    
    technical_questions = [
        "Explain the difference between var, let, and const in JavaScript.",
        "What is the difference between == and === in JavaScript?",
        "Explain the concept of closures in JavaScript.",
        "What is the event loop in JavaScript?",
        "Explain the difference between synchronous and asynchronous programming.",
        "What are promises in JavaScript and how do they work?",
        "Explain the concept of REST APIs.",
        "What is the difference between HTTP and HTTPS?",
        "Explain the MVC architecture pattern.",
        "What is the difference between SQL and NoSQL databases?",
        "What is object-oriented programming?",
        "Explain the SOLID principles.",
        "What is the difference between abstract class and interface?",
        "Explain dependency injection.",
        "What are design patterns? Give examples."
    ]
    
    behavioral_questions = [
        "Tell me about a time when you faced a challenging problem at work. How did you solve it?",
        "Describe a situation where you had to work with a difficult team member.",
        "Tell me about a project you're most proud of.",
        "How do you handle tight deadlines and pressure?",
        "Describe a time when you had to learn a new technology quickly.",
        "Tell me about a time when you made a mistake. How did you handle it?",
        "How do you stay updated with new technologies?",
        "Describe your ideal work environment.",
        "Tell me about a time when you had to give constructive feedback.",
        "How do you prioritize tasks when you have multiple deadlines?",
        "Describe a situation where you showed leadership.",
        "Tell me about a time when you disagreed with your manager.",
        "How do you handle conflicts in a team?",
        "Describe a time when you went above and beyond.",
        "What motivates you in your work?"
    ]
    
    if category.lower() == 'technical':
        questions = technical_questions
    else:
        questions = behavioral_questions
    
    # Return requested number of questions
    return questions[:min(num_questions, len(questions))]


# REPLACE the start_interview function with this:

@app.route('/api/start-interview', methods=['POST'])
def start_interview():
    """Start a new interview session"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    
    # Check limits
    limits = can_start_interview(user_id)
    if not limits['can_start']:
        return jsonify({
            'error': 'Interview limit reached',
            'limits': limits
        }), 403
    
    try:
        data = request.json
        role = data.get('role', 'Software Engineer')
        category = data.get('category', 'Technical')
        difficulty = data.get('difficulty', None)
        num_questions = data.get('num_questions', 5)
        
        # Generate session ID
        session_id = f"session_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Get questions - with fallback if model not available
        try:
            questions = model.get_questions(
                role=role,
                category=category,
                difficulty=difficulty,
                num_questions=num_questions
            )
        except Exception as model_error:
            print(f"[WARNING] Model error: {model_error}")
            print("[INFO] Using fallback questions")
            # Fallback questions if model fails
            questions = get_fallback_questions(role, category, num_questions)
        
        if not questions or len(questions) == 0:
            return jsonify({'error': 'Failed to generate questions'}), 500
        
        # Store in database
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute('''
            INSERT INTO interview_sessions 
            (user_id, session_id, role, category, difficulty, total_questions)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, session_id, role, category, difficulty or 'mixed', len(questions)))
        
        # Update user's total interviews
        c.execute('UPDATE users SET total_interviews = total_interviews + 1 WHERE id = ?', (user_id,))
        
        conn.commit()
        conn.close()
        
        # Store session in memory
        interview_sessions[session_id] = {
            'user_id': user_id,
            'role': role,
            'category': category,
            'difficulty': difficulty,
            'questions': questions,
            'current_index': 0,
            'answers': [],
            'tab_switches': 0,
            'warning_count': 0,
            'start_time': datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'total_questions': len(questions),
            'first_question': questions[0] if questions else None
        })
        
    except Exception as e:
        print(f"[ERROR] Failed to start interview: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to start interview: {str(e)}'}), 500
