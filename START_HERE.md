# 🚀 QUICK START GUIDE - AI Interview System

## ✅ Server is Running!

Your server is now live at:
- **http://localhost:5000**
- **http://127.0.0.1:5000**

---

## 🎯 IMPORTANT: Always Use `auth_app.py`

### ❌ WRONG:
```cmd
python app.py  # Don't use this!
```

### ✅ CORRECT:
```cmd
python auth_app.py  # Use this!
```

**Why?**
- `app.py` = Old basic version (no authentication, no features)
- `auth_app.py` = Enhanced version with all features

---

## 📋 What to Do Now

### Step 1: Test the Diagnostic Tool

Open in your browser:
```
http://localhost:5000/auth-diagnostic
```

This will test:
- ✅ Server connection
- ✅ Registration endpoint
- ✅ Firebase configuration
- ✅ Google Sign-In

**It will tell you exactly what's wrong!**

---

### Step 2: Fix Google Authentication

**The diagnostic tool will show you if Google Sign-In is enabled.**

If it's NOT enabled:

1. Click the "Enable Google Sign-In" button in the diagnostic tool
2. OR go directly to: https://console.firebase.google.com/project/mokmat-c3474/authentication/providers
3. Click "Google"
4. Toggle "Enable" to ON (must be BLUE)
5. Select support email
6. Click "Save"
7. Wait 30 seconds
8. Try again

---

### Step 3: Try the System

1. **Login Page**:
   ```
   http://localhost:5000/login
   ```

2. **Register Page**:
   ```
   http://localhost:5000/register
   ```

3. **Main Page** (after login):
   ```
   http://localhost:5000
   ```

---

## 🔧 Common Errors & Solutions

### Error: "Network error. Please check your connection"

**Cause**: Server not running or wrong server

**Solution**:
```cmd
# Stop any running server (Ctrl+C)
# Then run the CORRECT file:
python auth_app.py
```

---

### Error: "ModuleNotFoundError: No module named 'flask'"

**Cause**: Running `app.py` instead of `auth_app.py`

**Solution**:
```cmd
# Don't run app.py!
# Run this instead:
python auth_app.py
```

---

### Error: "Authentication failed" (Google Sign-In)

**Cause**: Google Sign-In not enabled in Firebase

**Solution**:
1. Open diagnostic tool: http://localhost:5000/auth-diagnostic
2. Click "Test Google Sign-In"
3. Follow the solution it provides
4. Usually: Enable Google in Firebase Console

---

### Error: "Check your internet" (Registration)

**Cause**: Server not running or browser cache

**Solution**:
```cmd
# 1. Make sure server is running:
python auth_app.py

# 2. Clear browser cache:
# Press Ctrl+Shift+Delete
# Clear "Cached images and files"
# Try again
```

---

## 📱 How to Use the System

### 1. **Register/Login**

**Option A: Traditional**
- Go to http://localhost:5000/register
- Enter username, email, password
- Click "Sign Up"

**Option B: Google Sign-In**
- Go to http://localhost:5000/login
- Click "Continue with Google"
- Select your Google account
- Done!

### 2. **Start Interview**

After login:
- Select role (e.g., Software Engineer)
- Select category (Technical/Behavioral)
- Select difficulty
- Click "Start Interview"

### 3. **During Interview**

You'll see:
- ✅ **Your face** in top-right corner (live video)
- ✅ **Monitoring panel** in bottom-left (real-time status)
- ✅ **Questions** in the center
- ✅ **Voice recognition** button (speak your answer)

### 4. **Monitoring Features**

The system tracks:
- 😊 **Face Detection** - Are you visible?
- 👁️ **Eye Contact** - Are you looking at screen?
- 🧍 **Body Posture** - Are you sitting properly?
- 📱 **Tab Switching** - Did you switch tabs?

**If you switch tabs:**
- 🔊 **3 loud beeps** will play
- ⚠️ Warning modal will appear
- Strike counter increases
- After 3 strikes → Interview terminated

---

## 🎨 What You'll See

### Login Page
```
┌─────────────────────────────┐
│  🎯 Welcome Back            │
│                             │
│  [Continue with Google]     │ ← Click this!
│                             │
│  ────── OR ──────           │
│                             │
│  Username: [________]       │
│  Password: [________]       │
│  [Sign In]                  │
└─────────────────────────────┘
```

### Interview Screen
```
┌─────────────────────────────────────┐
│ Video Feed (Top-Right)              │
│ ┌─────────────┐                     │
│ │ 📹 LIVE     │                     │
│ │ [Your Face] │  Question 1 of 5    │
│ └─────────────┘                     │
│                                     │
│ Q: Explain closures in JavaScript  │
│                                     │
│ [🎤 Start Speaking]                 │
│ Answer: [________________]          │
│ [Submit Answer]                     │
└─────────────────────────────────────┘

Monitoring Panel (Bottom-Left)
┌─────────────────────────┐
│ 🎯 Real-Time Monitoring │
│ [ACTIVE] ●              │
├─────────────────────────┤
│ 😊 Face: Detected ●     │
│ 👁️ Eye: Good ●          │
│ 🧍 Posture: Excellent ● │
│ 📱 Tabs: Active ●       │
├─────────────────────────┤
│ 85%  92%  85%           │
│ Focus Post Eye          │
└─────────────────────────┘
```

---

## ✅ Quick Checklist

Before starting, make sure:

- [ ] Server is running (`python auth_app.py`)
- [ ] Can access http://localhost:5000
- [ ] Diagnostic tool works (http://localhost:5000/auth-diagnostic)
- [ ] Google Sign-In is enabled in Firebase (if using it)
- [ ] Camera and microphone permissions granted
- [ ] Using Chrome, Edge, or Firefox

---

## 🆘 Still Having Issues?

### 1. Run Diagnostic Tool
```
http://localhost:5000/auth-diagnostic
```
It will tell you exactly what's wrong!

### 2. Check Server is Running
```cmd
# Should see this:
Running on http://127.0.0.1:5000
```

### 3. Check Browser Console
- Press F12
- Click "Console" tab
- Look for error messages
- Copy the error and check the solution guides

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `auth_app.py` | **Main server** (use this!) |
| `app.py` | Old version (don't use) |
| `AUTH_ERROR_FIX.md` | Authentication troubleshooting |
| `MONITORING_FEATURES_COMPLETE.md` | Monitoring features guide |
| `templates/auth_diagnostic.html` | Diagnostic tool |

---

## 🎉 You're All Set!

**Server is running at**: http://localhost:5000

**Next steps**:
1. Open diagnostic tool: http://localhost:5000/auth-diagnostic
2. Test everything
3. Fix any issues it finds
4. Start using the system!

---

**Remember**: Always run `python auth_app.py`, NOT `python app.py`! 🚀
