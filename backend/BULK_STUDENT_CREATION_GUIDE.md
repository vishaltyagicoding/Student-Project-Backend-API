# 📦 Bulk Student Creation Guide

## Overview

Create multiple students in a single API call. Perfect for importing student data from CSV, Excel, or other sources.

## 🚀 Endpoint

```
POST /api/students/students/bulk_create/
```

**Authentication:** Required (JWT Token)

## 📝 Request Format

```json
{
  "students": [
    {
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@example.com",
      "student_id": "STU001",
      "college": 1,
      "course": 1,
      "branch": 1
    },
    {
      "first_name": "Jane",
      "last_name": "Smith",
      "email": "jane.smith@example.com",
      "student_id": "STU002",
      "college": 1,
      "course": 1,
      "branch": 1
    }
  ]
}
```

## ✅ Success Response

```json
{
  "success": 2,
  "failed": 0,
  "created_students": [
    {
      "index": 0,
      "student_id": "STU001",
      "email": "john.doe@example.com",
      "id": 1
    },
    {
      "index": 1,
      "student_id": "STU002",
      "email": "jane.smith@example.com",
      "id": 2
    }
  ]
}
```

## ⚠️ Partial Success Response

If some students fail validation:

```json
{
  "success": 1,
  "failed": 1,
  "created_students": [
    {
      "index": 0,
      "student_id": "STU001",
      "email": "john.doe@example.com",
      "id": 1
    }
  ],
  "errors": [
    {
      "index": 1,
      "data": {
        "first_name": "Jane",
        "email": "invalid-email",
        "student_id": "STU002"
      },
      "errors": {
        "email": ["Enter a valid email address."]
      }
    }
  ]
}
```

## 📋 Required Fields

Each student object must include:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `first_name` | string | ✅ Yes | Student's first name |
| `last_name` | string | ✅ Yes | Student's last name |
| `email` | string | ✅ Yes | Unique email address |
| `student_id` | string | ✅ Yes | Unique student ID |
| `college` | integer | ❌ No | College ID |
| `course` | integer | ❌ No | CollegeCourse ID |
| `branch` | integer | ❌ No | CollegeBranch ID |

## 🎯 Complete Example

### Step 1: Prepare Your Data

```json
{
  "students": [
    {
      "first_name": "Alice",
      "last_name": "Williams",
      "email": "alice.williams@example.com",
      "student_id": "CS2024001",
      "college": 1,
      "course": 1,
      "branch": 1
    },
    {
      "first_name": "Bob",
      "last_name": "Brown",
      "email": "bob.brown@example.com",
      "student_id": "CS2024002",
      "college": 1,
      "course": 1,
      "branch": 1
    },
    {
      "first_name": "Charlie",
      "last_name": "Davis",
      "email": "charlie.davis@example.com",
      "student_id": "CS2024003",
      "college": 1,
      "course": 1,
      "branch": 1
    },
    {
      "first_name": "Diana",
      "last_name": "Miller",
      "email": "diana.miller@example.com",
      "student_id": "CS2024004",
      "college": 1,
      "course": 1,
      "branch": 1
    },
    {
      "first_name": "Eve",
      "last_name": "Wilson",
      "email": "eve.wilson@example.com",
      "student_id": "CS2024005",
      "college": 1,
      "course": 1,
      "branch": 1
    }
  ]
}
```

### Step 2: Send Request

```bash
curl -X POST http://127.0.0.1:8000/api/students/students/bulk_create/ \
  -H "Authorization: Bearer <your_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "students": [
      {
        "first_name": "Alice",
        "last_name": "Williams",
        "email": "alice.williams@example.com",
        "student_id": "CS2024001",
        "college": 1,
        "course": 1,
        "branch": 1
      }
    ]
  }'
```

### Step 3: Check Response

```json
{
  "success": 5,
  "failed": 0,
  "created_students": [
    {"index": 0, "student_id": "CS2024001", "email": "alice.williams@example.com", "id": 1},
    {"index": 1, "student_id": "CS2024002", "email": "bob.brown@example.com", "id": 2},
    {"index": 2, "student_id": "CS2024003", "email": "charlie.davis@example.com", "id": 3},
    {"index": 3, "student_id": "CS2024004", "email": "diana.miller@example.com", "id": 4},
    {"index": 4, "student_id": "CS2024005", "email": "eve.wilson@example.com", "id": 5}
  ]
}
```

## 🧪 Using Postman

1. **Open Postman**
2. **Navigate to:** Students → Bulk Create Students
3. **Modify the request body** with your student data
4. **Click "Send"**
5. **Check response** for success/failure details

## 📊 Import from CSV/Excel

### Python Script Example

