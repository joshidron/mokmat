# 🌐 Server Information - Interview System

## 📍 Your IP Addresses

### Local Machine IP
```
IPv4 Address: 192.168.0.108
```

### Localhost
```
127.0.0.1
localhost
```

## 🚀 Running Servers

### Main Interview Application
**Status:** ✅ RUNNING

**URLs:**
- Local: `http://localhost:5000`
- Network: `http://192.168.0.108:5000`

**Access from:**
- Same computer: `http://localhost:5000`
- Other devices on same network: `http://192.168.0.108:5000`

### Gesture Recognition API
**Status:** ⏸️ NOT RUNNING (MediaPipe compatibility issue)

**URLs (when running):**
- Local: `http://localhost:5001`
- Network: `http://192.168.0.108:5001`

## 🔗 Access URLs

### For You (Same Computer)
```
Main App:     http://localhost:5000
Gesture API:  http://localhost:5001
```

### For Other Devices (Same WiFi Network)
```
Main App:     http://192.168.0.108:5000
Gesture API:  http://192.168.0.108:5001
```

### For Mobile/Tablet Testing
Open browser and go to:
```
http://192.168.0.108:5000
```

## 📱 QR Code Access
You can generate a QR code for easy mobile access:
```
URL: http://192.168.0.108:5000
```

## 🎯 Main Features Available

### Interview System (Port 5000)
- ✅ User Authentication (Login/Register)
- ✅ Google OAuth Sign-in
- ✅ Interview Sessions
- ✅ Voice Recognition
- ✅ Tab Monitoring
- ✅ Face Detection (JavaScript-based)
- ✅ PDF Report Generation
- ✅ Audio Alerts
- ✅ Admin Dashboard

### Gesture Recognition (Port 5001)
- ⏸️ Python-based gesture detection (needs MediaPipe fix)
- Alternative: JavaScript face detection already working

## 🔧 Current Status

### ✅ Working
- Main interview application on port 5000
- JavaScript-based face detection
- All interview features
- Database and authentication

### ⚠️ Needs Attention
- Python gesture API (MediaPipe compatibility)
- Alternative: Use existing JavaScript face detection

## 🌐 Network Configuration

### Your Network
- IP Address: `192.168.0.108`
- Subnet: `192.168.0.x`
- Gateway: (check router)

### Firewall Settings
If you can't access from other devices:
1. Open Windows Firewall
2. Allow Python through firewall
3. Allow ports 5000 and 5001

### Port Forwarding (Optional)
For external access outside your network:
1. Configure router port forwarding
2. Forward ports 5000, 5001 to 192.168.0.108
3. Use your public IP address

## 📋 Quick Commands

### Check Your IP
```powershell
ipconfig | findstr /i "IPv4"
```

### Test Server
```powershell
# Test main app
curl http://localhost:5000

# Test from network
curl http://192.168.0.108:5000
```

### Stop Servers
Press `Ctrl+C` in the terminal running the server

### Restart Servers
```powershell
python app.py
```

## 🔐 Security Notes

### For Local Network Use
- Current setup is fine
- Only accessible on your WiFi network
- No external access

### For Production/Internet Use
- Use HTTPS (SSL certificate)
- Set up proper authentication
- Use environment variables for secrets
- Configure firewall rules
- Use reverse proxy (nginx)

## 📞 Access Information Summary

**Main Interview App:**
```
Local:    http://localhost:5000
Network:  http://192.168.0.108:5000
```

**Features:**
- Login/Register
- Start Interview
- Voice Recognition
- Face Detection (JS)
- PDF Reports
- Admin Panel

**Gesture API (when fixed):**
```
Local:    http://localhost:5001
Network:  http://192.168.0.108:5001
```

## 🎉 You're Live!

Your interview system is now running and accessible at:

### 🖥️ On This Computer
**http://localhost:5000**

### 📱 On Other Devices (Same WiFi)
**http://192.168.0.108:5000**

---

**Note:** The Python gesture recognition API has a MediaPipe compatibility issue. However, your existing JavaScript-based face detection system is working perfectly! You can use that for now.

**To access:** Open any browser and navigate to the URLs above!
