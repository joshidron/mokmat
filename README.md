# 🎯 AI Interview System

A powerful, **completely free** AI-powered interview platform that uses machine learning to conduct intelligent interviews. No API costs, no third-party services - everything runs locally on your machine!

## ✨ Features

- 🤖 **AI-Powered Question Selection** - Smart question selection based on role, category, and difficulty
- 📊 **Machine Learning Model** - Trained locally using scikit-learn (no API costs!)
- 🎨 **Beautiful UI** - Modern, responsive interface with smooth animations
- 📈 **Progress Tracking** - Real-time progress monitoring during interviews
- 💾 **Results Export** - Download interview results as text files
- 🔄 **Adaptive Difficulty** - Questions adapt based on performance
- 🎓 **Multiple Categories** - Technical and Behavioral questions
- 🌟 **Premium Design** - Vibrant gradients, glassmorphism, and micro-animations

## 📦 What's Included

- **600+ Interview Questions** covering:
  - Technical concepts (data structures, algorithms, OOP, etc.)
  - Behavioral scenarios (leadership, teamwork, problem-solving)
  - Multiple difficulty levels (easy, medium, hard)

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
- Load the question dataset
- Train the ML model
- Save the trained model to the `model/` directory
- Display training statistics

### 3. Start the Server

```bash
python app.py
```

### 4. Open Your Browser

Navigate to: `http://localhost:5000`

## 🎮 How to Use

### Starting an Interview

1. **Select Role**: Choose between Software Engineer or HR
2. **Select Category**: Technical or Behavioral questions
3. **Choose Difficulty**: Easy, Medium, Hard, or Mixed
4. **Set Number of Questions**: Choose how many questions (1-20)
5. **Click "Start Interview"**

### During the Interview

- Read each question carefully
- Type your answer in the text area
- Click "Submit Answer" to move to the next question
- Or click "Skip Question" if you want to skip
- Track your progress with the progress bar

### After the Interview

- View your completion statistics
- Review all questions and answers
- Download results as a text file
- Start a new interview anytime

## 🏗️ Project Structure

```
codewave/
├── app.py                      # Flask backend server
├── train_model.py              # ML model training script
├── interview_questions.csv     # Dataset (600+ questions)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── model/                      # Trained model files (generated)
│   ├── vectorizer.pkl
│   ├── difficulty_classifier.pkl
│   ├── category_classifier.pkl
│   └── questions_db.csv
├── templates/
│   └── interview.html          # Main HTML template
└── static/
    ├── css/
    │   └── interview.css       # Premium styles
    └── js/
        └── interview.js        # Frontend logic
```

## 🔧 Technical Details

### Machine Learning Model

- **Algorithm**: Random Forest Classifier
- **Features**: TF-IDF vectorization of questions
- **Tasks**: 
  - Difficulty prediction
  - Category classification
  - Follow-up question generation

### Backend API

- **Framework**: Flask
- **Endpoints**:
  - `POST /api/start-interview` - Start new session
  - `GET /api/get-question/<session_id>` - Get current question
  - `POST /api/submit-answer/<session_id>` - Submit answer
  - `GET /api/get-results/<session_id>` - Get interview results
  - `POST /api/predict-difficulty` - Predict question difficulty
  - `GET /api/stats` - Get system statistics

### Frontend

- **Pure JavaScript** - No frameworks required
- **Modern CSS** - Gradients, animations, glassmorphism
- **Responsive Design** - Works on all screen sizes
- **Smooth Animations** - Enhanced user experience

## 🎨 Design Philosophy

This project follows modern web design principles:

- **Vibrant Colors**: HSL-based color system for harmony
- **Dark Mode**: Easy on the eyes for long sessions
- **Micro-animations**: Smooth transitions and hover effects
- **Glassmorphism**: Modern, premium aesthetic
- **Typography**: Inter font for clarity and professionalism

## 📊 Dataset Statistics

- **Total Questions**: 600+
- **Categories**: Technical, Behavioral
- **Roles**: Software Engineer, HR
- **Difficulty Levels**: Easy, Medium, Hard
- **Question Types**:
  - Comparison questions ("Explain the difference between...")
  - Definition questions ("What is... and how is it used?")
  - Internal workings ("How does... work internally?")
  - Importance questions ("Why is... important?")
  - Scenario questions ("When would you use...?")
  - Behavioral questions ("Describe a time when...")

## 🔒 Privacy & Cost

- ✅ **100% Free** - No API costs or subscriptions
- ✅ **Runs Locally** - All data stays on your machine
- ✅ **No Internet Required** - After initial setup
- ✅ **Open Source** - Modify and extend as needed

## 🛠️ Customization

### Adding Your Own Questions

Edit `interview_questions.csv` and add rows in this format:

```csv
question,role,category,difficulty
"Your question here",Software Engineer,Technical,medium
```

Then retrain the model:

```bash
python train_model.py
```

### Modifying the UI

- **Colors**: Edit CSS variables in `static/css/interview.css`
- **Layout**: Modify `templates/interview.html`
- **Behavior**: Update `static/js/interview.js`

## 🐛 Troubleshooting

### Model Not Found Error

If you see "Model not found" error:
1. Make sure you ran `python train_model.py` first
2. Check that the `model/` directory exists
3. Verify all `.pkl` files are present

### Port Already in Use

If port 5000 is busy, edit `app.py` and change:

```python
app.run(debug=True, port=5000)  # Change 5000 to another port
```

### Dependencies Installation Failed

Try installing packages individually:

```bash
pip install flask
pip install flask-cors
pip install pandas
pip install scikit-learn
```

## 🚀 Future Enhancements

Potential features to add:

- [ ] Voice recording for answers
- [ ] Timer for each question
- [ ] Scoring system with AI evaluation
- [ ] Multi-language support
- [ ] Video interview mode
- [ ] Interview templates for different roles
- [ ] Analytics dashboard
- [ ] Export to PDF

## 📝 License

This project is free to use and modify for personal and commercial purposes.

## 🙏 Credits

Built with:
- Flask (Web framework)
- scikit-learn (Machine learning)
- Pandas (Data processing)
- Pure CSS & JavaScript (Frontend)

---

**Made with ❤️ for developers who want a free, powerful interview system**

Need help? Have questions? Feel free to reach out!
