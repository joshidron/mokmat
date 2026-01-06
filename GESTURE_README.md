# 🎯 Live Camera Gesture Recognition System

## Overview

This is a comprehensive **Python-based live camera gesture recognition system** designed for your interview application. It uses **OpenCV**, **MediaPipe**, and **Flask** to provide real-time detection of facial expressions, hand gestures, and body posture.

## ✨ Features

### Gesture Detection Capabilities

| Gesture | Description | Use Case |
|---------|-------------|----------|
| 😊 **Smile Detection** | Analyzes mouth landmarks to detect smiles | Measures positivity and engagement |
| 👁️ **Eye Contact** | Tracks gaze direction | Assesses confidence and attention |
| 👍 **Thumbs Up** | Recognizes thumbs up hand gesture | Positive feedback indicator |
| 👋 **Wave** | Detects hand waving motion | Greeting or acknowledgment |
| 🤔 **Thinking Pose** | Identifies hand near face | Shows contemplation |
| 📐 **Posture Analysis** | Monitors body alignment | Confidence vs slouching |
| 🔄 **Head Nod** | Tracks vertical head movement | Agreement indicator |
| 😰 **Nervous Gestures** | Detects fidgeting | Stress level indicator |

### Technical Features

- ✅ **Real-time Processing** - 30-60 FPS on modern hardware
- ✅ **Multi-modal Detection** - Face, hands, and body pose
- ✅ **REST API** - Easy integration with any frontend
- ✅ **Video Streaming** - MJPEG stream with gesture overlays
- ✅ **Session Recording** - Save gesture data as JSON
- ✅ **Engagement Scoring** - Automatic calculation of engagement metrics
- ✅ **Visual Feedback** - On-screen indicators for detected gestures

## 📦 Installation

### Quick Install

Run the automated installer:

```bash
python install_gesture_recognition.py
```

### Manual Install

Install dependencies:

```bash
pip install -r gesture_requirements.txt
```

Or install individually:

```bash
pip install opencv-python mediapipe numpy flask flask-cors
```

## 🚀 Usage

### Option 1: Standalone Mode

Run gesture recognition directly:

```bash
python gesture_recognition.py
```

**Controls:**
- Press `q` to quit
- Press `s` to save session data

### Option 2: API Server Mode

Start the Flask API server:

```bash
python gesture_api.py
```

Or use the batch file:

```bash
start_gesture_api.bat
```

Server runs on: `http://localhost:5001`

### Option 3: Complete System

Start both interview app and gesture API:

```bash
start_complete_system.bat
```

This starts:
- Main Interview App: `http://localhost:5000`
- Gesture API: `http://localhost:5001`

## 🔌 API Endpoints

### Start Recognition
```http
POST /api/gesture/start
Content-Type: application/json

{
  "camera_index": 0
}
```

### Stop Recognition
```http
POST /api/gesture/stop
```

### Get Status
```http
GET /api/gesture/status
```

**Response:**
```json
{
  "success": true,
  "is_running": true,
  "current_gestures": {
    "smile": true,
    "eye_contact": true,
    "thumbs_up": false,
    "wave": false,
    "thinking": false,
    "posture": "confident",
    "nervous": false
  },
  "stats": {
    "duration_seconds": 120.5,
    "total_frames": 3615,
    "fps": 30.0,
    "gestures_detected": {
      "smile": 245,
      "eye_contact": 1820,
      "thumbs_up": 12
    }
  }
}
```

### Video Stream
```http
GET /api/gesture/video_feed
```

Returns MJPEG video stream with gesture overlays.

### Get Current Frame
```http
GET /api/gesture/frame
```

Returns base64-encoded image with gesture data.

### Save Session
```http
POST /api/gesture/save_session
Content-Type: application/json

{
  "filename": "session_123.json"
}
```

### Health Check
```http
GET /api/gesture/health
```

## 🎨 Frontend Integration

### Include JavaScript

Add to your HTML:

```html
<script src="/static/js/python_gesture_integration.js"></script>
```

### Start Gesture Recognition

```javascript
// Start when interview begins
await window.pythonGesture.start();

// Display video feed
const videoElement = document.getElementById('gestureVideo');
videoElement.src = 'http://localhost:5001/api/gesture/video_feed';

// Get real-time updates
setInterval(async () => {
    const summary = window.pythonGesture.getGestureSummary();
    console.log('Engagement Score:', summary.engagementScore);
}, 1000);

// Stop when interview ends
await window.pythonGesture.stop();
```

### Listen for Gesture Events

```javascript
document.addEventListener('gesture-detected', (event) => {
    console.log('Gesture detected:', event.detail.gesture);
    
    // Show notification or update UI
    if (event.detail.gesture === 'smile') {
        showNotification('Great smile! 😊');
    }
});
```

## 📊 Session Data

Gesture data is saved as JSON:

```json
{
  "timestamp": "2026-01-07T00:39:36",
  "duration_seconds": 300.5,
  "total_frames": 9015,
  "fps": 30.0,
  "gestures_detected": {
    "smile": 450,
    "eye_contact": 7200,
    "thumbs_up": 25,
    "wave": 8,
    "thinking": 120,
    "confident_posture": 6500,
    "nervous_gestures": 45,
    "nod": 35
  },
  "gesture_rates": {
    "smile": 90.0,
    "eye_contact": 1440.0
  }
}
```

## 🎯 Integration with Interview System

### Backend Integration

Add to your `app.py`:

```python
import requests

@app.route('/get_results/<session_id>')
def get_results_with_gestures(session_id):
    # ... existing code ...
    
    # Fetch gesture data
    try:
        response = requests.get('http://localhost:5001/api/gesture/stats')
        if response.status_code == 200:
            gesture_data = response.json()
            session_data['gesture_analysis'] = gesture_data['stats']
    except Exception as e:
        print(f"Failed to fetch gesture data: {e}")
    
    return render_template('results.html', data=session_data)
```

