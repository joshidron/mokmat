"""
Installation Script for Gesture Recognition System
Installs all required dependencies for camera-based gesture detection
"""

import subprocess
import sys
import os


def run_command(command, description):
    """Run a command and print status"""
    print(f"\n{'='*60}")
    print(f"📦 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ {description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        print(f"Error: {e.stderr}")
        return False


def main():
    """Main installation function"""
    print("\n" + "="*60)
    print("GESTURE RECOGNITION SYSTEM - INSTALLATION")
    print("="*60)
    print("\nThis script will install all required dependencies:")
    print("  - OpenCV (cv2)")
    print("  - MediaPipe")
    print("  - NumPy")
    print("  - Flask")
    print("  - Additional utilities")
    
    input("\nPress Enter to continue...")
    
    # Check Python version
    print(f"\n🐍 Python Version: {sys.version}")
    
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required")
        return
    
    # Upgrade pip
    run_command(
        f"{sys.executable} -m pip install --upgrade pip",
        "Upgrading pip"
    )
    
    # Install packages
    packages = [
        ("opencv-python", "OpenCV - Computer Vision Library"),
        ("mediapipe", "MediaPipe - ML Solutions"),
        ("numpy", "NumPy - Numerical Computing"),
        ("flask", "Flask - Web Framework"),
        ("flask-cors", "Flask-CORS - Cross-Origin Support"),
    ]
    
    failed_packages = []
    
    for package, description in packages:
        success = run_command(
            f"{sys.executable} -m pip install {package}",
            f"Installing {description}"
        )
        
        if not success:
            failed_packages.append(package)
    
    # Summary
    print("\n" + "="*60)
    print("INSTALLATION SUMMARY")
    print("="*60)
    
    if not failed_packages:
        print("\n✅ All packages installed successfully!")
        print("\nYou can now run:")
        print("  1. Standalone: python gesture_recognition.py")
        print("  2. API Server: python gesture_api.py")
        print("  3. Integration: See GESTURE_INTEGRATION_GUIDE.md")
    else:
        print("\n⚠️ Some packages failed to install:")
        for package in failed_packages:
            print(f"  - {package}")
        print("\nPlease install them manually using:")
        print(f"  {sys.executable} -m pip install <package_name>")
    
    print("\n" + "="*60)
    
    # Test imports
    print("\n🧪 Testing imports...")
    
    try:
        import cv2
        print(f"✅ OpenCV version: {cv2.__version__}")
    except ImportError:
        print("❌ OpenCV import failed")
    
    try:
        import mediapipe as mp
        print(f"✅ MediaPipe version: {mp.__version__}")
    except ImportError:
        print("❌ MediaPipe import failed")
    
    try:
        import numpy as np
        print(f"✅ NumPy version: {np.__version__}")
    except ImportError:
        print("❌ NumPy import failed")
    
    try:
        import flask
        print(f"✅ Flask version: {flask.__version__}")
    except ImportError:
        print("❌ Flask import failed")
    
    print("\n✅ Installation complete!")


if __name__ == "__main__":
    main()
