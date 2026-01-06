# 🔧 Google Sign-In Troubleshooting Guide

## Issue: "Continue with Google" Not Working

### Quick Fixes (Try these first)

#### 1. **Enable Google Sign-In in Firebase Console**

**This is the most common issue!**

1. Go to: https://console.firebase.google.com/project/mokmat-c3474/authentication/providers
2. Find "Google" in the list
3. Click on it
4. Toggle "Enable" to ON
5. Select your support email from dropdown
6. Click "Save"

**Without this, Google Sign-In will NOT work!**

---

#### 2. **Add localhost to Authorized Domains**

1. Go to: https://console.firebase.google.com/project/mokmat-c3474/authentication/settings
2. Click "Authorized domains" tab
3. Click "Add domain"
4. Type: `localhost`
5. Click "Add"

---

#### 3. **Check Browser Console for Errors**

1. Open your browser (Chrome recommended)
2. Press `F12` to open Developer Tools
3. Click "Console" tab
4. Click "Continue with Google"
5. Look for error messages

**Common Errors:**

| Error Code | Meaning | Solution |
|------------|---------|----------|
| `auth/operation-not-allowed` | Google Sign-In not enabled | Enable it in Firebase Console (Step 1) |
| `auth/unauthorized-domain` | Domain not authorized | Add localhost to authorized domains (Step 2) |
| `auth/popup-blocked` | Browser blocked popup | Allow popups for localhost |
| `auth/network-request-failed` | Network issue | Check internet connection |

---

### Detailed Troubleshooting

#### Error 1: "operation-not-allowed"

**Full Error:**
```
Firebase: Error (auth/operation-not-allowed).
```

**Cause:** Google Sign-In provider is not enabled in Firebase

**Solution:**
1. Go to Firebase Console → Authentication → Sign-in method
2. Enable Google provider
3. Save changes
4. Refresh your page and try again

---

#### Error 2: "unauthorized-domain"

**Full Error:**
```
Firebase: Error (auth/unauthorized-domain).
```

**Cause:** localhost is not in the authorized domains list

**Solution:**
1. Go to Firebase Console → Authentication → Settings → Authorized domains
2. Add `localhost`
3. Wait 1-2 minutes for changes to propagate
4. Try again

---

#### Error 3: "popup-blocked"

**Full Error:**
```
Popup was blocked. Please allow popups for this site.
```

**Cause:** Browser is blocking the Google Sign-In popup

**Solution:**

**For Chrome:**
1. Click the popup blocked icon in address bar
2. Select "Always allow popups from localhost"
3. Try again

**For Firefox:**
1. Click the blocked popup notification
2. Select "Allow popups for localhost"
3. Try again

---

#### Error 4: "Firebase initialization failed"

**Cause:** Firebase SDK not loaded or configuration error

**Solution:**

1. **Check if Firebase scripts are loaded:**
   - Open browser console
   - Type: `firebase`
   - Should show Firebase object, not "undefined"

2. **If undefined, check HTML:**
   ```html
   <!-- These should be in your HTML <head> -->
   <script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-app-compat.js"></script>
   <script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-auth-compat.js"></script>
   ```

3. **Check internet connection**

---

### Testing Steps

#### Step 1: Test Firebase Connection

Open browser console and run:
```javascript
console.log('Firebase loaded:', typeof firebase !== 'undefined');
console.log('Auth loaded:', typeof firebase.auth !== 'undefined');
```

Should show:
```
Firebase loaded: true
Auth loaded: true
```

---

#### Step 2: Test Firebase Initialization

In console:
```javascript
initializeFirebase();
```

Should show:
```
[OK] Firebase initialized successfully
   Project: mokmat-c3474
```

---

#### Step 3: Test Google Sign-In

Click "Continue with Google" button and watch console for:

**Success:**
```
[INFO] Starting Google Sign-In...
[OK] Google Sign-In successful
   User: Your Name your.email@gmail.com
[INFO] Sending user data to backend...
[OK] User registered/logged in on backend
[OK] Complete sign-in successful
```

**Failure:**
```
[ERROR] Google Sign-In error: ...
   Error code: auth/...
   Error message: ...
```

---

### Common Solutions

#### Solution 1: Clear Browser Cache

1. Press `Ctrl+Shift+Delete`
2. Select "Cached images and files"
3. Click "Clear data"
4. Restart browser
5. Try again

---

#### Solution 2: Try Different Browser

- **Recommended:** Google Chrome (best Firebase support)
- **Alternative:** Microsoft Edge
- **Avoid:** Internet Explorer (not supported)

---

#### Solution 3: Check Firewall/Antivirus

Some firewalls block Firebase:
1. Temporarily disable firewall
2. Try Google Sign-In
3. If it works, add exception for:
   - `*.googleapis.com`
   - `*.firebaseapp.com`

---

#### Solution 4: Use Incognito/Private Mode

1. Open incognito window (`Ctrl+Shift+N`)
2. Go to `http://localhost:5000/login`
3. Try Google Sign-In
4. If it works, clear cookies in normal mode

---

### Verification Checklist

Before asking for help, verify:

- [ ] Google Sign-In is enabled in Firebase Console
- [ ] localhost is in authorized domains
- [ ] Browser allows popups for localhost
- [ ] Firebase scripts are loading (check console)
- [ ] Internet connection is working
- [ ] Using supported browser (Chrome/Edge/Firefox)
- [ ] Server is running (`python auth_app.py`)
- [ ] Visiting correct URL (`http://localhost:5000/login`)

---

### Still Not Working?

#### Check Backend

1. **Verify server is running:**
   ```cmd
   python auth_app.py
   ```

2. **Check if `/api/google-auth` endpoint exists:**
   - Open: `http://localhost:5000/api/google-auth`
   - Should show: "Method Not Allowed" (this is OK, means endpoint exists)

3. **Check server logs:**
   - Look at terminal where server is running
   - Should show requests when you click Google button

---

#### Enable Debug Mode

Add this to your HTML before the closing `</body>` tag:

```html
<script>
// Enable detailed logging
firebase.auth().useDeviceLanguage();
firebase.auth().onAuthStateChanged((user) => {
    console.log('[DEBUG] Auth state changed:', user ? user.email : 'signed out');
});
</script>
```

---

### Quick Test Script

Open browser console and paste this:

```javascript
// Test complete flow
async function testGoogleSignIn() {
    console.log('=== Testing Google Sign-In ===');
    
    // Test 1: Firebase loaded
    console.log('1. Firebase loaded:', typeof firebase !== 'undefined');
    
    // Test 2: Initialize
    const init = initializeFirebase();
    console.log('2. Initialized:', init);
    
    // Test 3: Try sign in
    console.log('3. Attempting sign in...');
    const result = await signInWithGoogle();
    console.log('4. Result:', result);
    
    return result;
}

testGoogleSignIn();
```

---

### Contact Support

If still not working, provide:

1. **Browser console output** (copy all errors)
2. **Browser name and version**
3. **Operating system**
4. **Screenshot of Firebase Console → Authentication → Sign-in method**
5. **Screenshot of error message**

---

## Most Common Fix

**90% of the time, the issue is:**

Google Sign-In is not enabled in Firebase Console!

**Solution:**
1. Go to: https://console.firebase.google.com/project/mokmat-c3474/authentication/providers
2. Click "Google"
3. Toggle "Enable"
4. Save
5. Try again

---

**That's it! Your Google Sign-In should now work!** 🎉
