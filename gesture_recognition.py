"""
Live Camera Gesture Recognition System for Interview Application
Uses OpenCV, MediaPipe, and TensorFlow for real-time gesture detection
"""

import cv2
import mediapipe as mp
import numpy as np
import time
from collections import deque
import json
from datetime import datetime


class GestureRecognizer:
    """Real-time gesture recognition using MediaPipe and OpenCV"""
    
    def __init__(self):
        # Initialize MediaPipe solutions
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_hands = mp.solutions.hands
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Initialize detectors
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Gesture tracking data
        self.gesture_history = deque(maxlen=30)  # Last 30 frames
        self.head_positions = deque(maxlen=10)
        self.hand_positions = deque(maxlen=10)
        
        # Gesture counters
        self.gestures_detected = {
            'smile': 0,
            'thumbs_up': 0,
            'wave': 0,
            'nod': 0,
            'eye_contact': 0,
            'thinking': 0,
            'confident_posture': 0,
            'nervous_gestures': 0
        }
        
        # Session data
        self.session_start = time.time()
        self.frame_count = 0
        
    def calculate_distance(self, point1, point2):
        """Calculate Euclidean distance between two points"""
        return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    def detect_smile(self, face_landmarks, image_width, image_height):
        """Detect smile based on mouth landmarks"""
        # Mouth corner points
        left_mouth = face_landmarks.landmark[61]
        right_mouth = face_landmarks.landmark[291]
        top_lip = face_landmarks.landmark[13]
        bottom_lip = face_landmarks.landmark[14]
        
        # Convert to pixel coordinates
        mouth_width = abs(right_mouth.x - left_mouth.x) * image_width
        mouth_height = abs(top_lip.y - bottom_lip.y) * image_height
        
        # Smile ratio
        if mouth_height > 0:
            smile_ratio = mouth_width / mouth_height
            if smile_ratio > 3.5:
                self.gestures_detected['smile'] += 1
                return True, smile_ratio
        
        return False, 0
    
    def detect_eye_contact(self, face_landmarks, image_width, image_height):
        """Detect if person is looking at camera"""
        # Get eye landmarks
        left_eye = face_landmarks.landmark[33]
        right_eye = face_landmarks.landmark[263]
        nose_tip = face_landmarks.landmark[1]
        
        # Calculate eye center
        eye_center_x = (left_eye.x + right_eye.x) / 2
        
        # Check if nose is centered between eyes
        deviation = abs(nose_tip.x - eye_center_x)
        eye_distance = abs(right_eye.x - left_eye.x)
        
        if deviation < eye_distance * 0.15:  # Within 15% of eye distance
            self.gestures_detected['eye_contact'] += 1
            return True
        
        return False
    
    def detect_head_nod(self, face_landmarks, image_height):
        """Detect head nodding gesture"""
        nose_tip = face_landmarks.landmark[1]
        current_y = nose_tip.y * image_height
        
        self.head_positions.append(current_y)
        
        if len(self.head_positions) >= 10:
            positions = list(self.head_positions)
            # Check for up-down pattern
            max_pos = max(positions)
            min_pos = min(positions)
            
            if max_pos - min_pos > 20:  # Significant vertical movement
                # Check for oscillation pattern
                mid_point = (max_pos + min_pos) / 2
                crossings = 0
                for i in range(1, len(positions)):
                    if (positions[i-1] < mid_point and positions[i] >= mid_point) or \
                       (positions[i-1] >= mid_point and positions[i] < mid_point):
                        crossings += 1
                
                if crossings >= 2:  # At least one complete nod
                    self.gestures_detected['nod'] += 1
                    return True
        
        return False
    
    def detect_thumbs_up(self, hand_landmarks, handedness):
        """Detect thumbs up gesture"""
        # Get thumb and finger tips
        thumb_tip = hand_landmarks.landmark[4]
        index_tip = hand_landmarks.landmark[8]
        middle_tip = hand_landmarks.landmark[12]
        ring_tip = hand_landmarks.landmark[16]
        pinky_tip = hand_landmarks.landmark[20]
        
        # Get palm base
        wrist = hand_landmarks.landmark[0]
        
        # Thumb should be extended upward
        thumb_extended = thumb_tip.y < wrist.y
        
        # Other fingers should be curled
        fingers_curled = (index_tip.y > wrist.y and 
                         middle_tip.y > wrist.y and 
                         ring_tip.y > wrist.y and 
                         pinky_tip.y > wrist.y)
        
        if thumb_extended and fingers_curled:
            self.gestures_detected['thumbs_up'] += 1
            return True
        
        return False
    
    def detect_wave(self, hand_landmarks):
        """Detect waving gesture"""
        wrist = hand_landmarks.landmark[0]
        current_x = wrist.x
        
        self.hand_positions.append(current_x)
        
        if len(self.hand_positions) >= 10:
            positions = list(self.hand_positions)
            # Check for side-to-side movement
            max_pos = max(positions)
            min_pos = min(positions)
            
            if max_pos - min_pos > 0.1:  # Significant horizontal movement
                self.gestures_detected['wave'] += 1
                return True
        
        return False
    
    def detect_thinking_pose(self, pose_landmarks, hand_landmarks):
        """Detect thinking pose (hand near face)"""
        if pose_landmarks and hand_landmarks:
            # Get face position (nose)
            nose = pose_landmarks.landmark[0]
            
            # Get hand position (wrist)
            wrist = hand_landmarks.landmark[0]
            
            # Calculate distance
            distance = self.calculate_distance(
                (nose.x, nose.y),
                (wrist.x, wrist.y)
            )
            
            if distance < 0.15:  # Hand close to face
                self.gestures_detected['thinking'] += 1
                return True
        
        return False
    
    def detect_posture(self, pose_landmarks):
        """Detect body posture (confident vs slouching)"""
        if pose_landmarks:
            # Get shoulder and hip landmarks
            left_shoulder = pose_landmarks.landmark[11]
            right_shoulder = pose_landmarks.landmark[12]
            left_hip = pose_landmarks.landmark[23]
            right_hip = pose_landmarks.landmark[24]
            
            # Calculate shoulder-hip alignment
            shoulder_center_y = (left_shoulder.y + right_shoulder.y) / 2
            hip_center_y = (left_hip.y + right_hip.y) / 2
            
            # Calculate shoulder width
            shoulder_width = abs(right_shoulder.x - left_shoulder.x)
            
            # Good posture: shoulders above hips, shoulders wide
            if shoulder_center_y < hip_center_y and shoulder_width > 0.2:
                self.gestures_detected['confident_posture'] += 1
                return 'confident'
            else:
                return 'slouching'
        
        return 'unknown'
    
    def detect_nervous_gestures(self, hand_landmarks):
        """Detect nervous gestures (fidgeting, rapid movements)"""
        if len(self.hand_positions) >= 5:
            positions = list(self.hand_positions)[-5:]
            
            # Calculate movement variance
            variance = np.var(positions)
            
            if variance > 0.01:  # High variance indicates fidgeting
                self.gestures_detected['nervous_gestures'] += 1
                return True
        
        return False
    
    def process_frame(self, frame):
        """Process a single frame and detect all gestures"""
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_height, image_width, _ = frame.shape
        
        # Process with MediaPipe
        face_results = self.face_mesh.process(rgb_frame)
        hand_results = self.hands.process(rgb_frame)
        pose_results = self.pose.process(rgb_frame)
        
        # Current frame gestures
        current_gestures = {
            'smile': False,
            'eye_contact': False,
            'head_nod': False,
            'thumbs_up': False,
            'wave': False,
            'thinking': False,
            'posture': 'unknown',
            'nervous': False
        }
        
        # Detect face gestures
        if face_results.multi_face_landmarks:
            face_landmarks = face_results.multi_face_landmarks[0]
            
            # Draw face mesh
            self.mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_tesselation_style()
            )
            
            # Detect gestures
            is_smiling, smile_ratio = self.detect_smile(face_landmarks, image_width, image_height)
            current_gestures['smile'] = is_smiling
            
            current_gestures['eye_contact'] = self.detect_eye_contact(
                face_landmarks, image_width, image_height
            )
            
            current_gestures['head_nod'] = self.detect_head_nod(
                face_landmarks, image_height
            )
        
        # Detect hand gestures
        if hand_results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(hand_results.multi_hand_landmarks):
                # Draw hand landmarks
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
                
                # Detect gestures
                handedness = hand_results.multi_handedness[idx].classification[0].label
                current_gestures['thumbs_up'] = self.detect_thumbs_up(hand_landmarks, handedness)
                current_gestures['wave'] = self.detect_wave(hand_landmarks)
                current_gestures['nervous'] = self.detect_nervous_gestures(hand_landmarks)
                
                # Detect thinking pose
                if pose_results.pose_landmarks:
                    current_gestures['thinking'] = self.detect_thinking_pose(
                        pose_results.pose_landmarks,
                        hand_landmarks
                    )
        
        # Detect body posture
        if pose_results.pose_landmarks:
            # Draw pose landmarks
            self.mp_drawing.draw_landmarks(
                frame,
                pose_results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
            )
            
            current_gestures['posture'] = self.detect_posture(pose_results.pose_landmarks)
        
        # Add to history
        self.gesture_history.append(current_gestures)
        self.frame_count += 1
        
        return frame, current_gestures
    
    def draw_gesture_indicators(self, frame, gestures):
        """Draw gesture indicators on frame"""
        height, width = frame.shape[:2]
        
        # Create overlay
        overlay = frame.copy()
        
        # Define indicator positions
        y_offset = 30
        x_offset = 10
        
        # Gesture indicators
        indicators = [
            ('😊 Smile', gestures['smile'], (0, 255, 0)),
            ('👁️ Eye Contact', gestures['eye_contact'], (0, 255, 255)),
            ('👍 Thumbs Up', gestures['thumbs_up'], (255, 200, 0)),
            ('👋 Wave', gestures['wave'], (255, 150, 0)),
            ('🤔 Thinking', gestures['thinking'], (200, 100, 255)),
            ('📐 Posture: ' + gestures['posture'], gestures['posture'] == 'confident', (100, 200, 255))
        ]
        
        for i, (label, active, color) in enumerate(indicators):
            y_pos = y_offset + (i * 35)
            
            # Background rectangle
            bg_color = color if active else (50, 50, 50)
            cv2.rectangle(overlay, (x_offset, y_pos - 20), (x_offset + 250, y_pos + 10), bg_color, -1)
            
            # Text
            text_color = (255, 255, 255) if active else (150, 150, 150)
            cv2.putText(overlay, label, (x_offset + 10, y_pos), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2)
        
        # Blend overlay
        alpha = 0.7
        frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
        
        return frame
    
    def get_session_stats(self):
        """Get statistics for the current session"""
        duration = time.time() - self.session_start
        
        stats = {
            'duration_seconds': duration,
            'total_frames': self.frame_count,
            'fps': self.frame_count / duration if duration > 0 else 0,
            'gestures_detected': self.gestures_detected.copy(),
            'gesture_rates': {}
        }
        
        # Calculate gesture rates (per minute)
        if duration > 0:
            minutes = duration / 60
            for gesture, count in self.gestures_detected.items():
                stats['gesture_rates'][gesture] = count / minutes
        
        return stats
    
    def save_session_data(self, filename='gesture_session.json'):
        """Save session data to JSON file"""
        stats = self.get_session_stats()
        stats['timestamp'] = datetime.now().isoformat()
        
        with open(filename, 'w') as f:
            json.dump(stats, f, indent=2)
        
        return stats
    
    def release(self):
        """Release all resources"""
        self.face_mesh.close()
        self.hands.close()
        self.pose.close()


