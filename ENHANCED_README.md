# 🎯 AI Interview System - Enhanced Edition

A powerful, **completely free** AI-powered interview platform with advanced features including user authentication, interview limits, tab switching detection, and dynamic performance reports. No API costs, no third-party services - everything runs locally!

## ✨ Key Features

### 🔐 **User Authentication**
- Secure login and registration system
- Session management
- User-specific interview tracking

### 📊 **Interview Limits**
- **2 interviews per 24 hours** - Prevents system abuse
- **5 total interviews maximum** - Lifetime limit per user
- Real-time limit tracking and display

### 👁️ **Tab Switching Detection**
- Monitors when users switch tabs during interviews
- Records tab switches in the database
- Displays warnings to keep users focused
- Includes tab switch count in final report

### 📈 **Dynamic Report Generation**
- Performance ratings (Excellent, Good, Fair, Needs Improvement)
- Completion rate analysis
- Average answer length tracking
- Personalized strengths identification
- Custom recommendations based on performance
- Tab switching warnings in reports

### 🎨 **Premium UI/UX**
- Modern, responsive design
- Smooth animations and transitions
- Vibrant color gradients
- Real-time progress tracking
- User-friendly interface

### 🤖 **AI-Powered Features**
- Smart question selection based on role and difficulty
- 600+ interview questions
- Machine learning model (trained locally)
- Technical and Behavioral categories

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Train the Model

```bash
python train_model.py
```

This will:
- Load 600+ interview questions
- Train the ML model using scikit-learn
- Save the model to `model/` directory
- Display training statistics

### 3. Start the Enhanced Server

```bash
python auth_app.py
```

### 4. Open Your Browser

Navigate to: `http://localhost:5000`

You'll be redirected to the login page if not authenticated.

## 📖 How to Use

### First Time Setup

1. **Register an Account**
   - Click "Register" tab
   - Enter username, email, and password (min 6 characters)
   - Click "Create Account"

2. **Login**
   - Enter your username and password
   - Click "Login"

### Starting an Interview

1. **Check Your Limits**
   - View remaining interviews (24h and total)
   - Displayed on the setup screen

2. **Select Your Role**
   - Choose between Software Engineer or HR Professional
   - This determines the type of questions you'll receive

3. **Configure Interview**
   - **Category**: Technical or Behavioral
   - **Difficulty**: Easy, Medium, Hard, or Mixed
   - **Number of Questions**: 1-10 questions

4. **Start Interview**
   - Click "Start Interview"
   - Interview begins immediately

### During the Interview

- **Stay Focused**: Don't switch tabs! The system detects this
- **Read Carefully**: Take time to understand each question
- **Type Your Answer**: Provide detailed responses
- **Submit**: Click "Submit Answer" or press Ctrl+Enter
- **Skip**: You can skip questions if needed
- **Track Progress**: Progress bar shows your completion status

### After the Interview

1. **View Performance Report**
   - Performance rating (Excellent/Good/Fair/Needs Improvement)
   - Completion rate percentage
   - Average answer length
   - Tab switching warnings (if any)

2. **Review Feedback**
   - Personalized strengths
   - Custom recommendations
   - Detailed feedback on performance

3. **Check Answers**
   - Review all questions and your answers
   - See timestamps for each response

4. **Download Results**
   - Click "Download Results" for a text file
   - Includes complete report and all answers

5. **Start New Interview**
   - If limits allow, start another interview
   - Limits reset after 24 hours

## 🏗️ Project Structure

```
codewave/
├── auth_app.py                 # Enhanced Flask backend with authentication
├── train_model.py              # ML model training script
├── interview_questions.csv     # Dataset (600+ questions)
├── requirements.txt            # Python dependencies
├── interview_system.db         # SQLite database (auto-created)
├── README.md                   # This file
├── model/                      # Trained model files
│   ├── vectorizer.pkl
│   ├── difficulty_classifier.pkl
│   ├── category_classifier.pkl
│   └── questions_db.csv
├── templates/
│   ├── login.html              # Login/Register page
│   └── auth_interview.html     # Main interview interface
└── static/
    ├── css/
    │   ├── auth.css            # Authentication styles
    │   └── interview.css       # Interview interface styles
    └── js/
        ├── auth.js             # Authentication logic
        └── auth_interview.js   # Enhanced interview logic with tab detection
```

## 🔧 Technical Details

### Database Schema

**Users Table**
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email
- `password_hash`: SHA-256 hashed password
- `created_at`: Registration timestamp
- `total_interviews`: Total interviews completed

**Interview Sessions Table**
- `id`: Primary key
- `user_id`: Foreign key to users
- `session_id`: Unique session identifier
- `role`: Selected role (Software Engineer/HR)
- `category`: Technical/Behavioral
- `difficulty`: easy/medium/hard/mixed
- `total_questions`: Number of questions
- `completed`: Boolean completion status
- `tab_switches`: Number of tab switches detected
- `start_time`: Interview start timestamp
- `end_time`: Interview end timestamp

