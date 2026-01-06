# Gesture Recognition Integration Guide

## 🎯 Overview

This guide explains how to integrate the Python-based live camera gesture recognition system with your existing interview application.

## 📦 What's Included

### Python Files
1. **`gesture_recognition.py`** - Core gesture detection system
2. **`gesture_api.py`** - Flask API server for integration
3. **`install_gesture_recognition.py`** - Automated installer
4. **`gesture_requirements.txt`** - Dependencies list

### Features Detected
- 😊 **Smile Detection** - Facial expression analysis
- 👁️ **Eye Contact** - Gaze direction tracking
- 👍 **Thumbs Up** - Hand gesture recognition
- 👋 **Wave** - Hand movement detection
- 🤔 **Thinking Pose** - Hand near face detection
- 📐 **Posture Analysis** - Body alignment tracking
- 🔄 **Head Nod** - Vertical head movement
- 😰 **Nervous Gestures** - Fidgeting detection

## 🚀 Quick Start

### Step 1: Install Dependencies

Run the installation script:
```bash
python install_gesture_recognition.py
```

Or install manually:
```bash
pip install -r gesture_requirements.txt
```

### Step 2: Test Standalone System

Run the standalone gesture recognition:
```bash
python gesture_recognition.py
```

**Controls:**
- Press `q` to quit
- Press `s` to save session data

### Step 3: Start API Server

Run the Flask API server:
```bash
python gesture_api.py
```

The server will start on `http://localhost:5001`

## 🔌 API Integration

### Available Endpoints

#### 1. Start Gesture Recognition
```http
POST /api/gesture/start
Content-Type: application/json

{
  "camera_index": 0
}
```

**Response:**
```json
{
  "success": true,
  "message": "Gesture recognition started"
}
```

#### 2. Stop Gesture Recognition
```http
POST /api/gesture/stop
```

**Response:**
```json
{
  "success": true,
  "message": "Gesture recognition stopped"
}
```

#### 3. Get Current Status
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
      "thumbs_up": 12,
      "wave": 5,
      "thinking": 34,
      "confident_posture": 2100,
      "nervous_gestures": 15
    }
  }
}
```

#### 4. Video Stream
```http
GET /api/gesture/video_feed
```

Returns MJPEG video stream with gesture overlays.

#### 5. Get Current Frame
```http
GET /api/gesture/frame
```

**Response:**
```json
{
  "success": true,
  "frame": "base64_encoded_image_data",
  "gestures": { ... }
}
```

#### 6. Save Session Data
```http
POST /api/gesture/save_session
Content-Type: application/json

{
  "filename": "interview_session_123.json"
}
```

## 🔗 Integration with Interview System

### Option 1: Dual Server Setup (Recommended)

Run both servers simultaneously:
1. Main interview app on port 5000
2. Gesture API on port 5001

**Advantages:**
- Isolated processes
- Easy to debug
- Can restart independently
- Better resource management

### Option 2: Merge into Main App

Add gesture routes to your existing `app.py`:

```python
# Add to app.py
from gesture_api import gesture_api

# Add routes
@app.route('/api/gesture/start', methods=['POST'])
def start_gesture():
    # ... (copy from gesture_api.py)
    pass

# ... (add other routes)
```

### Option 3: Microservices Architecture

Use the gesture API as a separate microservice:
- Deploy on different server/container
- Use HTTP requests for communication
- Scale independently

## 📝 Frontend Integration

### JavaScript Example

```javascript
// Start gesture recognition when interview begins
async function startGestureRecognition() {
    try {
        const response = await fetch('http://localhost:5001/api/gesture/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ camera_index: 0 })
        });
        
        const data = await response.json();
        console.log('Gesture recognition started:', data);
        
        // Start polling for gesture updates
        startGesturePolling();
    } catch (error) {
        console.error('Failed to start gesture recognition:', error);
    }
}

// Poll for gesture updates
let gestureInterval;

function startGesturePolling() {
    gestureInterval = setInterval(async () => {
        try {
            const response = await fetch('http://localhost:5001/api/gesture/status');
            const data = await response.json();
            
            if (data.success) {
                updateGestureUI(data.current_gestures);
                updateGestureStats(data.stats);
            }
        } catch (error) {
            console.error('Failed to get gesture status:', error);
        }
    }, 1000); // Update every second
}

// Update UI with gesture data
function updateGestureUI(gestures) {
    // Update smile indicator
    document.getElementById('smileIndicator').classList.toggle('active', gestures.smile);
    
    // Update eye contact indicator
    document.getElementById('eyeContactIndicator').classList.toggle('active', gestures.eye_contact);
    
    // Update posture display
    document.getElementById('postureStatus').textContent = gestures.posture;
    
    // ... update other indicators
}

