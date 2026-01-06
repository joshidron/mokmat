# 🔥 Firebase Setup Guide

Follow these steps to set up the backend for your AI Interview System.

## 1. Create a Firebase Project
1. Go to the [Firebase Console](https://console.firebase.google.com/).
2. Click **"Add project"**.
3. Name your project (e.g., `ai-interview-system`).
4. Disable Google Analytics (optional, for simplicity) and click **"Create project"**.

## 2. Enable Authentication
1. In the left sidebar, click **Build** > **Authentication**.
2. Click **"Get started"**.
3. Select **Email/Password**:
   - Enable "Email/Password".
   - Click **Save**.
4. Click **"Add new provider"** > **Google**:
   - Enable it.
   - Set the support email.
   - Click **Save**.

## 3. Setup Realtime Database
1. In the left sidebar, click **Build** > **Realtime Database**.
2. Click **"Create Database"**.
3. Select a location (e.g., United States).
4. Start in **Test mode** (for easier development) or **Locked mode** (you will need to update rules).
   - *Recommendation for now:* **Test mode** (Read/write: true).
5. Click **Enable**.

## 4. Get Web Configuration (For Frontend)
1. Click the **Gear icon** (Project settings) next to "Project Overview".
2. Scroll down to "Your apps".
3. Click the **Web icon** (`</>`).
4. Register app (e.g., `InterviewWeb`).
5. **Copy the `firebaseConfig` object**. You will need this for `static/js/firebase_config.js`.

It usually looks like this:
```javascript
const firebaseConfig = {
  apiKey: "AIzaSy...",
  authDomain: "project-id.firebaseapp.com",
  databaseURL: "https://project-id.firebaseio.com",
  projectId: "project-id",
  storageBucket: "project-id.firebasestorage.app",
  messagingSenderId: "...",
  appId: "..."
};
```

## 5. Get Service Account Key (For Backend)
1. In Project Settings, go to the **Service accounts** tab.
2. Click **"Generate new private key"**.
3. Save the `.json` file.
4. Rename it to `serviceAccountKey.json`.
5. Move it to your project root folder (`d:\codewave\`).
