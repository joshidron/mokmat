# 🎯 AI Interview System - Enhanced Tracking & Voice Recognition

## Overview
A comprehensive AI-powered interview system with advanced monitoring capabilities, including full body posture tracking, eye movement analysis, tab switching detection, and voice recognition for hands-free answering.

## 🚀 New Features

### 1. **Voice Recognition for Answers** 🎤
- **Speech-to-Text**: Answer questions using your voice instead of typing
- **Real-time Transcription**: See your words appear as you speak
- **Multi-language Support**: Supports English (US, UK, India), Hindi, Spanish, French, German, Chinese, Japanese, Korean
- **Continuous Listening**: Keeps listening until you stop
- **Interim Results**: Shows what you're saying in real-time
- **Error Handling**: Graceful handling of microphone issues

**How to Use:**
1. Click the "🎤 Start Speaking" button
2. Speak your answer clearly
3. Click "Stop Speaking" when done
4. Your answer will appear in the text area
5. Submit as normal

### 2. **Full Body Posture Tracking** 🧍
- **Real-time Pose Detection**: Uses MediaPipe Pose to track your body
- **Posture Metrics**:
  - Shoulder alignment (detects slouching)
  - Head tilt angle
  - Body center position (detects leaning)
  - Distance from camera
- **Visual Feedback**: Green skeleton overlay on video
- **Posture Score**: 0-100% rating displayed in dashboard
- **Violation Detection**: Logs poor posture incidents

**Posture Requirements:**
- ✅ Sit upright with level shoulders
- ✅ Keep head straight (minimal tilt)
- ✅ Stay centered in frame
- ✅ Maintain appropriate distance from camera

### 3. **Advanced Eye Movement Tracking** 👁️
- **Gaze Direction**: Tracks where you're looking (left, right, up, down, center)
- **Focus Percentage**: Measures how often you look at the camera
- **Blink Rate Monitoring**: Detects stress indicators
- **Gaze Stability**: Measures eye movement frequency
- **Eye Contact Score**: Real-time percentage display

**Eye Tracking Metrics:**
- Focus percentage (should be >75%)
- Gaze direction (should be "center")
- Blink rate (normal: <30 blinks/min)
- Gaze stability score

### 4. **Tab Switching Detection** ⚠️
- **3-Strike Warning System**:
  - **1st Violation**: Warning message
  - **2nd Violation**: Final warning with countdown
  - **3rd Violation**: Interview terminated + 24-hour ban
- **Multiple Detection Methods**:
  - Page Visibility API
  - Window blur/focus events
  - Keyboard shortcut detection (Alt+Tab, Cmd+Tab)
  - Mouse leave detection
- **Visual & Audio Warnings**: Modal popups with sound alerts
- **Automatic Termination**: Prevents cheating

### 5. **Interview Attempt Limits** 📊
- **Daily Limit**: Maximum 2 interviews per 24 hours
- **Total Limit**: Maximum 5 interviews (lifetime)
- **Ban System**: 24-hour cooldown after violations
- **Real-time Display**: Shows remaining attempts
- **Persistent Tracking**: Stored in database

### 6. **Comprehensive Monitoring Dashboard** 📈
- **Real-time Metrics Display**:
  - Posture indicator (🧍)
  - Eye contact score (👁️)
  - Engagement score (overall)
  - Tab switch counter
- **Color-coded Status**: Green (good), Yellow (fair), Red (poor)
- **Fixed Position**: Always visible during interview
- **Responsive Design**: Adapts to mobile devices

## 🛠️ Technical Implementation

### Frontend Technologies
```javascript
// AI/ML Models
- TensorFlow.js (core ML framework)
- MediaPipe Face Mesh (eye tracking)
- MediaPipe Pose (body tracking)

// Browser APIs
- Web Speech API (voice recognition)
- Page Visibility API (tab detection)
- MediaDevices API (camera/microphone)
- Canvas API (visual overlays)
```

### Backend Technologies
```python
# Flask Server
- SQLite database
- Session management
- RESTful API endpoints
- Real-time event logging
```

### Database Schema
```sql
-- Enhanced interview_sessions table
CREATE TABLE interview_sessions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    session_id TEXT UNIQUE,
    role TEXT,
    category TEXT,
    difficulty TEXT,
    total_questions INTEGER,
    completed BOOLEAN,
    tab_switches INTEGER DEFAULT 0,
    posture_violations INTEGER DEFAULT 0,
    eye_tracking_score REAL DEFAULT 0.0,
    focus_percentage REAL DEFAULT 0.0,
    terminated BOOLEAN DEFAULT 0,
    terminated_reason TEXT,
    warning_count INTEGER DEFAULT 0,
    start_time TIMESTAMP,
    end_time TIMESTAMP
);

-- Tracking events table
CREATE TABLE tracking_events (
    id INTEGER PRIMARY KEY,
    session_id TEXT,
    event_type TEXT,  -- 'tab_switch', 'posture_violation', 'eye_wander', etc.
    timestamp TIMESTAMP,
    details TEXT
);

-- User violations table
CREATE TABLE user_violations (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    violation_type TEXT,
    violation_time TIMESTAMP,
    ban_until TIMESTAMP
);
```

## 📋 API Endpoints

### New Endpoints
```
POST /api/track-event/<session_id>
- Log tracking events (posture, eye movement, etc.)
- Body: { event_type, details }

POST /api/update-tracking-metrics/<session_id>
- Update real-time metrics
- Body: { eye_tracking_score, focus_percentage }

POST /api/report-tab-switch/<session_id>
- Report tab switching (3-strike system)
- Returns: { warning, terminated, ban_until }

GET /api/check-limits
- Check if user can start interview
- Returns: { can_start, remaining_24h, remaining_total, ban_until }
```

