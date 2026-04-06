# 🔐 OTP Email Verification Guide

## Overview

Your Student Management System uses **OTP (One-Time Password)** for email verification during registration. This ensures that users provide valid email addresses.

## 📧 Email Configuration

Currently configured email: `alberttyagi123@gmail.com`

OTP emails will be sent from this address to users who register.

## 🔄 Registration & Verification Flow

### Step 1: Register User

```bash
POST /api/auth/register/
Content-Type: application/json

{
  "email": "pythonbyvishal@gmail.com",
  "username": "vishal",
  "password": "SecurePass123",
  "password2": "SecurePass123",
  "first_name": "Vishal",
  "last_name": "Python"
}
```

**Response:**
```json
{
  "detail": "Registration successful. Please check your email for the OTP to verify your account."
}
```

**What happens:**
- ✅ User account created (but inactive)
- ✅ 6-digit OTP generated
- ✅ Email sent to `pythonbyvishal@gmail.com` with OTP
- ✅ OTP valid for 10 minutes

### Step 2: Check Email

Check your inbox at `pythonbyvishal@gmail.com` for an email with subject:
**"Your Email Verification OTP"**

Email content:
```
Your OTP is: 123456
It expires in 10 minutes.
```

### Step 3: Verify OTP

```bash
POST /api/auth/verify-otp/
Content-Type: application/json

{
  "email": "pythonbyvishal@gmail.com",
  "otp": "123456"
}
```

**Success Response:**
```json
{
  "detail": "Email verified successfully.",
  "user": {
    "id": 1,
    "email": "pythonbyvishal@gmail.com",
    "username": "vishal",
    "first_name": "Vishal",
    "last_name": "Python"
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**What happens:**
- ✅ OTP marked as used
- ✅ User account activated
- ✅ JWT tokens returned
- ✅ User can now login

### Step 4: Login (After Verification)

```bash
POST /api/auth/login/
Content-Type: application/json

{
  "email": "pythonbyvishal@gmail.com",
  "password": "SecurePass123"
}
```

## 🔄 Resend OTP

If OTP expired or not received:

```bash
POST /api/auth/resend-otp/
Content-Type: application/json

{
  "email": "pythonbyvishal@gmail.com"
}
```

**Response:**
```json
{
  "detail": "OTP resent successfully."
}
```

**What happens:**
- ✅ Old OTPs invalidated
- ✅ New 6-digit OTP generated
- ✅ New email sent
- ✅ New OTP valid for 10 minutes

## 📱 Using Postman

### 1. Import Collection
- Import `Student_Management_API.postman_collection.json`
- Email is pre-configured to `pythonbyvishal@gmail.com`

### 2. Register
- Open **Authentication → Register**
- Click **Send**
- Check email for OTP

### 3. Verify OTP
- Open **Authentication → Verify OTP**
- Replace `"otp": "123456"` with actual OTP from email
- Click **Send**
- Tokens automatically saved!

### 4. Resend OTP (if needed)
- Open **Authentication → Resend OTP**
- Click **Send**
- Check email for new OTP

## ⚠️ Common Errors

### ❌ Error: "Invalid OTP"

**Causes:**
- Wrong OTP entered
- OTP already used
- OTP expired (>10 minutes)

**Solution:**
- Check email for correct OTP
- Request new OTP using resend endpoint

---

### ❌ Error: "OTP has expired. Please request a new one."

**Cause:** OTP older than 10 minutes

**Solution:**
```bash
POST /api/auth/resend-otp/
{
  "email": "pythonbyvishal@gmail.com"
}
```

---

### ❌ Error: "No pending verification found for this email."

**Causes:**
- Email already verified
- Email not registered

**Solution:**
- If already verified, just login
- If not registered, register first

---

### ❌ Error: "User not found."

**Cause:** Email not registered

**Solution:**
- Register first using `/api/auth/register/`

---

### ❌ Error: "Your account has been disabled."

**Cause:** Account not verified yet

**Solution:**
- Verify OTP first
- Or resend OTP if expired

---

## 🧪 Testing Flow

### Complete Test Scenario

```bash
# 1. Register
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "pythonbyvishal@gmail.com",
    "username": "vishal",
    "password": "SecurePass123",
    "password2": "SecurePass123",
    "first_name": "Vishal",
    "last_name": "Python"
  }'

# Response: Registration successful. Check email.

# 2. Check email at pythonbyvishal@gmail.com
# Get OTP: 123456

# 3. Verify OTP
curl -X POST http://127.0.0.1:8000/api/auth/verify-otp/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "pythonbyvishal@gmail.com",
    "otp": "123456"
  }'

# Response: Email verified + JWT tokens

# 4. Use tokens for authenticated requests
curl -X GET http://127.0.0.1:8000/api/students/students/ \
  -H "Authorization: Bearer <access_token>"
```

## 📊 OTP Details

| Property | Value |
|----------|-------|
| Length | 6 digits |
| Validity | 10 minutes |
| Type | Numeric only (0-9) |
| Reusable | No (one-time use) |
| Email From | alberttyagi123@gmail.com |
| Email To | pythonbyvishal@gmail.com (for testing) |

## 🔒 Security Features

✅ **OTP expires after 10 minutes**
✅ **One-time use only**
✅ **Old OTPs invalidated on resend**
✅ **Account inactive until verified**
✅ **Cannot login without verification**

## 💡 Tips

1. **Check spam folder** if email not received
2. **OTP is case-sensitive** (though it's only numbers)
3. **Request new OTP** if expired
4. **Save JWT tokens** after verification
5. **Use Postman** for easier testing

## 🎯 Quick Reference

### All OTP Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/auth/register/` | POST | Register & send OTP |
| `/api/auth/verify-otp/` | POST | Verify OTP & activate |
| `/api/auth/resend-otp/` | POST | Resend new OTP |
| `/api/auth/login/` | POST | Login (after verification) |

## 📧 Email Not Received?

### Troubleshooting Steps:

1. **Check spam/junk folder**
2. **Verify email address is correct**
3. **Check server logs:**
   ```bash
   tail -f backend/logs/django.log
   ```
4. **Verify email configuration in .env:**
   ```env
   EMAIL_HOST_USER=alberttyagi123@gmail.com
   EMAIL_HOST_PASSWORD=vjilmztooxjgexzg
   ```
5. **Test email manually:**
   ```bash
   python manage.py shell
   
   from django.core.mail import send_mail
   send_mail(
       'Test Email',
       'This is a test.',
       'alberttyagi123@gmail.com',
       ['pythonbyvishal@gmail.com'],
       fail_silently=False,
   )
   ```

## 🚀 Production Recommendations

For production deployment:

1. **Use professional email service:**
   - SendGrid
   - AWS SES
   - Mailgun

2. **Add email templates:**
   - HTML formatted emails
   - Company branding
   - Better styling

3. **Implement rate limiting:**
   - Limit OTP requests per email
   - Prevent spam/abuse

4. **Add SMS backup:**
   - Send OTP via SMS too
   - Use Twilio or similar

5. **Monitor email delivery:**
   - Track delivery rates
   - Handle bounces
   - Log failures

---

**Your test email `pythonbyvishal@gmail.com` is now configured in the Postman collection! 🎉**