// Stop gesture recognition when interview ends
async function stopGestureRecognition() {
    clearInterval(gestureInterval);
    
    try {
        // Save session data
        await fetch('http://localhost:5001/api/gesture/save_session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                filename: `session_${sessionId}.json`
            })
        });
        
        // Stop recognition
        await fetch('http://localhost:5001/api/gesture/stop', {
            method: 'POST'
        });
        
        console.log('Gesture recognition stopped');
    } catch (error) {
        console.error('Failed to stop gesture recognition:', error);
    }
}

// Display video feed
function displayGestureVideo() {
    const videoElement = document.getElementById('gestureVideo');
    videoElement.src = 'http://localhost:5001/api/gesture/video_feed';
}
```

### HTML Example

```html
<!-- Add to interview template -->
<div class="gesture-monitoring-panel">
    <h3>🎯 Gesture Monitoring</h3>
    
    <!-- Video Feed -->
    <div class="gesture-video-container">
        <img id="gestureVideo" src="" alt="Gesture Feed">
    </div>
    
    <!-- Gesture Indicators -->
    <div class="gesture-indicators">
        <div class="gesture-item" id="smileIndicator">
            <span class="icon">😊</span>
            <span class="label">Smile</span>
        </div>
        
        <div class="gesture-item" id="eyeContactIndicator">
            <span class="icon">👁️</span>
            <span class="label">Eye Contact</span>
        </div>
        
        <div class="gesture-item" id="thumbsUpIndicator">
            <span class="icon">👍</span>
            <span class="label">Thumbs Up</span>
        </div>
        
        <div class="gesture-item" id="postureIndicator">
            <span class="icon">📐</span>
            <span class="label">Posture: <span id="postureStatus">-</span></span>
        </div>
    </div>
    
    <!-- Statistics -->
    <div class="gesture-stats">
        <div class="stat">
            <span class="stat-label">Smiles</span>
            <span class="stat-value" id="smileCount">0</span>
        </div>
        <div class="stat">
            <span class="stat-label">Eye Contact %</span>
            <span class="stat-value" id="eyeContactPercent">0%</span>
        </div>
    </div>
</div>
```

## 🎨 Adding to Enhanced Interview Page

### Modify `templates/enhanced_interview.html`

Add gesture monitoring section after the existing video section:

```html
<!-- Add after line 177 -->
<div class="gesture-monitoring-section">
    <div class="section-header">
        <h3>🎯 Advanced Gesture Analysis</h3>
        <button class="btn btn-small" id="toggleGestureBtn">Toggle View</button>
    </div>
    
    <div class="gesture-grid">
        <!-- Python-based gesture feed -->
        <div class="gesture-feed">
            <img id="pythonGestureFeed" src="" alt="Gesture Analysis">
        </div>
        
        <!-- Real-time metrics -->
        <div class="gesture-metrics">
            <div class="metric-card" data-gesture="smile">
                <div class="metric-icon">😊</div>
                <div class="metric-info">
                    <div class="metric-label">Smiles</div>
                    <div class="metric-value" id="pythonSmileCount">0</div>
                </div>
            </div>
            
            <div class="metric-card" data-gesture="eye_contact">
                <div class="metric-icon">👁️</div>
                <div class="metric-info">
                    <div class="metric-label">Eye Contact</div>
                    <div class="metric-value" id="pythonEyeContact">0%</div>
                </div>
            </div>
            
            <div class="metric-card" data-gesture="posture">
                <div class="metric-icon">📐</div>
                <div class="metric-info">
                    <div class="metric-label">Posture</div>
                    <div class="metric-value" id="pythonPosture">-</div>
                </div>
            </div>
        </div>
    </div>
</div>
```

### Create JavaScript Integration File

Create `static/js/python_gesture_integration.js`:

```javascript
class PythonGestureIntegration {
    constructor() {
        this.apiUrl = 'http://localhost:5001/api/gesture';
        this.isRunning = false;
        this.pollInterval = null;
        this.sessionData = {};
    }
    