## 🎮 Usage Instructions

### Starting an Interview

1. **Login** to your account
2. **Check Limits**: View remaining interview attempts
3. **Test Camera & Microphone**: Click "Test Camera & Microphone"
4. **Read Requirements**: Review monitoring requirements
5. **Configure Interview**: Select role, category, difficulty, questions
6. **Start Interview**: Click "Start Interview"

### During the Interview

1. **Position Yourself**:
   - Sit upright in front of camera
   - Ensure full upper body is visible
   - Look at the camera
   - Stay in frame

2. **Answer Questions**:
   - **Option A (Voice)**: Click "🎤 Start Speaking" and speak your answer
   - **Option B (Text)**: Type your answer in the text area
   - Click "Submit Answer" when ready

3. **Monitor Your Performance**:
   - Check the monitoring dashboard (top-right)
   - Maintain good posture (green indicator)
   - Keep eye contact (>75% focus)
   - Avoid switching tabs

4. **Warnings**:
   - If you receive a warning, acknowledge it immediately
   - Correct your behavior to avoid termination
   - 3 violations = automatic termination + ban

### After the Interview

1. **View Results**: Comprehensive report with all metrics
2. **Download Report**: Save your results as PDF
3. **Start New Interview**: If attempts remaining

## ⚙️ Configuration

### Voice Recognition Languages
```javascript
const VOICE_LANGUAGES = {
    'en-US': 'English (US)',
    'en-GB': 'English (UK)',
    'en-IN': 'English (India)',
    'hi-IN': 'Hindi',
    'es-ES': 'Spanish',
    'fr-FR': 'French',
    'de-DE': 'German',
    'zh-CN': 'Chinese',
    'ja-JP': 'Japanese',
    'ko-KR': 'Korean'
};
```

### Detection Thresholds
```javascript
// Posture Tracking
shoulderAngle: 15°      // Max shoulder tilt
headTilt: 20°           // Max head tilt
centerOffset: 0.2       // 20% of frame
minFaceSize: 0.15       // 15% of frame
maxFaceSize: 0.40       // 40% of frame

// Eye Tracking
gazeWanderTime: 3000ms  // 3 seconds
focusLossTime: 5000ms   // 5 seconds
maxBlinkRate: 30        // blinks per minute

// Tab Switching
maxWarnings: 3          // 3 strikes
banDuration: 24h        // 24 hours
```

## 🔒 Privacy & Security

### Data Handling
- ✅ All video/audio processing done **locally** in browser
- ✅ No video/audio data sent to server
- ✅ Only metrics and events logged to database
- ✅ User consent required before monitoring
- ✅ Clear disclosure of what's being tracked

### User Rights
- Right to know what's being monitored
- Right to decline (cannot proceed with interview)
- Right to review tracking data
- Right to delete account and data

## 🐛 Troubleshooting

### Camera Not Working
**Issue**: Camera unavailable or not detected

**Solutions**:
1. Check browser permissions (Settings → Privacy → Camera)
2. Ensure no other app is using the camera
3. Try refreshing the page
4. Use HTTPS (required in production)
5. Try a different browser (Chrome recommended)

### Microphone Not Working
**Issue**: Voice recognition not working

**Solutions**:
1. Check browser permissions (Settings → Privacy → Microphone)
2. Test microphone in system settings
3. Ensure microphone is not muted
4. Try a different browser
5. Check if Web Speech API is supported

### Posture Not Detected
**Issue**: Posture tracking not working

**Solutions**:
1. Ensure full upper body is visible
2. Improve lighting conditions
3. Move closer to camera
4. Remove obstructions
5. Check if MediaPipe Pose loaded correctly

### Eye Tracking Inaccurate
**Issue**: Eye tracking shows incorrect gaze direction

**Solutions**:
1. Look directly at camera
2. Improve lighting (avoid backlighting)
3. Ensure face is clearly visible
4. Remove glasses if causing issues
5. Calibrate by looking at camera

### False Tab Switch Warnings
**Issue**: Getting warnings without switching tabs

**Solutions**:
1. Disable browser notifications
2. Close other applications
3. Don't click outside browser window
4. Avoid using Alt+Tab or Cmd+Tab
5. Keep browser in focus

## 📊 Performance Metrics

### System Requirements
- **Browser**: Chrome 90+, Edge 90+, Safari 14+, Firefox 88+
- **Camera**: 720p or higher recommended
- **Microphone**: Any working microphone
- **Internet**: Stable connection for loading models
- **CPU**: Modern processor (for AI models)
- **RAM**: 4GB+ recommended

### Model Sizes
- MediaPipe Face Mesh: ~5-10 MB
- MediaPipe Pose: ~10-15 MB
- Total initial load: ~20-25 MB
- Cached after first use

### Detection Performance
- Face detection: 30-60 FPS
- Pose detection: 15-30 FPS
- Eye tracking: 30-60 FPS
- Voice recognition: Real-time

## 🚀 Getting Started

### Installation

1. **Clone Repository**:
```bash
git clone https://github.com/yourusername/ai-interview-system.git
cd ai-interview-system
```

2. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run Server**:
```bash
python auth_app.py
```

4. **Access Application**:
```
http://localhost:5000
```

### First Time Setup

1. Register a new account
2. Login with credentials
3. Test camera and microphone
4. Start your first interview
5. Experience all tracking features!

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please read CONTRIBUTING.md first.

## 📧 Support

For issues or questions:
- GitHub Issues: [Create an issue](https://github.com/yourusername/ai-interview-system/issues)
- Email: support@example.com

---

**Built with ❤️ using TensorFlow.js, MediaPipe, and Flask**
