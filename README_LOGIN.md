# Interview System - Login Required Version

## Overview
This application now **ALWAYS requires login** before users can access the interview system.

## What Changed
- **`app.py`** is now the authenticated version (previously `auth_app.py`)
- **`app_no_auth.py`** is the backup of the old version without authentication
- All routes are protected and require user authentication

## Features
✅ **User Authentication**
- Email/Password registration and login
- Google OAuth integration
- Session management

✅ **Interview Limits**
- Maximum 2 interviews per 24 hours
- Maximum 5 interviews total per user
- Automatic limit tracking

✅ **Security Features**
- Tab switching detection (3-strike system)
- User ban system for violations
- Secure password hashing

✅ **Monitoring & Tracking**
- Body posture tracking
- Eye movement tracking
- Focus percentage monitoring
- Comprehensive event logging

✅ **PDF Report Generation**
- Dynamic report generation based on performance
- Detailed analytics and feedback
- Downloadable PDF reports

## How to Run

### Option 1: Using the Batch Script (Recommended)
```bash
start_with_login.bat
```

### Option 2: Direct Python Command
```bash
python app.py
```

### Option 3: PowerShell
```powershell
python app.py
```

## First Time Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize Database**
   The database will be created automatically on first run.

3. **Configure Google OAuth (Optional)**
   - Get credentials from [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
   - Set environment variables:
     ```bash
     set GOOGLE_CLIENT_ID=your_client_id
     set GOOGLE_CLIENT_SECRET=your_client_secret
     ```

## User Flow

1. **First Visit** → Redirected to `/login`
2. **New User** → Click "Register" → Create account
3. **Existing User** → Enter credentials → Login
4. **Authenticated** → Access interview system
5. **Complete Interview** → Generate PDF report

## Database Structure

The system uses SQLite with the following tables:
- `users` - User accounts and authentication
- `interview_sessions` - Interview session data
- `answers` - User answers to questions
- `tracking_events` - Monitoring events
- `user_violations` - Violation tracking and bans

## API Endpoints (All Protected)

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - Login user
- `POST /api/logout` - Logout user
- `POST /api/google-auth` - Google OAuth authentication

### Interview
- `POST /api/start-interview` - Start new interview (checks limits)
- `GET /api/get-question/<session_id>` - Get current question
- `POST /api/submit-answer/<session_id>` - Submit answer
- `GET /api/get-results/<session_id>` - Get interview results
- `GET /api/generate-report/<session_id>` - Generate PDF report

### Monitoring
- `POST /api/report-tab-switch/<session_id>` - Report tab switch
- `POST /api/track-event/<session_id>` - Track monitoring events
- `POST /api/update-tracking-metrics/<session_id>` - Update metrics

### User Stats
- `GET /api/check-limits` - Check interview limits
- `GET /api/user-stats` - Get user statistics

## Security Notes

⚠️ **Important Security Considerations:**

1. **Password Security**: Passwords are hashed using SHA-256. For production, consider using bcrypt or argon2.

2. **Session Security**: The app uses Flask sessions. Make sure to set a strong `SECRET_KEY` in production.

3. **Google OAuth**: Only works with proper credentials. Set up your OAuth app in Google Cloud Console.

4. **Database**: Currently using SQLite. For production, consider PostgreSQL or MySQL.

## Troubleshooting

### "Not authenticated" Error
- Clear browser cookies and login again
- Check if session is active

### Google OAuth Not Working
- Verify `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` are set
- Check OAuth redirect URIs in Google Cloud Console

### Interview Limit Reached
- Wait 24 hours for daily limit reset
- Contact admin if you need limit increase

### Database Errors
- Delete `interview_system.db` to reset (WARNING: loses all data)
- Run `python app.py` to recreate database

## File Structure

```
codewave/
├── app.py                    # Main application (with authentication)
├── app_no_auth.py           # Backup (without authentication)
├── auth_app.py              # Original authenticated version
├── train_model.py           # ML model training
├── report_generator.py      # PDF report generation
├── interview_system.db      # SQLite database
├── templates/
│   ├── login_enhanced.html  # Login page
│   ├── register_enhanced.html # Registration page
│   └── enhanced_interview.html # Main interview interface
├── static/
│   ├── css/                 # Stylesheets
│   └── js/                  # JavaScript files
└── reports/                 # Generated PDF reports
```

## Support

For issues or questions:
1. Check this README
2. Review the troubleshooting section
3. Check the console output for error messages
4. Review the database for data integrity

---

**Version**: 2.0 (Login Required)  
**Last Updated**: 2026-01-06
