"""
Flask API Integration for Gesture Recognition
Provides REST endpoints for the interview system to access gesture data
"""

from flask import Flask, Response, jsonify, request
import cv2
import json
import threading
import time
from gesture_recognition import GestureRecognizer
import base64
import numpy as np


class GestureAPI:
    """API wrapper for gesture recognition system"""
    
    def __init__(self):
        self.recognizer = GestureRecognizer()
        self.camera = None
        self.is_running = False
        self.current_frame = None
        self.current_gestures = {}
        self.lock = threading.Lock()
        
    def start_camera(self, camera_index=0):
        """Start camera capture"""
        if self.camera is None or not self.camera.isOpened():
            self.camera = cv2.VideoCapture(camera_index)
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.camera.set(cv2.CAP_PROP_FPS, 30)
            
            if self.camera.isOpened():
                self.is_running = True
                # Start processing thread
                threading.Thread(target=self._process_frames, daemon=True).start()
                return True
        return False
    
    def stop_camera(self):
        """Stop camera capture"""
        self.is_running = False
        if self.camera:
            self.camera.release()
            self.camera = None
    
    def _process_frames(self):
        """Process frames in background thread"""
        while self.is_running and self.camera and self.camera.isOpened():
            ret, frame = self.camera.read()
            
            if ret:
                # Mirror frame
                frame = cv2.flip(frame, 1)
                
                # Process with gesture recognition
                processed_frame, gestures = self.recognizer.process_frame(frame)
                
                # Draw indicators
                display_frame = self.recognizer.draw_gesture_indicators(
                    processed_frame, gestures
                )
                
                # Update shared state
                with self.lock:
                    self.current_frame = display_frame
                    self.current_gestures = gestures
            
            time.sleep(0.01)  # ~100 FPS max
    
    def get_current_frame(self):
        """Get current processed frame"""
        with self.lock:
            return self.current_frame.copy() if self.current_frame is not None else None
    
    def get_current_gestures(self):
        """Get current gesture data"""
        with self.lock:
            return self.current_gestures.copy()
    
    def get_session_stats(self):
        """Get session statistics"""
        return self.recognizer.get_session_stats()
    
    def generate_frames(self):
        """Generate frames for video streaming"""
        while self.is_running:
            frame = self.get_current_frame()
            
            if frame is not None:
                # Encode frame as JPEG
                ret, buffer = cv2.imencode('.jpg', frame)
                
                if ret:
                    frame_bytes = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            time.sleep(0.033)  # ~30 FPS


# Create Flask app
app = Flask(__name__)
gesture_api = GestureAPI()


@app.route('/api/gesture/start', methods=['POST'])
def start_gesture_recognition():
    """Start gesture recognition"""
    try:
        camera_index = request.json.get('camera_index', 0) if request.json else 0
        
        if gesture_api.start_camera(camera_index):
            return jsonify({
                'success': True,
                'message': 'Gesture recognition started'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to start camera'
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/gesture/stop', methods=['POST'])
def stop_gesture_recognition():
    """Stop gesture recognition"""
    try:
        gesture_api.stop_camera()
        return jsonify({
            'success': True,
            'message': 'Gesture recognition stopped'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/gesture/status', methods=['GET'])
def get_gesture_status():
    """Get current gesture status"""
    try:
        gestures = gesture_api.get_current_gestures()
        stats = gesture_api.get_session_stats()
        
        return jsonify({
            'success': True,
            'is_running': gesture_api.is_running,
            'current_gestures': gestures,
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/gesture/stats', methods=['GET'])
def get_session_stats():
    """Get detailed session statistics"""
    try:
        stats = gesture_api.get_session_stats()
        return jsonify({
            'success': True,
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/gesture/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(
        gesture_api.generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@app.route('/api/gesture/frame', methods=['GET'])
def get_current_frame():
    """Get current frame as base64 encoded image"""
    try:
        frame = gesture_api.get_current_frame()
        
        if frame is not None:
            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            
            if ret:
                # Convert to base64
                frame_base64 = base64.b64encode(buffer).decode('utf-8')
                
                return jsonify({
                    'success': True,
                    'frame': frame_base64,
                    'gestures': gesture_api.get_current_gestures()
                })
        
        return jsonify({
            'success': False,
            'message': 'No frame available'
        }), 404
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/gesture/save_session', methods=['POST'])
def save_session():
    """Save session data"""
    try:
        filename = request.json.get('filename', 'gesture_session.json') if request.json else 'gesture_session.json'
        stats = gesture_api.recognizer.save_session_data(filename)
        
        return jsonify({
            'success': True,
            'message': 'Session data saved',
            'stats': stats,
            'filename': filename
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


# Health check endpoint
@app.route('/api/gesture/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'is_running': gesture_api.is_running
    })


if __name__ == '__main__':
    print("=" * 60)
    print("GESTURE RECOGNITION API SERVER")
    print("=" * 60)
    print("\nStarting Flask server on http://localhost:5001")
    print("\nAvailable Endpoints:")
    print("  POST   /api/gesture/start       - Start gesture recognition")
    print("  POST   /api/gesture/stop        - Stop gesture recognition")
    print("  GET    /api/gesture/status      - Get current status")
    print("  GET    /api/gesture/stats       - Get session statistics")
    print("  GET    /api/gesture/video_feed  - Video stream")
    print("  GET    /api/gesture/frame       - Get current frame")
    print("  POST   /api/gesture/save_session - Save session data")
    print("  GET    /api/gesture/health      - Health check")
    print("\n" + "=" * 60)
    
    app.run(debug=True, port=5001, host='0.0.0.0', threaded=True)
