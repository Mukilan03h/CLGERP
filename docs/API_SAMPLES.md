# API Sample Requests

This document provides sample API requests for the College ERP backend, formatted as `cURL` commands. You can import these commands into tools like Postman.

## Authentication

All API requests require a JSON Web Token (JWT) to be included in the `Authorization` header.

### 1. Obtain a JWT

First, you need to obtain a JWT by sending a `POST` request to the `/api/auth/login/` endpoint with a valid username and password.

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
-H "Content-Type: application/json" \
-d '{
    "username": "admin",
    "password": "password"
}'
```

The response will contain `access` and `refresh` tokens:

```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 2. Making Authenticated Requests

Include the `access` token in the `Authorization` header for all subsequent requests.

```bash
curl -X GET http://localhost:8000/api/some_endpoint/ \
-H "Authorization: Bearer <your_access_token>"
```

---

## Module API Samples

Below are sample requests for various modules.

### Inventory Module

**Endpoint:** `/api/inventory/`

**1. List all inventory items:**

```bash
curl -X GET http://localhost:8000/api/inventory/ \
-H "Authorization: Bearer <your_access_token>"
```

**2. Create a new inventory item:**

```bash
curl -X POST http://localhost:8000/api/inventory/ \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your_access_token>" \
-d '{
    "name": "Laptop",
    "quantity": 50,
    "status": "in_stock"
}'
```

**3. Retrieve a specific inventory item:**

```bash
curl -X GET http://localhost:8000/api/inventory/1/ \
-H "Authorization: Bearer <your_access_token>"
```

### Payroll Module

**Endpoint:** `/api/payroll/`

**1. List all payroll records:**

```bash
curl -X GET http://localhost:8000/api/payroll/ \
-H "Authorization: Bearer <your_access_token>"
```

**2. Create a new payroll record:**

```bash
curl -X POST http://localhost:8000/api/payroll/ \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your_access_token>" \
-d '{
    "employee": 1,
    "amount": 50000.00,
    "pay_date": "2025-11-30"
}'
```

### Placements Module

**Endpoint:** `/api/placements/`

**1. List all placement records:**

```bash
curl -X GET http://localhost:8000/api/placements/ \
-H "Authorization: Bearer <your_access_token>"
```

**2. Create a new placement record:**

```bash
curl -X POST http://localhost:8000/api/placements/ \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your_access_token>" \
-d '{
    "student": 1,
    "company": "Tech Corp",
    "role": "Software Engineer",
    "status": "offered"
}'
```

### Students Module

**Endpoint:** `/api/students/`

**1. List all students:**

```bash
curl -X GET http://localhost:8000/api/students/ \
-H "Authorization: Bearer <your_access_token>"
```

**2. Create a new student:**

```bash
curl -X POST http://localhost:8000/api/students/ \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your_access_token>" \
-d '{
    "name": "John Doe",
    "roll_no": "S12345",
    "department": 1,
    "semester": 3,
    "guardian_info": "Jane Doe, 555-1234"
}'
```

### Faculty Module

**Endpoint:** `/api/faculty/`

**1. List all faculty:**

```bash
curl -X GET http://localhost:8000/api/faculty/ \
-H "Authorization: Bearer <your_access_token>"
```

**2. Create a new faculty member:**

```bash
curl -X POST http://localhost:8000/api/faculty/ \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your_access_token>" \
-d '{
    "name": "Dr. Smith",
    "department": 1,
    "designation": "Professor"
}'
```

### Notifications Module

**Endpoint:** `/api/notifications/`

**1. List all notifications:**

```bash
curl -X GET http://localhost:8000/api/notifications/ \
-H "Authorization: Bearer <your_access_token>"
```

**2. Create a new notification:**

```bash
curl -X POST http://localhost:8000/api/notifications/ \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your_access_token>" \
-d '{
    "user": 1,
    "message": "Your fees are due.",
    "notification_type": "alert"
}'
```

### Documents Module

**Endpoint:** `/api/documents/`

**1. List all documents:**

```bash
curl -X GET http://localhost:8000/api/documents/ \
-H "Authorization: Bearer <your_access_token>"
```

**2. Upload a new document:**
*Note: This is a multipart/form-data request, not JSON.*
```bash
curl -X POST http://localhost:8000/api/documents/ \
-H "Authorization: Bearer <your_access_token>" \
-F "user=1" \
-F "document_type=transcript" \
-F "file=@/path/to/your/file.pdf"
```

### Accounting Module

**Endpoint:** `/api/accounting/`

**1. List all transactions:**

```bash
curl -X GET http://localhost:8000/api/accounting/ \
-H "Authorization: Bearer <your_access_token>"
```

**2. Create a new transaction:**

```bash
curl -X POST http://localhost:8000/api/accounting/ \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your_access_token>" \
-d '{
    "transaction_type": "income",
    "amount": 1000.00,
    "description": "Tuition fee payment"
}'
```

### Audit Module

**Endpoint:** `/api/audit/`

**1. List all audit logs:**

```bash
curl -X GET http://localhost:8000/api/audit/ \
-H "Authorization: Bearer <your_access_token>"
```

### Examination Module

**Endpoint:** `/api/examination/`

**1. List all exams:**

```bash
curl -X GET http://localhost:8000/api/examination/ \
-H "Authorization: Bearer <your_access_token>"
```

**2. Create a new exam:**

```bash
curl -X POST http://localhost:8000/api/examination/ \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your_access_token>" \
-d '{
    "name": "Midterm Exam",
    "date": "2025-12-15"
}'
```

### Timetable Module

**Endpoint:** `/api/timetable/`

**1. List all timetable entries:**

```bash
curl -X GET http://localhost:8000/api/timetable/ \
-H "Authorization: Bearer <your_access_token>"
```

### Hostel Module

**Endpoint:** `/api/hostel/`

**1. List all hostel records:**

```bash
curl -X GET http://localhost:8000/api/hostel/ \
-H "Authorization: Bearer <your_access_token>"
```

### Library Module

**Endpoint:** `/api/library/`

**1. List all library books:**

```bash
curl -X GET http://localhost:8000/api/library/ \
-H "Authorization: Bearer <your_access_token>"
```

### Transport Module

**Endpoint:** `/api/transport/`

**1. List all transport routes:**

```bash
curl -X GET http://localhost:8000/api/transport/ \
-H "Authorization: Bearer <your_access_token>"
```
