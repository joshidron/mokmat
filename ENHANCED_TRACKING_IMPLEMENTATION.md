# Enhanced Interview Tracking Implementation

## Overview
This document outlines the implementation of comprehensive tracking features for the AI Interview System, including full body posture tracking, eye movement detection, tab switching prevention, and interview attempt limits.

## Features Implemented

### 1. **Full Body Posture Tracking**
Using MediaPipe Pose detection to track:
- **Sitting Posture**: Detect slouching, leaning, proper upright position
- **Body Alignment**: Track shoulder alignment and spine position
- **Head Position**: Monitor head tilt and position relative to camera
- **Hand Movements**: Detect excessive fidgeting or hand gestures
- **Distance from Camera**: Ensure user maintains appropriate distance

**Posture Metrics:**
- Shoulder angle (should be level)
- Spine alignment (vertical)
- Head tilt angle (should be minimal)
- Body center position (should be centered)

### 2. **Advanced Eye Movement Tracking**
Enhanced eye tracking beyond basic eye contact:
- **Gaze Direction**: Track where user is looking (left, right, up, down, center)
- **Eye Movement Patterns**: Detect excessive wandering or reading behavior
- **Blink Rate**: Monitor natural vs. stressed blinking patterns
- **Focus Duration**: Track how long user maintains focus on camera
- **Pupil Dilation**: (if camera quality allows) Detect stress indicators

**Eye Tracking Metrics:**
- Gaze stability score
- Focus percentage
- Average gaze duration
- Eye movement frequency

### 3. **Tab/Window Switching Detection**
Comprehensive monitoring to prevent cheating:
- **Visibility API**: Detect when page loses focus
- **Blur/Focus Events**: Track window focus changes
- **Mouse Leave Detection**: Monitor when cursor leaves interview window
- **Keyboard Shortcuts**: Detect Alt+Tab, Cmd+Tab attempts
- **Fullscreen Enforcement**: Encourage/require fullscreen mode

**Actions on Detection:**
- **First Warning**: Display warning message
- **Second Warning**: Final warning with countdown
- **Third Violation**: Terminate interview immediately
- **Permanent Ban**: User cannot retake for 24 hours

### 4. **Interview Attempt Limits**
Strict enforcement of interview quotas:
- **Daily Limit**: Maximum 2 interviews per 24-hour period
- **Total Limit**: Maximum 5 interviews ever (lifetime)
- **Cooldown Period**: 24-hour lockout after violations
- **Database Tracking**: Persistent storage of all attempts

**Limit Display:**
- Show remaining attempts before starting
- Real-time countdown of available interviews
- Clear messaging when limits reached

### 5. **Comprehensive Monitoring Dashboard**
Real-time visual feedback during interview:
- **Posture Indicator**: Green/Yellow/Red status
- **Eye Contact Score**: Percentage display
- **Focus Timer**: Time maintaining proper attention
- **Violation Counter**: Tab switches and warnings
- **Overall Engagement Score**: Combined metric

## Technical Implementation

### Libraries & Technologies

#### Frontend:
```javascript
// TensorFlow.js for ML models
- @tensorflow/tfjs
- @tensorflow/tfjs-backend-webgl
- @mediapipe/face_mesh (existing)
- @mediapipe/pose (NEW - for body tracking)
- @mediapipe/face_detection (enhanced)

// Page Visibility Detection
- Page Visibility API
- Focus/Blur event listeners
- Fullscreen API
```

#### Backend:
```python
# Flask with enhanced database schema
- SQLite for user/session tracking
- Datetime tracking for 24-hour limits
- Session state management
```

### Database Schema Updates

