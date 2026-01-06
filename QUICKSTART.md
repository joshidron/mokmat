# 🚀 Quick Start Guide - AI Interview System

## Installation Steps

### Step 1: Install Python Packages

Run these commands one by one:

```bash
pip install flask==3.0.0
pip install flask-cors==4.0.0
pip install pandas
pip install scikit-learn
pip install numpy
```

**OR** try the requirements file:
```bash
pip install -r requirements.txt
```

### Step 2: Train the Model

```bash
python train_model.py
```

Expected output:
```
📚 Loading dataset...
✅ Loaded 600+ questions
🔧 Training model...
✅ Model trained successfully!
💾 Saving model...
```

### Step 3: Start the Server

**For the enhanced version (with login, limits, tab detection):**
```bash
python auth_app.py
```

**For the basic version (no authentication):**
```bash
python app.py
```

### Step 4: Open Browser

Go to: **http://localhost:5000**

---

## Features Overview

### ✅ Enhanced Version (`auth_app.py`)

**Includes:**
- ✅ User login/registration
- ✅ Interview limits (2 per 24h, 5 total max)
- ✅ Tab switching detection
- ✅ Dynamic performance reports
- ✅ User statistics tracking
- ✅ Role selection for interviews

**Perfect for:**
- Production use
- Multiple users
- Tracking and analytics
- Preventing abuse

### 🔥 Firebase Version (`firebase_app.py`)

**Includes:**
- ✅ Google Authentication
- ✅ Email/Password Authentication
- ✅ Realtime Database
- ✅ All features of Enhanced version

**Setup Required:**
1. Follow `FIREBASE_SETUP.md` to get keys
2. Put `serviceAccountKey.json` in root folder
3. Update `firebase_app.py` with your Database URL
4. Update `static/js/firebase_config.js` with your keys

**Start with:**
```bash
python firebase_app.py
```

### ⚡ Basic Version ('app.py')

**Includes:**
- ✅ AI-powered questions
- ✅ Interview sessions
- ✅ Results download
- ✅ Question difficulty selection

**Perfect for:**
- Quick testing
- Single user
- No authentication needed
- Simple setup

---

## First Time Usage

### Enhanced Version

1. **Register Account**
   - Click "Register" tab
   - Enter username, email, password
   - Click "Create Account"

2. **Login**
   - Enter credentials
   - Click "Login"

3. **Start Interview**
   - Select your role (Software Engineer/HR)
   - Choose category (Technical/Behavioral)
   - Pick difficulty level
   - Set number of questions
   - Click "Start Interview"

4. **Complete Interview**
   - Answer each question
   - Don't switch tabs (it's tracked!)
   - Submit or skip questions
   - View your performance report

### Basic Version

1. **Configure Interview**
   - Select role and category
   - Choose difficulty
   - Set question count

2. **Answer Questions**
   - Type your answers
   - Submit each one
   - Track progress

3. **View Results**
   - See completion stats
   - Review your answers
   - Download results

---

## Troubleshooting

### ❌ "Module not found" Error

**Solution:**
```bash
pip install <missing_module>
```

### ❌ "Model not found" Error

**Solution:**
```bash
python train_model.py
```

### ❌ Port 5000 Already in Use

**Solution:**
Edit `auth_app.py` or `app.py`, change the last line:
```python
app.run(debug=True, port=5001)  # Change to 5001 or any free port
```

### ❌ Database Error

**Solution:**
Delete `interview_system.db` file and restart server

---

## Quick Tips

### 💡 For Best Results

1. **Provide Detailed Answers** - Longer, thoughtful answers get better ratings
2. **Stay Focused** - Don't switch tabs during interviews
3. **Complete All Questions** - Skipping hurts your completion rate
4. **Review Feedback** - Use recommendations to improve

### 📊 Understanding Limits

- **24-Hour Limit**: 2 interviews per day
- **Total Limit**: 5 interviews maximum
- **Reset**: 24-hour limit resets after 24 hours
- **Purpose**: Prevents system abuse, encourages quality

### 🎯 Performance Ratings

- **Excellent**: 90%+ completion, detailed answers
- **Good**: 70%+ completion, solid answers
- **Fair**: 50%+ completion
- **Needs Improvement**: <50% completion

---

## File Structure

```
codewave/
├── auth_app.py              ← Enhanced server (USE THIS)
├── app.py                   ← Basic server
├── train_model.py           ← Model training
├── interview_questions.csv  ← Dataset
├── requirements.txt         ← Dependencies
├── templates/               ← HTML files
│   ├── login.html
│   ├── auth_interview.html
│   └── interview.html
└── static/                  ← CSS & JS
    ├── css/
    └── js/
```

---

## Next Steps

1. ✅ Install dependencies
2. ✅ Train the model
3. ✅ Start the server
4. ✅ Create an account
5. ✅ Take your first interview!

**Happy Interviewing! 🎯**

---

## Need Help?

- Check `ENHANCED_README.md` for detailed documentation
- Review code comments
- Test with sample data
