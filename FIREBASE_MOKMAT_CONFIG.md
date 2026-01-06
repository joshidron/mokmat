# Firebase Configuration for mokmat-c3474 Project

## Your Firebase Project Details

**Project ID**: `mokmat-c3474`
**Project URL**: https://console.firebase.google.com/project/mokmat-c3474

## Step-by-Step Configuration

### 1. Get Your Firebase Configuration

1. **Go to Project Settings**:
   - Open: https://console.firebase.google.com/project/mokmat-c3474/settings/general
   - Scroll down to "Your apps" section
   - If you don't have a web app, click "Add app" (</> icon)
   - If you already have a web app, you'll see the config

2. **Copy the Firebase Config**:
   - Look for the `firebaseConfig` object
   - It should look like this:
   ```javascript
   const firebaseConfig = {
       apiKey: "AIza...",
       authDomain: "mokmat-c3474.firebaseapp.com",
       projectId: "mokmat-c3474",
       storageBucket: "mokmat-c3474.appspot.com",
       messagingSenderId: "...",
       appId: "...",
       measurementId: "..."
   };
   ```

### 2. Enable Authentication

1. **Go to Authentication**:
   - Visit: https://console.firebase.google.com/project/mokmat-c3474/authentication
   - Click "Get started" (if first time)

2. **Enable Google Sign-In**:
   - Click "Sign-in method" tab
   - Find "Google" provider
   - Click on it
   - Toggle "Enable"
   - Select your support email
   - Click "Save"

3. **Add Authorized Domains**:
   - In Authentication → Settings → Authorized domains
   - Add: `localhost` (for development)
   - Add your production domain later

### 3. Set Up Firestore Database

1. **Go to Firestore Database**:
   - Visit: https://console.firebase.google.com/project/mokmat-c3474/firestore
   - Click "Create database"

2. **Choose Mode**:
   - Select "Start in test mode" (for development)
   - Click "Next"

3. **Choose Location**:
   - Select closest region (e.g., "asia-south1" for India)
   - Click "Enable"

4. **Wait for Database Creation**:
   - This may take a minute

### 4. Configure Security Rules

Once Firestore is created, update security rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users collection
    match /users/{userId} {
      allow read: if request.auth != null;
      allow write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Interview sessions collection
    match /interview_sessions/{sessionId} {
      allow read, write: if request.auth != null;
    }
    
    // Tracking events collection
    match /tracking_events/{eventId} {
      allow read, write: if request.auth != null;
    }
  }
}
```

### 5. Update Your Application

After getting your Firebase config, update these files:

#### File 1: `static/js/firebase_auth.js`

Replace lines 6-13 with your actual config:
```javascript
const firebaseConfig = {
    apiKey: "YOUR_ACTUAL_API_KEY",
    authDomain: "mokmat-c3474.firebaseapp.com",
    projectId: "mokmat-c3474",
    storageBucket: "mokmat-c3474.appspot.com",
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
    appId: "YOUR_APP_ID",
    measurementId: "YOUR_MEASUREMENT_ID"
};
```

## Quick Setup Checklist

- [ ] Go to Firebase Console
- [ ] Add web app (if not exists)
- [ ] Copy Firebase configuration
- [ ] Enable Google Authentication
- [ ] Create Firestore Database
- [ ] Update `firebase_auth.js` with your config
- [ ] Test Google Sign-In on localhost

## Testing

1. **Start your server**:
   ```cmd
   python auth_app.py
   ```

2. **Open browser**:
   ```
   http://localhost:5000/login
   ```

3. **Click "Continue with Google"**:
   - Should open Google Sign-In popup
   - Select your account
   - Should redirect to main page

4. **Verify in Firebase Console**:
   - Go to Authentication → Users
   - You should see your account listed

## Troubleshooting

### Can't find Firebase config?
- Go to: https://console.firebase.google.com/project/mokmat-c3474/settings/general
- Scroll to "Your apps"
- Click on your web app
- Config is shown in the code snippet

### Google Sign-In not working?
- Check if Google provider is enabled in Authentication
- Verify `localhost` is in Authorized domains
- Check browser console for errors

### Database errors?
- Make sure Firestore is created
- Check security rules allow authenticated users
- Verify Firebase SDK is loaded correctly

## Next Steps

After configuration:
1. Test Google Sign-In
2. Test user registration
3. Verify data is saved to Firestore
4. Test interview tracking features

---

**Your Firebase project is ready to be configured!**

Just follow the steps above to get your configuration and update the files.