```sql
-- Add to interview_sessions table
ALTER TABLE interview_sessions ADD COLUMN posture_violations INTEGER DEFAULT 0;
ALTER TABLE interview_sessions ADD COLUMN eye_tracking_score REAL DEFAULT 0.0;
ALTER TABLE interview_sessions ADD COLUMN focus_percentage REAL DEFAULT 0.0;
ALTER TABLE interview_sessions ADD COLUMN terminated_reason TEXT;
ALTER TABLE interview_sessions ADD COLUMN warning_count INTEGER DEFAULT 0;

-- Add tracking events table
CREATE TABLE tracking_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    event_type TEXT NOT NULL, -- 'tab_switch', 'posture_violation', 'eye_wander', etc.
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details TEXT,
    FOREIGN KEY (session_id) REFERENCES interview_sessions(session_id)
);

-- Add user violations table
CREATE TABLE user_violations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    violation_type TEXT NOT NULL,
    violation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ban_until TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### File Structure

```
codewave/
├── static/
│   ├── js/
│   │   ├── pose_tracking.js (NEW)
│   │   ├── eye_tracking.js (NEW)
│   │   ├── tab_monitor.js (NEW)
│   │   ├── interview_monitor.js (ENHANCED)
│   │   └── auth_interview.js (ENHANCED)
│   └── css/
│       └── monitoring_ui.css (NEW)
├── templates/
│   └── auth_interview.html (ENHANCED)
└── auth_app.py (ENHANCED)
```

## Implementation Steps

### Step 1: Update Backend (auth_app.py)
- [x] Add new database tables
- [x] Implement violation tracking
- [x] Add endpoints for tracking events
- [x] Enhance interview termination logic
- [x] Add ban/cooldown enforcement

### Step 2: Add Body Posture Tracking
- [ ] Load MediaPipe Pose model
- [ ] Implement posture detection algorithm
- [ ] Calculate posture metrics
- [ ] Display real-time posture feedback
- [ ] Log posture violations

### Step 3: Enhance Eye Tracking
- [ ] Implement gaze direction detection
- [ ] Track eye movement patterns
- [ ] Calculate focus metrics
- [ ] Display eye tracking indicators
- [ ] Log eye tracking events

### Step 4: Implement Tab Monitoring
- [ ] Add Page Visibility API listeners
- [ ] Detect focus/blur events
- [ ] Implement warning system (3 strikes)
- [ ] Auto-terminate on violations
- [ ] Display warning modals

### Step 5: Create Monitoring UI
- [ ] Design real-time monitoring dashboard
- [ ] Add posture indicator widget
- [ ] Add eye tracking widget
- [ ] Add violation counter
- [ ] Add engagement score display

### Step 6: Testing & Refinement
- [ ] Test all tracking features
- [ ] Calibrate detection thresholds
- [ ] Test termination logic
- [ ] Verify limit enforcement
- [ ] Cross-browser testing

## User Experience Flow

### Before Interview:
1. User logs in
2. System checks interview limits
3. Display remaining attempts
4. Show requirements (camera, fullscreen, etc.)
5. User accepts monitoring terms
6. Camera/pose calibration screen

### During Interview:
1. Continuous monitoring active
2. Real-time feedback displayed
3. Warnings shown for violations
4. Automatic termination on severe violations
5. All events logged to database

### After Interview:
1. Display comprehensive report
2. Show tracking metrics
3. Provide feedback on posture/focus
4. Update user statistics
5. Calculate remaining attempts

## Detection Thresholds

### Posture Violations:
- **Slouching**: Shoulder angle > 15° from horizontal
- **Leaning**: Body center offset > 20% from frame center
- **Head Tilt**: Head angle > 20° from vertical
- **Distance**: Face size < 15% or > 40% of frame

### Eye Tracking:
- **Gaze Wander**: Eyes off-center > 3 seconds
- **Focus Loss**: Looking away > 5 seconds = warning
- **Reading Behavior**: Rapid horizontal eye movement

### Tab Switching:
- **First Offense**: Warning message
- **Second Offense**: Final warning + 10s countdown
- **Third Offense**: Immediate termination + 24h ban

## Privacy & Ethics

### Data Handling:
- All video processing done locally (client-side)
- Only metrics sent to server, not video data
- Clear disclosure of monitoring to users
- Option to review tracking data
- Compliance with privacy regulations

### User Consent:
- Explicit consent required before interview
- Clear explanation of what's being tracked
- Right to decline (cannot proceed with interview)
- Data retention policy disclosed

## Performance Optimization

### Client-Side:
- Use WebGL backend for TensorFlow.js
- Optimize detection frequency (15-30 FPS)
- Lazy load models
- Efficient canvas rendering

### Server-Side:
- Batch event logging
- Database indexing on user_id and timestamps
- Efficient query optimization
- Caching for limit checks

## Future Enhancements

1. **AI-Powered Anomaly Detection**: ML model to detect unusual behavior patterns
2. **Voice Analysis**: Detect stress, confidence in speech
3. **Micro-Expression Detection**: Advanced emotion recognition
4. **Screen Recording**: Optional recording for review
5. **Multi-Camera Support**: Multiple angles for better tracking
6. **Mobile Support**: Adapt tracking for mobile devices

## Troubleshooting

### Common Issues:
1. **Pose not detected**: Ensure full upper body visible
2. **Eye tracking inaccurate**: Improve lighting, look at camera
3. **False tab switch warnings**: Disable browser notifications
4. **Performance issues**: Close other tabs, use Chrome

---

**Implementation Date**: January 2026
**Version**: 2.0
**Status**: In Progress