def main():
    """Main function to run gesture recognition"""
    print("=" * 60)
    print("LIVE CAMERA GESTURE RECOGNITION SYSTEM")
    print("=" * 60)
    print("\nInitializing camera and gesture recognition...")
    
    # Initialize gesture recognizer
    recognizer = GestureRecognizer()
    
    # Initialize camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Could not open camera")
        return
    
    # Set camera properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    print("✅ Camera initialized successfully!")
    print("\nGesture Detection Active:")
    print("  - 😊 Smile Detection")
    print("  - 👁️ Eye Contact Tracking")
    print("  - 👍 Thumbs Up Recognition")
    print("  - 👋 Wave Detection")
    print("  - 🤔 Thinking Pose")
    print("  - 📐 Posture Analysis")
    print("\nPress 'q' to quit, 's' to save session data")
    print("=" * 60)
    
    try:
        while True:
            ret, frame = cap.read()
            
            if not ret:
                print("❌ Error: Failed to capture frame")
                break
            
            # Mirror the frame for natural interaction
            frame = cv2.flip(frame, 1)
            
            # Process frame
            processed_frame, gestures = recognizer.process_frame(frame)
            
            # Draw gesture indicators
            display_frame = recognizer.draw_gesture_indicators(processed_frame, gestures)
            
            # Add FPS counter
            stats = recognizer.get_session_stats()
            fps_text = f"FPS: {stats['fps']:.1f}"
            cv2.putText(display_frame, fps_text, (display_frame.shape[1] - 150, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Display frame
            cv2.imshow('Gesture Recognition - Interview System', display_frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                print("\n🛑 Stopping gesture recognition...")
                break
            elif key == ord('s'):
                print("\n💾 Saving session data...")
                stats = recognizer.save_session_data()
                print(f"✅ Session data saved!")
                print(f"   Duration: {stats['duration_seconds']:.1f}s")
                print(f"   Total Frames: {stats['total_frames']}")
                print(f"   Gestures Detected: {sum(stats['gestures_detected'].values())}")
    
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user")
    
    finally:
        # Cleanup
        print("\n🧹 Cleaning up resources...")
        
        # Save final session data
        final_stats = recognizer.save_session_data('final_session.json')
        
        print("\n" + "=" * 60)
        print("SESSION SUMMARY")
        print("=" * 60)
        print(f"Duration: {final_stats['duration_seconds']:.1f} seconds")
        print(f"Total Frames: {final_stats['total_frames']}")
        print(f"Average FPS: {final_stats['fps']:.1f}")
        print("\nGestures Detected:")
        for gesture, count in final_stats['gestures_detected'].items():
            print(f"  {gesture.replace('_', ' ').title()}: {count}")
        print("=" * 60)
        
        cap.release()
        cv2.destroyAllWindows()
        recognizer.release()
        
        print("\n✅ Gesture recognition system stopped successfully!")


if __name__ == "__main__":
    main()
