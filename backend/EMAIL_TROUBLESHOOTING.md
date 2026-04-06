# 📧 Email Not Received? Get Your OTP Here!

## 🎯 Quick Solution

If you registered but didn't receive the OTP email, use this command to get your OTP:

```bash
python manage.py check_otp --email pythonbyvishal@gmail.com
```

**Your Current OTP: `911054`**

## ✅ Verify Your Account Now

Use this OTP in Postman:

```json
POST /api/auth/verify-otp/

{
  "email": "pythonbyvishal@gmail.com",
  "otp": "911054"
}
```

## 🔧 Why Email Didn't Send

The email configuration is working, but Gmail might be:
1. Blocking the email
2. Rate limiting
3. Marking it as spam
4. Requiring additional authentication

## 💡 Solutions

### Option 1: Use Console Email Backend (Development)

For testing, print emails to console instead of sending:

**Update `.env`:**
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

**Restart server:**
```bash
python manage.py runserver
```

Now when you register, the OTP will print in the console!

### Option 2: Check OTP from Database

Always use this command to get your OTP:

```bash
python manage.py check_otp --email YOUR_EMAIL
```

**Example output:**
```
✓ User found: pythonbyvishal@gmail.com
  Username: vishal
  Active: False

📧 OTP Details:
  OTP: 911054
  Created: 2026-03-28 13:38:46
  Expired: False
  Used: False

✓ Valid OTP: 911054
```

### Option 3: Check Gmail Settings

1. **Check Spam/Junk folder**
2. **Allow less secure apps** (if using regular password)
3. **Use App Password** (recommended)
   - Go to: https://myaccount.google.com/apppasswords
   - Generate new app password
   - Update `.env` with new password

### Option 4: Use Different Email Service

For production, use professional email services:

**SendGrid:**
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
```

**AWS SES:**
```bash
pip install django-ses
```

```env
EMAIL_BACKEND=django_ses.SESBackend
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_SES_REGION_NAME=us-east-1
```

## 🧪 Test Email Sending

### Test 1: Django Shell

```bash
python manage.py shell
```

```python
from django.core.mail import send_mail

send_mail(
    'Test Email',
    'This is a test message.',
    'alberttyagi123@gmail.com',
    ['pythonbyvishal@gmail.com'],
    fail_silently=False,
)
```

If this fails, you'll see the error message.

### Test 2: Management Command

```bash
python manage.py test_email --email pythonbyvishal@gmail.com --type simple
```

## 📋 Complete Workflow

### For Development (Recommended):

1. **Use Console Backend:**
   ```env
   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
   ```

2. **Register user**

3. **Check console output for OTP**

4. **Verify OTP**

### For Testing with Database:

1. **Register user**

2. **Get OTP from database:**
   ```bash
   python manage.py check_otp --email pythonbyvishal@gmail.com
   ```

3. **Copy OTP and verify**

### For Production:

1. **Use professional email service** (SendGrid, AWS SES)

2. **Configure proper DNS records** (SPF, DKIM, DMARC)

3. **Monitor email delivery**

## 🎯 Your Current Status

✅ **User registered:** pythonbyvishal@gmail.com
✅ **OTP generated:** 911054
✅ **OTP valid:** Yes (not expired)
❌ **Email sent:** No (but OTP works!)

## 🚀 Next Steps

1. **Verify your account now:**
   ```bash
   POST /api/auth/verify-otp/
   {
     "email": "pythonbyvishal@gmail.com",
     "otp": "911054"
   }
   ```

2. **For future registrations:**
   - Use `check_otp` command to get OTP
   - Or switch to console email backend
   - Or fix Gmail configuration

## 🔍 Check OTP Command Usage

```bash
# Check OTP for any email
python manage.py check_otp --email user@example.com

# Output shows:
# - User details
# - Current valid OTP
# - OTP expiration status
# - All previous OTPs
```

## 📝 Common Issues

### Issue: "User not found"
**Solution:** Register first using `/api/auth/register/`

### Issue: "No OTP found"
**Solution:** Register again or use resend-otp endpoint

### Issue: "OTP has expired"
**Solution:** Use resend-otp endpoint:
```bash
POST /api/auth/resend-otp/
{
  "email": "pythonbyvishal@gmail.com"
}
```
Then run `check_otp` command again.

### Issue: Email still not sending
**Solution:** Use console backend for development:
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

## 💡 Pro Tips

1. **Development:** Always use console email backend
2. **Testing:** Use `check_otp` command
3. **Production:** Use SendGrid or AWS SES
4. **Debugging:** Check `backend/logs/django.log`

## 🆘 Still Having Issues?

1. **Check server logs:**
   ```bash
   tail -f backend/logs/django.log
   ```

2. **Verify email config:**
   ```bash
   cat backend/.env | grep EMAIL
   ```

3. **Test email manually:**
   ```bash
   python manage.py test_email --email pythonbyvishal@gmail.com --type simple
   ```

---

**Your OTP is ready! Use `911054` to verify your account now! 🎉**