**Answers Table**
- `id`: Primary key
- `session_id`: Foreign key to sessions
- `question`: Question text
- `answer`: User's answer
- `timestamp`: Answer submission time

### API Endpoints

**Authentication**
- `POST /api/register` - Register new user
- `POST /api/login` - Login user
- `POST /api/logout` - Logout user

**Interview Management**
- `GET /api/check-limits` - Check interview limits
- `POST /api/start-interview` - Start new interview
- `GET /api/get-question/<session_id>` - Get current question
- `POST /api/submit-answer/<session_id>` - Submit answer
- `POST /api/report-tab-switch/<session_id>` - Report tab switch
- `GET /api/get-results/<session_id>` - Get interview results

**User Stats**
- `GET /api/user-stats` - Get user statistics

### Tab Detection

The system uses multiple methods to detect tab switching:

1. **Visibility API**: Detects when page becomes hidden
2. **Window Blur**: Detects when window loses focus
3. **Real-time Reporting**: Immediately sends tab switch events to server
4. **Visual Warnings**: Shows warning banner when detected
5. **Report Integration**: Includes tab switches in final report

### Dynamic Report Generation

Reports are generated based on:

- **Completion Rate**: Percentage of questions answered
- **Answer Quality**: Average answer length
- **Tab Switches**: Number of focus losses
- **Response Time**: Time between answers
- **Participation**: Skipped vs answered questions

Performance levels:
- **Excellent**: 90%+ completion, detailed answers (>100 chars)
- **Good**: 70%+ completion, solid answers (>50 chars)
- **Fair**: 50%+ completion
- **Needs Improvement**: <50% completion

## 🎨 Customization

### Adding Questions

Edit `interview_questions.csv`:

```csv
question,role,category,difficulty
"Your custom question",Software Engineer,Technical,medium
```

Then retrain:
```bash
python train_model.py
```

### Modifying Limits

Edit `auth_app.py`:

```python
# Change these values in can_start_interview() function
last_24h < 2  # Change 2 to your desired 24h limit
total < 5     # Change 5 to your desired total limit
```

### Customizing UI

- **Colors**: Edit CSS variables in `static/css/interview.css`
- **Layout**: Modify `templates/auth_interview.html`
- **Behavior**: Update `static/js/auth_interview.js`

## 🔒 Security Features

- ✅ **Password Hashing**: SHA-256 encryption
- ✅ **Session Management**: Secure Flask sessions
- ✅ **SQL Injection Protection**: Parameterized queries
- ✅ **User Isolation**: Users can only access their own data
- ✅ **Rate Limiting**: Interview limits prevent abuse

## 📊 Interview Limits Explained

### 24-Hour Limit (2 interviews)
- Resets every 24 hours from first interview
- Prevents system overload
- Encourages quality over quantity

### Total Limit (5 interviews)
- Lifetime maximum per user
- Can be adjusted in code
- Prevents unlimited usage

### Checking Limits
- Displayed on setup screen
- Real-time updates
- Clear error messages when limits reached

## 🐛 Troubleshooting

### "Interview limit reached" Error

**Solution**: 
- Wait 24 hours for daily limit reset
- Or contact admin to reset total limit

### Tab Detection Too Sensitive

**Solution**:
- Stay on the interview tab
- Don't use other applications during interview
- Tab switches are recorded but don't stop the interview

### Model Not Found

**Solution**:
```bash
python train_model.py
```

### Database Errors

**Solution**:
Delete `interview_system.db` and restart server (will recreate database)

### Port Already in Use

**Solution**:
Edit `auth_app.py`:
```python
app.run(debug=True, port=5001)  # Change port
```

## 📈 Future Enhancements

Potential features to add:

- [ ] Email verification
- [ ] Password reset functionality
- [ ] Admin dashboard
- [ ] Interview analytics
- [ ] Export to PDF
- [ ] Voice recording
- [ ] Video interview mode
- [ ] AI answer evaluation
- [ ] Multi-language support
- [ ] Interview scheduling
- [ ] Peer review system

## 🎯 Use Cases

### For Job Seekers
- Practice interview skills
- Get instant feedback
- Track progress over time
- Prepare for real interviews

### For Recruiters
- Screen candidates
- Standardize interview process
- Generate performance reports
- Track candidate responses

### For Educators
- Assess student knowledge
- Create practice exams
- Monitor student progress
- Generate performance analytics

## 📝 License

This project is free to use and modify for personal and commercial purposes.

## 🙏 Credits

Built with:
- **Flask** - Web framework
- **scikit-learn** - Machine learning
- **Pandas** - Data processing
- **SQLite** - Database
- **Pure CSS & JavaScript** - Frontend

---

**Made with ❤️ for developers who want a free, powerful, and feature-rich interview system**

## 🆘 Support

Need help? Have questions?
- Check the troubleshooting section
- Review the code comments
- Test with the provided dataset

**Happy Interviewing! 🎯**
