# 📝 User Registration Guide

## Quick Registration Example

### ✅ Correct Registration Request

```bash
POST http://127.0.0.1:8000/api/auth/register/
Content-Type: application/json

{
  "email": "john.doe@example.com",
  "username": "johndoe",
  "password": "SecurePass123",
  "password2": "SecurePass123",
  "first_name": "John",
  "last_name": "Doe"
}
```

### 📋 Required Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | ✅ Yes | Valid email address (must be unique) |
| `username` | string | ✅ Yes | Username (must be unique) |
| `password` | string | ✅ Yes | Password (min 8 characters) |
| `password2` | string | ✅ Yes | Password confirmation (must match password) |
| `first_name` | string | ❌ No | User's first name |
| `last_name` | string | ❌ No | User's last name |

### ⚠️ Important Notes

1. **password2 is REQUIRED** - This is for password confirmation
2. **password and password2 must match exactly**
3. **Email must be unique** - Cannot register with existing email
4. **Username must be unique** - Cannot register with existing username
5. **Password must be strong** - Minimum 8 characters, avoid common passwords

## Step-by-Step Guide

### Using Postman

1. **Open Postman**
2. **Import Collection:**
   - File → Import
   - Select `Student_Management_API.postman_collection.json`
3. **Navigate to:**
   - Authentication → Register
4. **Modify the request body:**
   ```json
   {
     "email": "your-email@example.com",
     "username": "your-username",
     "password": "YourPassword123",
     "password2": "YourPassword123",
     "first_name": "Your First Name",
     "last_name": "Your Last Name"
   }
   ```
5. **Click "Send"**

### Using cURL

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "username": "johndoe",
    "password": "SecurePass123",
    "password2": "SecurePass123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Using Python

```python
import requests

url = "http://127.0.0.1:8000/api/auth/register/"
data = {
    "email": "john.doe@example.com",
    "username": "johndoe",
    "password": "SecurePass123",
    "password2": "SecurePass123",
    "first_name": "John",
    "last_name": "Doe"
}

response = requests.post(url, json=data)
print(response.json())
```

### Using JavaScript (Fetch)

```javascript
fetch('http://127.0.0.1:8000/api/auth/register/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'john.doe@example.com',
    username: 'johndoe',
    password: 'SecurePass123',
    password2: 'SecurePass123',
    first_name: 'John',
    last_name: 'Doe'
  })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

## Success Response

```json
{
  "id": 1,
  "email": "john.doe@example.com",
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "date_joined": "2024-01-01T00:00:00Z"
}
```

## Common Errors

### ❌ Missing password2

```json
{
  "password2": ["This field is required."]
}
```

**Fix:** Add `password2` field with same value as `password`

### ❌ Passwords don't match

```json
{
  "password": ["Passwords don't match"]
}
```

**Fix:** Ensure `password` and `password2` are identical

### ❌ Email already exists

```json
{
  "email": ["user with this email already exists."]
}
```

**Fix:** Use a different email or login with existing account

### ❌ Weak password

```json
{
  "password": ["This password is too common."]
}
```

**Fix:** Use a stronger, more unique password

## After Registration

Once registered successfully, you can:

1. **Login to get JWT tokens:**
   ```bash
   POST /api/auth/login/
   {
     "email": "john.doe@example.com",
     "password": "SecurePass123"
   }
   ```

2. **Use the access token for authenticated requests:**
   ```bash
   GET /api/students/students/
   Authorization: Bearer <your_access_token>
   ```

## Complete Flow Example

```bash
# 1. Register
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "username": "johndoe",
    "password": "SecurePass123",
    "password2": "SecurePass123",
    "first_name": "John",
    "last_name": "Doe"
  }'

# 2. Login
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "SecurePass123"
  }'

# Response: Save the access token
# {
#   "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
#   "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
# }

# 3. Use token for authenticated requests
curl -X GET http://127.0.0.1:8000/api/students/students/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

## Password Requirements

✅ **Valid passwords:**
- `SecurePass123`
- `MyP@ssw0rd!`
- `StrongPassword2024`

❌ **Invalid passwords:**
- `password` (too common)
- `12345678` (too common)
- `abc123` (too short)

## Tips

1. **Use strong passwords** - Mix of letters, numbers, and symbols
2. **Keep credentials secure** - Don't share passwords
3. **Test in Postman first** - Easier to debug
4. **Check response status** - 201 = success, 400 = validation error
5. **Save tokens securely** - Store access/refresh tokens safely

## Need Help?

- 📖 Full API docs: http://127.0.0.1:8000/
- 🔧 Common errors: `COMMON_ERRORS.md`
- 🚀 Quick start: `QUICK_START.md`
- 📚 API reference: `API_DOCUMENTATION.md`

---

**Happy Coding! 🎉**
