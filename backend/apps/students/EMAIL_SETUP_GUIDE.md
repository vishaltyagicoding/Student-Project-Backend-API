# Email Setup Guide for Student Registration

## Quick Start

### Step 1: Configure Email Settings

Add these to your `.env` file:

```env
# Gmail Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

### Step 2: Gmail App Password Setup

1. Go to your Google Account: https://myaccount.google.com/
2. Select Security
3. Enable 2-Step Verification (if not already enabled)
4. Go to App Passwords: https://myaccount.google.com/apppasswords
5. Select "Mail" and your device
6. Copy the 16-character password
7. Use this password in `EMAIL_HOST_PASSWORD`

### Step 3: Start Celery Worker

```bash
# Linux/Mac
celery -A config worker -l info

# Windows
celery -A config worker -l info --pool=solo
```

### Step 4: Test Email Configuration

```bash
# Test simple email
python manage.py test_email --email your-test@email.com --type simple

# Test registration email (requires Celery worker running)
python manage.py test_email --email your-test@email.com --type registration
```

## Development Mode (Console Backend)

For development, you can print emails to console instead of sending them:

In `settings.py`, add:
```python
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## Email Providers

### Gmail
- Host: smtp.gmail.com
- Port: 587
- TLS: True
- Requires App Password

### Outlook/Hotmail
```env
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

### SendGrid (Production)
```env
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
```

### AWS SES (Production)
```env
EMAIL_BACKEND=django_ses.SESBackend
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_SES_REGION_NAME=us-east-1
```

## How It Works

### 1. Student Registration Flow

```
Student Created → Signal Triggered → Celery Task Queued → Email Sent
```

### 2. Files Involved

- `signals.py` - Listens for student creation/update
- `tasks.py` - Contains Celery tasks for sending emails
- `templates/emails/` - Email HTML templates

### 3. Automatic Emails

When a student is created:
- Welcome email is automatically sent
- Contains student ID, email, and college name
- Processed asynchronously (non-blocking)

When a student is updated:
- Update notification email is sent
- Informs student of changes

## Troubleshooting

### Email not sending?

1. Check Celery worker is running
2. Verify email credentials in .env
3. Check logs: `backend/logs/django.log`
4. Test with console backend first

### Gmail "Less secure app" error?

- Use App Password instead of regular password
- Enable 2-Step Verification first

### Celery task not processing?

```bash
# Check Celery worker logs
celery -A config worker -l debug

# Check Redis is running
redis-cli ping
```

### Email goes to spam?

For production:
- Configure SPF records
- Set up DKIM
- Configure DMARC
- Use dedicated email service (SendGrid, AWS SES)

## Production Recommendations

1. Use dedicated email service (SendGrid, AWS SES, Mailgun)
2. Set up proper DNS records (SPF, DKIM, DMARC)
3. Monitor email delivery rates
4. Implement email bounce handling
5. Use email templates with company branding
6. Set up rate limiting
7. Configure retry policies
8. Monitor Celery queue length

## Testing

### Manual Test in Django Shell

```python
python manage.py shell

from apps.students.models import Student
from apps.students.tasks import send_student_registration_email

# Create test student
student = Student.objects.create(
    first_name="Test",
    last_name="User",
    email="test@example.com",
    student_id="TEST001"
)

# Email will be sent automatically via signal
```

### Check Celery Task Status

```python
from celery.result import AsyncResult

task_id = 'your-task-id'
result = AsyncResult(task_id)
print(result.state)  # PENDING, SUCCESS, FAILURE
print(result.info)   # Task result or error
```

## Support

For issues or questions:
- Check Django logs: `backend/logs/django.log`
- Check Celery worker output
- Verify email configuration
- Test with console backend first
