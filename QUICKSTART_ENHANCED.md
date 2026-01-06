# 🚀 Quick Start Guide - Enhanced AI Interview System

## Prerequisites
- Python 3.8 or higher
- Modern web browser (Chrome, Edge, Safari, or Firefox)
- Webcam and microphone
- Internet connection (for loading AI models)

## Installation Steps

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- Flask-CORS (cross-origin support)
- Pandas & NumPy (data processing)
- Scikit-learn (ML models)
- Authlib (OAuth support)

### 2. Initialize Database
The database will be automatically created when you first run the server.

### 3. Run the Server
```bash
python auth_app.py
```

You should see:
```
============================================================
🚀 ENHANCED INTERVIEW SYSTEM SERVER
============================================================

📡 Server starting on http://localhost:5000
   Features:
   ✅ User Authentication
   ✅ Interview Limits (2/24h, 5 total)
   ✅ Tab Switching Detection (3-strike system)
   ✅ Body Posture Tracking
   ✅ Eye Movement Tracking
   ✅ Comprehensive Monitoring
   ✅ Dynamic Report Generation

============================================================
```

### 4. Access the Application
Open your browser and navigate to:
```
http://localhost:5000
```

## First Time User Flow

### 1. Register Account
- Click "Register" on the login page
- Enter username, email, and password
- Click "Create Account"

### 2. Login
- Enter your credentials
- Click "Login"

### 3. Test Camera & Microphone
- On the setup screen, click "Test Camera & Microphone"
- Grant browser permissions when prompted
- Verify you see "✅ Camera and microphone working!"

### 4. Configure Interview
- Select your role (e.g., Software Engineer)
- Choose category (Technical or Behavioral)
- Select difficulty level
- Set number of questions (1-10)

### 5. Start Interview
- Review monitoring requirements
- Click "Start Interview"
- Wait for tracking systems to initialize

### 6. Answer Questions

**Using Voice (Recommended)**:
1. Click "🎤 Start Speaking"
2. Speak your answer clearly
3. Watch the real-time transcription
4. Click "Stop Speaking" when done
5. Review the text, edit if needed
6. Click "Submit Answer"

**Using Text**:
1. Type your answer in the text area
2. Click "Submit Answer"

### 7. Monitor Your Performance
Watch the monitoring dashboard (top-right) for:
- **Posture Score**: Keep it green (>75%)
- **Eye Contact**: Maintain focus on camera
- **Engagement Score**: Overall performance
- **Tab Switches**: Keep at 0!

### 8. Complete Interview
- Answer all questions
- View comprehensive results
- Download your report (optional)

## Important Rules

### ⚠️ Monitoring Requirements

**DO:**
- ✅ Sit upright with good posture
- ✅ Look at the camera
- ✅ Stay centered in frame
- ✅ Keep the interview tab in focus
- ✅ Speak clearly for voice recognition

**DON'T:**
- ❌ Switch tabs or windows
- ❌ Slouch or lean excessively
- ❌ Look away from camera for extended periods
- ❌ Move out of frame
- ❌ Use Alt+Tab or Cmd+Tab

### 🚨 Violation Consequences

**Tab Switching (3-Strike System)**:
- **1st Violation**: Warning message
- **2nd Violation**: Final warning
- **3rd Violation**: Interview terminated + 24-hour ban

**Interview Limits**:
- **Daily**: Maximum 2 interviews per 24 hours
- **Total**: Maximum 5 interviews (lifetime)
- **Ban**: 24-hour cooldown after violations

## Troubleshooting

### Camera Permission Denied
```
Error: Camera or microphone not accessible
```
**Solution**:
1. Click the camera icon in browser address bar
2. Select "Always allow"
3. Refresh the page

### Microphone Not Working
```
Error: Microphone permission denied
```
**Solution**:
1. Check browser settings → Privacy → Microphone
2. Enable microphone for localhost
3. Test microphone in system settings
4. Refresh the page

### Models Not Loading
```
Error: Failed to initialize monitoring
```
**Solution**:
1. Check internet connection
2. Clear browser cache
3. Try a different browser
4. Disable browser extensions

### Voice Recognition Not Supported
```
Warning: Speech Recognition not supported
```
**Solution**:
- Use Chrome, Edge, or Safari (Firefox has limited support)
- Enable Web Speech API in browser settings
- Fall back to text input

