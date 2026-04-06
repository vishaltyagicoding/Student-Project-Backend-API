# Common API Errors & Solutions

## Authentication Errors

### ❌ Error: `{"password2": ["This field is required."]}`

**Cause:** Missing password confirmation field in registration

**Solution:**
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePass123",
  "password2": "SecurePass123",  // ← Add this field
  "first_name": "John",
  "last_name": "Doe"
}
```

**Note:** Both `password` and `password2` must match exactly.

---

### ❌ Error: `{"password": ["Passwords don't match"]}`

**Cause:** password and password2 fields have different values

**Solution:**
```json
{
  "password": "SecurePass123",
  "password2": "SecurePass123"  // ← Must be identical
}
```

---

### ❌ Error: `{"detail": "Authentication credentials were not provided."}`

**Cause:** Missing or invalid JWT token in request header

**Solution:**
```bash
# Add Authorization header
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Steps:**
1. Login first: `POST /api/auth/login/`
2. Copy the `access` token from response
3. Add to header: `Authorization: Bearer <access_token>`

---

### ❌ Error: `{"detail": "Given token not valid for any token type"}`

**Cause:** Token expired or invalid

**Solution:**
1. Use refresh token to get new access token:
```json
POST /api/auth/token/refresh/
{
  "refresh": "your_refresh_token"
}
```
2. Or login again to get new tokens

---

### ❌ Error: `{"email": ["user with this email already exists."]}`

**Cause:** Email already registered

**Solution:**
- Use a different email address
- Or login with existing credentials

---

## Student Errors

### ❌ Error: `{"student_id": ["student with this student id already exists."]}`

**Cause:** Student ID must be unique

**Solution:**
- Use a different student_id
- Check existing students: `GET /api/students/students/`

---

### ❌ Error: `{"email": ["student with this email already exists."]}`

**Cause:** Email already used by another student

**Solution:**
- Use a different email address
- Update existing student instead of creating new one

---

### ❌ Error: `{"error": "Selected course does not belong to the selected college."}`

**Cause:** Course-College mismatch

**Solution:**
1. Get college courses: `GET /api/students/colleges/{id}/courses/`
2. Use a course ID from that list
3. Or use `null` for course field

---

### ❌ Error: `{"error": "Selected branch does not belong to the selected college."}`

**Cause:** Branch-College mismatch

**Solution:**
1. Get college branches: `GET /api/students/colleges/{id}/branches/`
2. Use a branch ID from that list
3. Or use `null` for branch field

---

## Permission Errors

### ❌ Error: `{"detail": "You do not have permission to perform this action."}`

**Cause:** Insufficient permissions (Admin required)

**Solution:**
- Login with admin account
- Or request admin access from system administrator

**Admin-only endpoints:**
- Create/Update/Delete Colleges
- Create/Update/Delete Branches
- Create/Update/Delete Courses
- Send bulk emails

---

### ❌ Error: `403 Forbidden`

**Cause:** Trying to update/delete another user's student record

**Solution:**
- Only owners or admins can update/delete student records
- Login with correct account
- Or request admin access

---

## Validation Errors

### ❌ Error: `{"password": ["This password is too short. It must contain at least 8 characters."]}`

**Solution:**
- Use password with minimum 8 characters
- Include mix of letters, numbers, and symbols

---

### ❌ Error: `{"password": ["This password is too common."]}`

**Solution:**
- Avoid common passwords like "password123"
- Use unique, strong password

---

### ❌ Error: `{"email": ["Enter a valid email address."]}`

**Solution:**
```json
{
  "email": "user@example.com"  // ← Must be valid email format
}
```

---

## Request Format Errors

### ❌ Error: `{"detail": "JSON parse error"}`

**Cause:** Invalid JSON format

**Solution:**
- Check JSON syntax (commas, quotes, brackets)
- Use JSON validator
- Ensure Content-Type header is set:
```
Content-Type: application/json
```

---

### ❌ Error: `{"detail": "Method \"GET\" not allowed."}`

**Cause:** Wrong HTTP method

**Solution:**
Check endpoint documentation for correct method:
- List: GET
- Create: POST
- Update: PUT/PATCH
- Delete: DELETE

---

## Search & Filter Errors

### ❌ Error: `{"error": "Search query parameter \"q\" is required"}`

**Cause:** Missing search query

**Solution:**
```bash
GET /api/students/students/search/?q=john  # ← Add ?q=query
```

---

### ❌ Error: `{"error": "college_id parameter is required"}`

**Cause:** Missing required parameter

**Solution:**
```bash
GET /api/students/students/by_college/?college_id=1  # ← Add parameter
```

---

## Email Errors

### ❌ Error: `{"error": "student_ids, subject, and message are required"}`

**Cause:** Missing required fields in bulk email

**Solution:**
```json
POST /api/students/students/send_bulk_email/
{
  "student_ids": [1, 2, 3],
  "subject": "Important Announcement",
  "message": "Your message here"
}
```

---

### ❌ Error: `{"error": "No students found with provided IDs"}`

**Cause:** Invalid student IDs

**Solution:**
- Check student IDs exist: `GET /api/students/students/`
- Use valid student IDs from the list

---

## Server Errors

### ❌ Error: `500 Internal Server Error`

**Cause:** Server-side error

**Solution:**
1. Check server logs: `backend/logs/django.log`
2. Verify database connection
3. Check Celery worker is running (for emails)
4. Contact system administrator

---

### ❌ Error: `404 Not Found`

**Cause:** Invalid endpoint or resource doesn't exist

**Solution:**
- Check URL spelling
- Verify resource ID exists
- Review API documentation

---

## Quick Troubleshooting Checklist

✅ **Before making requests:**
1. Server is running: `python manage.py runserver`
2. Database is migrated: `python manage.py migrate`
3. For emails: Celery worker is running
4. Using correct base URL: `http://127.0.0.1:8000`

✅ **For authenticated requests:**
1. Login first to get token
2. Add Authorization header
3. Token not expired (refresh if needed)

✅ **For POST/PUT requests:**
1. Content-Type: application/json
2. Valid JSON format
3. All required fields included
4. Field values match expected types

✅ **For debugging:**
1. Check server logs: `backend/logs/django.log`
2. Use Postman collection for testing
3. Verify request format in documentation
4. Test with simple requests first

---

## Getting Help

If you encounter an error not listed here:

1. **Check logs:**
   ```bash
   tail -f backend/logs/django.log
   ```

2. **Run system check:**
   ```bash
   python manage.py check
   ```

3. **Test with Postman:**
   - Import `Student_Management_API.postman_collection.json`
   - Use pre-configured requests

4. **Review documentation:**
   - Live docs: http://127.0.0.1:8000/
   - API docs: `API_DOCUMENTATION.md`
   - Quick start: `QUICK_START.md`

---

**Remember:** Most errors are due to missing required fields or incorrect authentication. Always check the documentation for required fields! 📚