### Frontend Integration

Add to `enhanced_interview.html`:

```html
<!-- Gesture Monitoring Panel -->
<div class="gesture-panel">
    <h3>🎯 Gesture Analysis</h3>
    
    <!-- Video Feed -->
    <img id="pythonGestureFeed" src="" alt="Gesture Feed">
    
    <!-- Metrics -->
    <div class="gesture-metrics">
        <div class="metric">
            <span>😊 Smiles:</span>
            <span id="pythonSmileCount">0</span>
        </div>
        <div class="metric">
            <span>👁️ Eye Contact:</span>
            <span id="pythonEyeContact">0%</span>
        </div>
        <div class="metric">
            <span>📐 Posture:</span>
            <span id="pythonPosture">-</span>
        </div>
    </div>
</div>

<!-- Include script -->
<script src="/static/js/python_gesture_integration.js"></script>
```

## 🔧 Configuration

### Camera Settings

Modify in `gesture_recognition.py`:

```python
# Change camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Change FPS
cap.set(cv2.CAP_PROP_FPS, 30)
```

### Detection Sensitivity

Adjust thresholds in `gesture_recognition.py`:

```python
# Smile detection threshold
if smile_ratio > 3.5:  # Lower = more sensitive

# Eye contact threshold
if deviation < eye_distance * 0.15:  # Higher = more lenient

# Head nod threshold
if max_pos - min_pos > 20:  # Lower = more sensitive
```

### API Port

Change in `gesture_api.py`:

```python
app.run(debug=True, port=5001, host='0.0.0.0')
```

## 🐛 Troubleshooting

### Camera Not Found

```bash
# List available cameras
python -c "import cv2; print([i for i in range(10) if cv2.VideoCapture(i).isOpened()])"
```

### Port Already in Use

```bash
# Kill process on port 5001 (Windows)
netstat -ano | findstr :5001
taskkill /PID <PID> /F
```

### Import Errors

```bash
# Reinstall dependencies
pip uninstall opencv-python mediapipe
pip install opencv-python mediapipe
```

### Low FPS

- Reduce camera resolution
- Close other applications
- Use GPU acceleration
- Disable some gesture detections

### CORS Issues

Add to `gesture_api.py`:

```python
from flask_cors import CORS
CORS(app)
```

## 📈 Performance

### System Requirements

- **CPU**: Modern multi-core processor (Intel i5/AMD Ryzen 5 or better)
- **RAM**: 4GB minimum, 8GB recommended
- **Camera**: Any USB webcam or built-in camera
- **OS**: Windows 10/11, Linux, macOS

### Performance Metrics

- **FPS**: 30-60 on modern hardware
- **Latency**: 16-33ms per frame
- **Model Size**: ~10-15 MB (downloaded once)
- **Memory Usage**: ~500MB-1GB

## 📚 File Structure

```
codewave/
├── gesture_recognition.py           # Core gesture detection
├── gesture_api.py                   # Flask API server
├── install_gesture_recognition.py   # Installer script
├── gesture_requirements.txt         # Dependencies
├── GESTURE_INTEGRATION_GUIDE.md    # Integration guide
├── GESTURE_README.md               # This file
├── start_gesture_api.bat           # Start API server
├── start_complete_system.bat       # Start everything
└── static/js/
    └── python_gesture_integration.js # Frontend integration
```

## 🎓 How It Works

### Detection Pipeline

```
Camera Frame
    ↓
Convert to RGB
    ↓
MediaPipe Processing
    ├── Face Mesh (468 landmarks)
    ├── Hand Detection (21 landmarks per hand)
    └── Pose Detection (33 landmarks)
    ↓
Gesture Analysis
    ├── Calculate distances
    ├── Analyze patterns
    └── Detect movements
    ↓
Update UI & Send to API
```

### Gesture Algorithms

**Smile Detection:**
- Measures mouth width-to-height ratio
- Threshold: ratio > 3.5

**Eye Contact:**
- Calculates nose-to-eye-center deviation
- Threshold: deviation < 15% of eye distance

**Head Nod:**
- Tracks nose Y-coordinate over time
- Detects oscillation pattern
- Threshold: 20+ pixels vertical movement

**Thumbs Up:**
- Checks thumb extended upward
- Verifies other fingers curled
- Uses hand landmark positions

## 🔐 Privacy & Security

- ✅ **All processing is local** - No data sent to external servers
- ✅ **No video recording** - Only real-time analysis
- ✅ **Session data only** - Gesture counts and statistics
- ✅ **User control** - Can start/stop anytime
- ✅ **Transparent** - Open source code

## 🚀 Next Steps

1. ✅ Install dependencies
2. ✅ Test standalone system
3. ✅ Start API server
4. ⬜ Integrate with frontend
5. ⬜ Test complete flow
6. ⬜ Customize for your needs
7. ⬜ Deploy to production

## 📞 Support

### Common Issues

1. **Camera not working**: Check permissions and other apps using camera
2. **Low FPS**: Reduce resolution or close other apps
3. **API not connecting**: Ensure server is running on port 5001
4. **Import errors**: Reinstall dependencies

### Debug Mode

Enable detailed logging:

```python
# In gesture_recognition.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📄 License

This gesture recognition system is part of your interview application.

## 🎉 Credits

Built with:
- [OpenCV](https://opencv.org/) - Computer vision
- [MediaPipe](https://google.github.io/mediapipe/) - ML solutions
- [Flask](https://flask.palletsprojects.com/) - Web framework

---

**Ready to get started?** Run `python install_gesture_recognition.py` to begin!