## Browser Compatibility

### Fully Supported ✅
- **Chrome** 90+ (Recommended)
- **Edge** 90+
- **Safari** 14+

### Partially Supported ⚠️
- **Firefox** 88+ (Voice recognition limited)

### Not Supported ❌
- Internet Explorer
- Opera Mini
- Older browser versions

## Performance Tips

### For Best Experience:
1. **Close Other Tabs**: Reduce CPU/memory usage
2. **Good Lighting**: Improves face/pose detection
3. **Stable Internet**: For loading AI models
4. **Wired Connection**: More reliable than WiFi
5. **Quiet Environment**: Better voice recognition

### System Requirements:
- **CPU**: Modern processor (2015+)
- **RAM**: 4GB minimum, 8GB recommended
- **Camera**: 720p or higher
- **Internet**: 5 Mbps or faster

## Advanced Configuration

### Change Voice Language
Edit `voice_recognition.js`:
```javascript
this.recognition.lang = 'en-US';  // Change to your language
```

Supported languages:
- `en-US` - English (US)
- `en-GB` - English (UK)
- `en-IN` - English (India)
- `hi-IN` - Hindi
- `es-ES` - Spanish
- `fr-FR` - French
- `de-DE` - German
- `zh-CN` - Chinese
- `ja-JP` - Japanese
- `ko-KR` - Korean

### Adjust Detection Thresholds
Edit `pose_tracking.js` or `eye_tracking.js`:
```javascript
this.thresholds = {
    shoulderAngle: 15,  // Increase for more lenient posture
    headTilt: 20,       // Increase for more head movement
    gazeWanderTime: 3000,  // Increase for longer gaze wander
    // ... etc
};
```

### Disable Specific Tracking
Edit `interview_monitor.js`:
```javascript
// Comment out to disable
// this.postureTracker = new PostureTracker(...);
// this.eyeTracker = new EyeTracker(...);
```

## Database Management

### View Database
```bash
sqlite3 interview_system.db
```

### Common Queries
```sql
-- View all users
SELECT * FROM users;

-- View interview sessions
SELECT * FROM interview_sessions;

-- View tracking events
SELECT * FROM tracking_events;

-- Check user violations
SELECT * FROM user_violations;

-- Reset user interview count
UPDATE users SET total_interviews = 0 WHERE username = 'testuser';

-- Remove ban
DELETE FROM user_violations WHERE user_id = 1;
```

### Backup Database
```bash
cp interview_system.db interview_system_backup.db
```

## Development Mode

### Enable Debug Mode
In `auth_app.py`:
```python
app.run(debug=True, port=5000, host='0.0.0.0')
```

### View Console Logs
- Open browser DevTools (F12)
- Check Console tab for tracking logs
- Check Network tab for API calls

### Test Without Limits
Temporarily disable limits in `auth_app.py`:
```python
def can_start_interview(user_id):
    return {
        'can_start': True,  # Always allow
        # ... rest of the code
    }
```

## Production Deployment

### Important Changes for Production:

1. **Disable Debug Mode**:
```python
app.run(debug=False, port=5000)
```

2. **Use HTTPS**:
- Camera/microphone require HTTPS in production
- Use SSL certificate (Let's Encrypt)

3. **Set Secret Key**:
```python
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key')
```

4. **Use Production Database**:
- Consider PostgreSQL or MySQL
- Set up proper backups

5. **Configure OAuth**:
```python
app.config['GOOGLE_CLIENT_ID'] = os.environ.get('GOOGLE_CLIENT_ID')
app.config['GOOGLE_CLIENT_SECRET'] = os.environ.get('GOOGLE_CLIENT_SECRET')
```

## Support

### Getting Help
- 📖 Read `ENHANCED_FEATURES_README.md` for detailed documentation
- 🐛 Check `ENHANCED_TRACKING_IMPLEMENTATION.md` for technical details
- 💬 Create GitHub issue for bugs
- 📧 Email support for questions

### Reporting Issues
Include:
1. Browser name and version
2. Operating system
3. Error message (if any)
4. Steps to reproduce
5. Screenshots (if applicable)

---

**Ready to start? Run `python auth_app.py` and open http://localhost:5000**

🎉 **Good luck with your interviews!**
