# 🔧 Troubleshooting Guide - Setup Issues

## Issue 1: PowerShell Execution Policy Error

### Error Message:
```
File D:\codewave\.venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system.
```

### Solutions:

#### **Option A: Use Batch File (Easiest)**
Simply run the batch file instead:
```cmd
quick_setup.bat
```

#### **Option B: Fix PowerShell Execution Policy**
Run PowerShell as Administrator and execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then run:
```powershell
.\quick_setup.ps1
```

#### **Option C: Bypass for Single Session**
```powershell
powershell -ExecutionPolicy Bypass -File quick_setup.ps1
```

---

## Issue 2: Missing Flask Module

### Error Message:
```
ModuleNotFoundError: No module named 'flask'
```

### Solutions:

#### **Option A: Use Quick Setup Scripts**
Run either:
```cmd
quick_setup.bat
```
OR
```powershell
.\quick_setup.ps1
```

#### **Option B: Manual Installation**

1. **Activate virtual environment:**
```cmd
.\.venv\Scripts\activate.bat
```

2. **Install dependencies:**
```cmd
pip install -r requirements.txt
```

3. **Run the server:**
```cmd
python auth_app.py
```

#### **Option C: Install Without Virtual Environment**
```cmd
pip install flask flask-cors authlib pandas numpy scikit-learn
python auth_app.py
```

---

## Issue 3: Virtual Environment Not Found

### Error Message:
```
The system cannot find the path specified: .venv\Scripts\activate.bat
```

### Solution:

Create a new virtual environment:
```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
pip install -r requirements.txt
python auth_app.py
```

---

## Issue 4: Pandas Installation Taking Too Long

### Problem:
Pandas installation is slow or hangs

### Solutions:

#### **Option A: Install Pre-built Wheel**
```cmd
pip install --upgrade pip
pip install pandas --only-binary :all:
```

#### **Option B: Skip Pandas (Temporary)**
Edit `requirements.txt` and comment out pandas:
```
flask==3.0.0
flask-cors==4.0.0
# pandas==2.2.0  # Commented out temporarily
numpy==1.26.2
scikit-learn==1.3.2
authlib==1.3.0
```

Then install:
```cmd
pip install -r requirements.txt
```

---

## Issue 5: Port 5000 Already in Use

### Error Message:
```
Address already in use
```

### Solutions:

#### **Option A: Kill Process Using Port 5000**
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

#### **Option B: Use Different Port**
Edit `auth_app.py` line 868:
```python
app.run(debug=True, port=5001, host='0.0.0.0')  # Changed to 5001
```

Then access: http://localhost:5001

---

## Issue 6: Database Locked Error

### Error Message:
```
sqlite3.OperationalError: database is locked
```

### Solution:

Delete the database and restart:
```cmd
del interview_system.db
python auth_app.py
```

---

## Quick Start Commands

### **Easiest Method (Recommended):**
```cmd
quick_setup.bat
```

### **Alternative Method:**
```cmd
# Activate virtual environment
.\.venv\Scripts\activate.bat

# Install dependencies
pip install flask flask-cors authlib

# Run server
python auth_app.py
```

### **Without Virtual Environment:**
```cmd
pip install flask flask-cors authlib pandas numpy scikit-learn
python auth_app.py
```

---

## Verification Steps

After installation, verify everything works:

1. **Check if server is running:**
   - Look for: "Server starting on http://localhost:5000"
   - No error messages

2. **Open browser:**
   - Navigate to: http://localhost:5000
   - You should see the login page

3. **Test features:**
   - Register a new account
   - Login
   - Test camera/microphone
   - Start an interview

---

## Common Issues & Quick Fixes

| Issue | Quick Fix |
|-------|-----------|
| PowerShell script won't run | Use `quick_setup.bat` instead |
| Flask not found | Run `pip install flask flask-cors` |
| Port 5000 in use | Change port in `auth_app.py` to 5001 |
| Pandas installation slow | Skip pandas temporarily or use pre-built wheel |
| Database locked | Delete `interview_system.db` |
| Virtual env not found | Run `python -m venv .venv` |

---

## Still Having Issues?

### Check Python Version:
```cmd
python --version
```
Required: Python 3.8 or higher

### Check pip Version:
```cmd
pip --version
```
Update if needed:
```cmd
python -m pip install --upgrade pip
```

### Reinstall Everything:
```cmd
# Remove virtual environment
rmdir /s .venv

# Create fresh virtual environment
python -m venv .venv

# Activate
.\.venv\Scripts\activate.bat

# Install
pip install flask flask-cors authlib

# Run
python auth_app.py
```

---

## Contact & Support

If you're still experiencing issues:

1. Check the error message carefully
2. Search for the error online
3. Review the documentation:
   - `ENHANCED_FEATURES_README.md`
   - `QUICKSTART_ENHANCED.md`
   - `IMPLEMENTATION_SUMMARY_V2.md`

---

**Most Common Solution: Just run `quick_setup.bat` and everything will be set up automatically!** 🚀
