# College ERP API Samples

This document provides sample API requests and responses for the College ERP system.

## Authentication

### Login

*   **Request:**
    ```http
    POST /api/auth/login/
    Content-Type: application/json

    {
        "username": "admin",
        "password": "password"
    }
    ```

*   **Response:**
    ```json
    {
        "refresh": "...",
        "access": "..."
    }
    ```

## Students

### List Students

*   **Request:** `GET /api/students/`
*   **Response:**
    ```json
    [
        {
            "id": 1,
            "user": 1,
            "name": "John Doe",
            "roll_no": "CS101",
            "department": 1,
            "semester": 1,
            "guardian_info": "Jane Doe",
            "documents": null
        }
    ]
    ```

## Faculty

### List Faculty

*   **Request:** `GET /api/faculty/`
*   **Response:**
    ```json
    [
        {
            "id": 1,
            "user": 2,
            "name": "Dr. Smith",
            "department": 1,
            "designation": "Professor",
            "subjects": [1]
        }
    ]
    ```

## Finance

### Create a Fee Payment

*   **Request:**
    ```http
    POST /api/finance/fee-payments/
    Content-Type: application/json

    {
        "student": 1,
        "fee_structure": 1,
        "amount_paid": "1000.00",
        "payment_date": "2025-11-05"
    }
    ```

*   **Response:**
    ```json
    {
        "id": 1,
        "student": 1,
        "fee_structure": 1,
        "amount_paid": "1000.00",
        "payment_date": "2025-11-05",
        "status": "pending"
    }
    ```

## Admissions

### Create an Application

*   **Request:**
    ```http
    POST /api/admissions/applications/
    Content-Type: application/json

    {
        "first_name": "New",
        "last_name": "Applicant",
        "email": "new@example.com",
        "phone_number": "0987654321",
        "date_of_birth": "2001-01-01",
        "address": "456 New Ave",
        "previous_education": "New School"
    }
    ```

*   **Response:**
    ```json
    {
        "id": 1,
        "first_name": "New",
        "last_name": "Applicant",
        "email": "new@example.com",
        "phone_number": "0987654321",
        "date_of_birth": "2001-01-01",
        "address": "456 New Ave",
        "previous_education": "New School",
        "status": "pending",
        "application_date": "2025-11-05T12:00:00Z"
    }
    ```

## Attendance

### Create an Attendance Record

*   **Request:**
    ```http
    POST /api/attendance/attendance/
    Content-Type: application/json

    {
        "student": 1,
        "subject": 1,
        "date": "2025-11-05",
        "status": "present"
    }
    ```

*   **Response:**
    ```json
    {
        "id": 1,
        "student": 1,
        "subject": 1,
        "date": "2025-11-05",
        "status": "present"
    }
    ```

## Examination

### Get Exam Results

*   **Request:** `GET /api/examination/results/`
*   **Response:**
    ```json
    [
        {
            "id": 1,
            "exam": 1,
            "student": 1,
            "total_marks": 85,
            "percentage": 85.0,
            "grade": "A"
        }
    ]
    ```

## Timetable

### Get Timetables

*   **Request:** `GET /api/timetable/timetables/`
*   **Response:**
    ```json
    [
        {
            "id": 1,
            "department": 1,
            "semester": 1,
            "subject": 1,
            "faculty": 1,
            "classroom": 1,
            "timeslot": 1
        }
    ]
    ```

## Hostel

### Get Hostel Allocations

*   **Request:** `GET /api/hostel/allocations/`
*   **Response:**
    ```json
    [
        {
            "id": 1,
            "room": 1,
            "student": 1,
            "date_allocated": "2025-11-05T12:00:00Z"
        }
    ]
    ```

## Library

### Create a Book Issue

*   **Request:**
    ```http
    POST /api/library/book-issues/
    Content-Type: application/json

    {
        "book": 1,
        "student": 1,
        "issue_date": "2025-11-05",
        "due_date": "2025-11-20"
    }
    ```

*   **Response:**
    ```json
    {
        "id": 1,
        "book": 1,
        "student": 1,
        "issue_date": "2025-11-05",
        "due_date": "2025-11-20",
        "return_date": null
    }
    ```

## Transport

### Get Transport Allocations

*   **Request:** `GET /api/transport/allocations/`
*   **Response:**
    ```json
    [
        {
            "id": 1,
            "student": 1,
            "route": 1
        }
    ]
    ```

## Payroll

### Get Payslips

*   **Request:** `GET /api/payroll/payslips/`
*   **Response:**
    ```json
    [
        {
            "id": 1,
            "faculty": 1,
            "month": 11,
            "year": 2025,
            "gross_salary": "60000.00",
            "total_deductions": "5000.00",
            "net_salary": "55000.00"
        }
    ]
    ```

## Placements

### Create a Job Application

*   **Request:**
    ```http
    POST /api/placements/applications/
    Content-Type: multipart/form-data; boundary=boundary

    --boundary
    Content-Disposition: form-data; name="job"

    1
    --boundary
    Content-Disposition: form-data; name="resume"; filename="resume.pdf"
    Content-Type: application/pdf

    <file content>
    --boundary--
    ```

*   **Response:**
    ```json
    {
        "id": 1,
        "job": 1,
        "student": 1,
        "resume": "http://localhost:8000/resumes/resume.pdf"
    }
    ```

## Notifications

### Get Notifications

*   **Request:** `GET /api/notifications/`
*   **Response:**
    ```json
    [
        {
            "id": 1,
            "recipient": 1,
            "message": "Test notification",
            "is_read": false,
            "timestamp": "2025-11-05T12:00:00Z"
        }
    ]
    ```