    async start() {
        try {
            const response = await fetch(`${this.apiUrl}/start`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ camera_index: 0 })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.isRunning = true;
                this.startPolling();
                this.displayVideoFeed();
                console.log('✅ Python gesture recognition started');
                return true;
            }
        } catch (error) {
            console.error('❌ Failed to start Python gesture recognition:', error);
            return false;
        }
    }
    
    async stop() {
        try {
            // Save session data first
            await this.saveSession();
            
            // Stop recognition
            const response = await fetch(`${this.apiUrl}/stop`, {
                method: 'POST'
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.isRunning = false;
                this.stopPolling();
                console.log('✅ Python gesture recognition stopped');
                return true;
            }
        } catch (error) {
            console.error('❌ Failed to stop Python gesture recognition:', error);
            return false;
        }
    }
    
    startPolling() {
        this.pollInterval = setInterval(() => this.updateStatus(), 1000);
    }
    
    stopPolling() {
        if (this.pollInterval) {
            clearInterval(this.pollInterval);
            this.pollInterval = null;
        }
    }
    
    async updateStatus() {
        try {
            const response = await fetch(`${this.apiUrl}/status`);
            const data = await response.json();
            
            if (data.success) {
                this.sessionData = data.stats;
                this.updateUI(data.current_gestures, data.stats);
            }
        } catch (error) {
            console.error('Failed to update gesture status:', error);
        }
    }
    
    updateUI(gestures, stats) {
        // Update gesture counts
        document.getElementById('pythonSmileCount').textContent = 
            stats.gestures_detected.smile || 0;
        
        // Calculate eye contact percentage
        const eyeContactPercent = stats.total_frames > 0 
            ? ((stats.gestures_detected.eye_contact / stats.total_frames) * 100).toFixed(1)
            : 0;
        document.getElementById('pythonEyeContact').textContent = `${eyeContactPercent}%`;
        
        // Update posture
        document.getElementById('pythonPosture').textContent = 
            gestures.posture || 'Unknown';
        
        // Highlight active gestures
        document.querySelectorAll('.metric-card').forEach(card => {
            const gesture = card.dataset.gesture;
            card.classList.toggle('active', gestures[gesture] === true);
        });
    }
    
    displayVideoFeed() {
        const videoElement = document.getElementById('pythonGestureFeed');
        if (videoElement) {
            videoElement.src = `${this.apiUrl}/video_feed`;
        }
    }
    
    async saveSession() {
        try {
            const filename = `gesture_session_${Date.now()}.json`;
            const response = await fetch(`${this.apiUrl}/save_session`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ filename })
            });
            
            const data = await response.json();
            console.log('Session data saved:', data);
            return data;
        } catch (error) {
            console.error('Failed to save session:', error);
        }
    }
    
    getSessionData() {
        return this.sessionData;
    }
}

// Initialize when interview starts
const pythonGesture = new PythonGestureIntegration();
```

## 🎯 Backend Integration

### Add to `app.py`

```python
# Add gesture data to interview results
@app.route('/get_results/<session_id>')
def get_results_with_gestures(session_id):
    # ... existing code ...
    
    # Fetch gesture data from API
    try:
        import requests
        gesture_response = requests.get('http://localhost:5001/api/gesture/stats')
        
        if gesture_response.status_code == 200:
            gesture_data = gesture_response.json()
            session_data['gesture_analysis'] = gesture_data['stats']
    except Exception as e:
        print(f"Failed to fetch gesture data: {e}")
    
    # ... rest of existing code ...
```

### Update Report Generation

Modify `report_generator.py` to include gesture metrics:

```python
def generate_report_with_gestures(session_data, gesture_data):
    # ... existing report code ...
    
    # Add gesture analysis section
    if gesture_data:
        report += "\n\n## Gesture Analysis\n\n"
        
        gestures = gesture_data['gestures_detected']
        
        report += f"- Smiles: {gestures.get('smile', 0)}\n"
        report += f"- Eye Contact: {gestures.get('eye_contact', 0)} frames\n"
        report += f"- Confident Posture: {gestures.get('confident_posture', 0)} frames\n"
        report += f"- Thumbs Up: {gestures.get('thumbs_up', 0)}\n"
        
        # Calculate engagement score
        total_frames = gesture_data['total_frames']
        if total_frames > 0:
            engagement = (gestures.get('eye_contact', 0) / total_frames) * 100
            report += f"\n**Engagement Score: {engagement:.1f}%**\n"
    
    return report
```

## 📊 Session Data Format

Gesture session data is saved as JSON:

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
    "eye_contact": 1440.0,
    "thumbs_up": 5.0
  }
}
```

## 🔧 Troubleshooting

### Camera Not Found
```bash
# List available cameras
python -c "import cv2; print([i for i in range(10) if cv2.VideoCapture(i).isOpened()])"
```

### Port Already in Use
```bash
# Change port in gesture_api.py
app.run(debug=True, port=5002, host='0.0.0.0')
```

### CORS Issues
```python
# Add to gesture_api.py
from flask_cors import CORS
CORS(app)
```

### Performance Issues
- Reduce camera resolution
- Lower FPS
- Disable some gesture detections
- Use GPU acceleration

## 📚 Additional Resources

- [OpenCV Documentation](https://docs.opencv.org/)
- [MediaPipe Documentation](https://google.github.io/mediapipe/)
- [Flask Documentation](https://flask.palletsprojects.com/)

## ✅ Next Steps

1. ✅ Install dependencies
2. ✅ Test standalone system
3. ✅ Start API server
4. ⬜ Integrate with frontend
5. ⬜ Update backend routes
6. ⬜ Test complete flow
7. ⬜ Deploy to production

---

**Need Help?** Check the console logs for detailed error messages and status updates.