```python
import requests
import pandas as pd

# Read CSV file
df = pd.read_csv('students.csv')

# Convert to required format
students = []
for _, row in df.iterrows():
    students.append({
        'first_name': row['first_name'],
        'last_name': row['last_name'],
        'email': row['email'],
        'student_id': row['student_id'],
        'college': int(row['college']),
        'course': int(row['course']),
        'branch': int(row['branch'])
    })

# Send bulk create request
url = 'http://127.0.0.1:8000/api/students/students/bulk_create/'
headers = {
    'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
    'Content-Type': 'application/json'
}
data = {'students': students}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

### CSV Format

```csv
first_name,last_name,email,student_id,college,course,branch
Alice,Williams,alice.williams@example.com,CS2024001,1,1,1
Bob,Brown,bob.brown@example.com,CS2024002,1,1,1
Charlie,Davis,charlie.davis@example.com,CS2024003,1,1,1
```

## ⚠️ Common Errors

### Error 1: Duplicate Email

```json
{
  "success": 0,
  "failed": 1,
  "errors": [
    {
      "index": 0,
      "data": {...},
      "errors": {
        "email": ["student with this email already exists."]
      }
    }
  ]
}
```

**Solution:** Ensure all emails are unique

### Error 2: Duplicate Student ID

```json
{
  "errors": {
    "student_id": ["student with this student id already exists."]
  }
}
```

**Solution:** Ensure all student IDs are unique

### Error 3: Invalid College/Course/Branch

```json
{
  "errors": {
    "course": ["Invalid pk \"999\" - object does not exist."]
  }
}
```

**Solution:** 
- Verify college, course, and branch IDs exist
- Remember: Use CollegeCourse and CollegeBranch IDs, not direct Course/Branch IDs

### Error 4: Missing Required Fields

```json
{
  "errors": {
    "first_name": ["This field is required."],
    "email": ["This field is required."]
  }
}
```

**Solution:** Include all required fields for each student

## 💡 Best Practices

### 1. Batch Size

For optimal performance:
- **Recommended:** 50-100 students per request
- **Maximum:** 500 students per request
- For larger imports, split into multiple requests

### 2. Validation Before Import

```python
# Validate data before sending
def validate_student(student):
    required_fields = ['first_name', 'last_name', 'email', 'student_id']
    for field in required_fields:
        if not student.get(field):
            return False, f"Missing {field}"
    
    # Validate email format
    if '@' not in student['email']:
        return False, "Invalid email format"
    
    return True, "Valid"

# Check all students before sending
for student in students:
    valid, message = validate_student(student)
    if not valid:
        print(f"Invalid student: {message}")
```

### 3. Handle Partial Success

```python
response = requests.post(url, json=data, headers=headers)
result = response.json()

print(f"✓ Successfully created: {result['success']} students")
print(f"✗ Failed: {result['failed']} students")

if result.get('errors'):
    print("\nErrors:")
    for error in result['errors']:
        print(f"  Student at index {error['index']}: {error['errors']}")
```

### 4. Email Notifications

After bulk creation, welcome emails are sent automatically to all students (if Celery is running).

## 📈 Performance Tips

1. **Use bulk_create for large datasets** (50+ students)
2. **Validate data before sending** to avoid partial failures
3. **Split large imports** into batches of 100 students
4. **Check for duplicates** before importing
5. **Use transactions** for data consistency

## 🔄 Retry Failed Students

If some students fail, you can retry just those:

```python
# Extract failed students
failed_students = []
for error in result.get('errors', []):
    failed_students.append(error['data'])

# Retry with corrected data
retry_data = {'students': failed_students}
retry_response = requests.post(url, json=retry_data, headers=headers)
```

## 📊 Response Fields Explained

| Field | Description |
|-------|-------------|
| `success` | Number of students successfully created |
| `failed` | Number of students that failed validation |
| `created_students` | Array of successfully created students with their IDs |
| `errors` | Array of validation errors for failed students |
| `index` | Position of student in original array (0-based) |

## 🎯 Use Cases

### 1. New Academic Year Import
Import entire batch of new students at once

### 2. Transfer Students
Add multiple transfer students from another institution

### 3. Data Migration
Migrate existing student data from old system

### 4. Batch Registration
Register multiple students from admission list

## 🆘 Troubleshooting

### Issue: All students failing

**Check:**
1. Are college, course, and branch IDs valid?
2. Are you using CollegeCourse and CollegeBranch IDs (not direct IDs)?
3. Is authentication token valid?
4. Are all required fields present?

### Issue: Some students created, some failed

**This is normal!** The endpoint processes all students and reports which ones succeeded/failed. Fix the failed ones and retry.

### Issue: Slow performance

**Solutions:**
1. Reduce batch size (try 50 students per request)
2. Ensure database indexes are created
3. Check server resources

## 📚 Related Endpoints

- `POST /api/students/students/` - Create single student
- `GET /api/students/students/` - List all students
- `POST /api/students/students/send_bulk_email/` - Send email to multiple students

---

**Create hundreds of students in seconds! 🚀**
