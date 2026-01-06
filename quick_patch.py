"""
Quick Patch for Interview Start Error
Apply this to fix "Failed to start interview" error

Instructions:
1. Run this script: python quick_patch.py
2. Restart server: python auth_app.py
3. Try starting interview again
"""

import os
import re

def apply_patch():
    auth_app_path = 'd:/codewave/auth_app.py'
    
    if not os.path.exists(auth_app_path):
        print(f"Error: {auth_app_path} not found!")
        return False
    
    print("Reading auth_app.py...")
    with open(auth_app_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already patched
    if 'get_fallback_questions' in content:
        print("Already patched! No changes needed.")
        return True
    
    print("Applying patch...")
    
    # Add fallback function before start_interview
    fallback_function = '''
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
        "What is the difference between SQL and NoSQL databases?"
    ]
    behavioral_questions = [
        "Tell me about a time when you faced a challenging problem at work.",
        "Describe a situation where you had to work with a difficult team member.",
        "Tell me about a project you're most proud of.",
        "How do you handle tight deadlines and pressure?",
        "Describe a time when you had to learn a new technology quickly."
    ]
    if category.lower() == 'technical':
        questions = technical_questions
    else:
        questions = behavioral_questions
    return questions[:min(num_questions, len(questions))]

'''
    
    # Find the start_interview function
    pattern = r"(@app\.route\('/api/start-interview', methods=\['POST'\]\))"
    content = re.sub(pattern, fallback_function + r'\1', content)
    
    # Replace the model.get_questions call
    old_code = '''    # Get questions
    questions = model.get_questions(
        role=role,
        category=category,
        difficulty=difficulty,
        num_questions=num_questions
    )'''
    
    new_code = '''    # Get questions - with fallback if model not available
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
        questions = get_fallback_questions(role, category, num_questions)
    
    if not questions or len(questions) == 0:
        return jsonify({'error': 'Failed to generate questions'}), 500'''
    
    content = content.replace(old_code, new_code)
    
    # Backup original file
    backup_path = auth_app_path + '.backup'
    print(f"Creating backup: {backup_path}")
    with open(backup_path, 'w', encoding='utf-8') as f:
        with open(auth_app_path, 'r', encoding='utf-8') as original:
            f.write(original.read())
    
    # Write patched file
    print("Writing patched file...")
    with open(auth_app_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n" + "="*60)
    print("✅ PATCH APPLIED SUCCESSFULLY!")
    print("="*60)
    print("\nNext steps:")
    print("1. Restart your server: python auth_app.py")
    print("2. Try starting an interview")
    print("\nBackup saved to:", backup_path)
    print("\nIf something goes wrong, restore from backup:")
    print(f"   copy {backup_path} {auth_app_path}")
    print("="*60)
    
    return True

if __name__ == '__main__':
    print("\n" + "="*60)
    print("INTERVIEW START ERROR - QUICK PATCH")
    print("="*60)
    print("\nThis will fix the 'Failed to start interview' error")
    print("by adding fallback questions when the model is not available.\n")
    
    response = input("Apply patch? (y/n): ")
    if response.lower() == 'y':
        apply_patch()
    else:
        print("Patch cancelled.")
