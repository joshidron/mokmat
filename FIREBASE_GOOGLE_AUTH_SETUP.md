# 🔥 Firebase Google Authentication Setup Guide

## Step 1: Create Firebase Project

1. **Go to Firebase Console**:
   - Visit: https://console.firebase.google.com/
   - Click "Add project" or "Create a project"

2. **Configure Project**:
   - Enter project name (e.g., "AI Interview System")
   - Accept terms and click "Continue"
   - Disable Google Analytics (optional) or configure it
   - Click "Create project"
   - Wait for project creation
   - Click "Continue"

## Step 2: Register Web App

1. **Add Web App**:
   - In Firebase Console, click the web icon (`</>`)
   - Enter app nickname (e.g., "Interview Web App")
   - Check "Also set up Firebase Hosting" (optional)
   - Click "Register app"

2. **Copy Firebase Configuration**:
   - You'll see a code snippet with `firebaseConfig`
   - Copy the configuration object
   - It looks like this:
   ```javascript
   const firebaseConfig = {
       apiKey: "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
       authDomain: "your-project.firebaseapp.com",
       projectId: "your-project",
       storageBucket: "your-project.appspot.com",
       messagingSenderId: "123456789012",
       appId: "1:123456789012:web:xxxxxxxxxxxxx",
       measurementId: "G-XXXXXXXXXX"
   };
   ```

## Step 3: Enable Google Authentication

1. **Go to Authentication**:
   - In Firebase Console sidebar, click "Authentication"
   - Click "Get started"

2. **Enable Google Sign-In**:
   - Click "Sign-in method" tab
   - Find "Google" in the providers list
   - Click on "Google"
   - Toggle "Enable"
   - Enter project support email
   - Click "Save"

## Step 4: Configure Your Application

### Update Firebase Configuration

1. **Open the file**: `static/js/firebase_auth.js`

2. **Replace the configuration** (lines 6-13):
   ```javascript
   const firebaseConfig = {
       apiKey: "YOUR_ACTUAL_API_KEY",
       authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
       projectId: "YOUR_PROJECT_ID",
       storageBucket: "YOUR_PROJECT_ID.appspot.com",
       messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
       appId: "YOUR_APP_ID",
       measurementId: "YOUR_MEASUREMENT_ID"
   };
   ```

3. **Paste your actual values** from Step 2

### Example Configuration:
```javascript
const firebaseConfig = {
    apiKey: "AIzaSyDXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    authDomain: "ai-interview-system.firebaseapp.com",
    projectId: "ai-interview-system",
    storageBucket: "ai-interview-system.appspot.com",
    messagingSenderId: "123456789012",
    appId: "1:123456789012:web:abcdef123456",
    measurementId: "G-ABCD1234"
};
```

## Step 5: Add Authorized Domains

1. **In Firebase Console**:
   - Go to Authentication → Settings → Authorized domains
   - Add your domains:
     - `localhost` (for development)
     - Your production domain (e.g., `yourapp.com`)

2. **Click "Add domain"** for each

## Step 6: Test the Integration

### Development Testing:

1. **Start your server**:
   ```cmd
   python auth_app.py
   ```

2. **Open browser**:
   ```
   http://localhost:5000/login
   ```

3. **Click "Continue with Google"**:
   - Google Sign-In popup should appear
   - Select your Google account
   - Grant permissions
   - You should be redirected to the main page

### Verify in Firebase Console:

1. Go to Authentication → Users
2. You should see your Google account listed
3. Check the "Providers" column shows "google.com"

## Step 7: Production Deployment

### Update Authorized Domains:

1. **In Firebase Console**:
   - Authentication → Settings → Authorized domains
   - Add your production domain
   - Example: `interview-system.com`

### Update Application URLs:

1. **If using custom domain**, update redirect URLs in your app
2. **Ensure HTTPS** is enabled (required for production)

## Troubleshooting

### Issue 1: "Firebase initialization failed"

**Solution**:
- Check if Firebase configuration is correct
- Verify all values are copied correctly
- Check browser console for specific errors

### Issue 2: "Popup blocked"

**Solution**:
- Allow popups for localhost in browser settings
- Or use redirect method instead of popup

### Issue 3: "Unauthorized domain"

**Solution**:
- Add domain to Authorized domains in Firebase Console
- Wait a few minutes for changes to propagate

### Issue 4: "API key not valid"

**Solution**:
- Verify API key in Firebase Console
- Regenerate API key if needed
- Update configuration in `firebase_auth.js`

## Security Best Practices

### 1. **Protect API Keys**:
   - For production, use environment variables
   - Don't commit Firebase config to public repositories
   - Use Firebase App Check for additional security

### 2. **Set Up Security Rules**:
   - Configure Firestore/Database security rules
   - Restrict access based on authentication

### 3. **Enable App Check** (Optional):
   - Protects your backend from abuse
   - Verifies requests come from your app

## Features Implemented

### ✅ Google Sign-In on Login Page
- One-click Google authentication
- Automatic account creation
- Session management

### ✅ Google Sign-Up on Register Page
- Same Google button for registration
- Creates user account automatically
- Links to existing email if found

### ✅ Seamless Integration
- Works with existing username/password login
- Stores Google profile picture
- Maintains session across page reloads

## File Structure

```
codewave/
├── static/
│   ├── js/
│   │   └── firebase_auth.js          # Firebase configuration & auth logic
│   └── css/
│       └── auth.css                   # Authentication pages styling
├── templates/
│   ├── login_enhanced.html            # Login with Google Sign-In
│   └── register_enhanced.html         # Register with Google Sign-Up
└── auth_app.py                        # Backend with /api/google-auth endpoint
```

## API Endpoint

### POST `/api/google-auth`

**Request Body**:
```json
{
    "uid": "google_user_id",
    "email": "user@gmail.com",
    "displayName": "John Doe",
    "photoURL": "https://...",
    "emailVerified": true
}
```

**Response**:
```json
{
    "success": true,
    "message": "Login successful",
    "user": {
        "id": 1,
        "username": "john_doe"
    }
}
```

## Next Steps

1. ✅ Configure Firebase project
2. ✅ Update `firebase_auth.js` with your config
3. ✅ Test Google Sign-In locally
4. ✅ Deploy to production with HTTPS
5. ✅ Add production domain to Firebase

## Support

- **Firebase Documentation**: https://firebase.google.com/docs/auth
- **Google Sign-In Guide**: https://firebase.google.com/docs/auth/web/google-signin
- **Troubleshooting**: https://firebase.google.com/docs/auth/web/start#troubleshooting

---

**Your Google Authentication is now ready to use!** 🎉

Just update the Firebase configuration and start using Google Sign-In on both login and register pages.
