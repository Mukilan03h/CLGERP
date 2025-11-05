# College ERP Backend

This is the backend for a comprehensive, production-ready College ERP system built with Django, Django REST Framework, and MongoDB. This project aims to provide a scalable and robust solution for managing all aspects of a college's operations.

## 1. Full Tech Stack Breakdown

*   **Python:** 3.8+
*   **Django:** 5.2.7
*   **Django REST Framework:** 3.14+
*   **Database:** MongoDB
*   **MongoDB Library:** djongo5
*   **Authentication:** djangorestframework-simplejwt (JWT)
*   **API Documentation:** drf-yasg (Swagger UI)
*   **Containerization:** Docker, Docker-Compose
*   **Code Quality:** Black, isort
*   **Testing:** Pytest, pytest-django

## 2. Database Schema Diagram

Below is a simplified text-based ERD of the core modules:

```
+----------------+       +------------------+       +----------------+
|      User      |       |     Student      |       |    Department    |
+----------------+       +------------------+       +----------------+
| id (PK)        |       | id (PK)          |       | id (PK)          |
| username       |       | name             |       | name             |
| password       |       | roll_no          |       | code             |
| role           |------>| department (FK)  |------>|                  |
+----------------+       | semester         |       +----------------+
                         | guardian_info    |
                         | documents        |
                         +------------------+

+----------------+       +------------------+       +----------------+
|     Faculty    |       |  LeaveRequest    |       |     Subject      |
+----------------+       +------------------+       +----------------+
| id (PK)        |       | id (PK)          |       | id (PK)          |
| name           |       | faculty (FK)     |------>| name             |
| department (FK)  |------>| start_date       |       | code             |
| designation    |       | end_date         |       | semester         |
| subjects (M2M) |------>| reason           |       +----------------+
+----------------+       | status           |
                         +------------------+

+----------------+
|   Attendance   |
+----------------+
| id (PK)        |
| date           |
| subject (FK)   |
| student (FK)   |
| status         |
+----------------+

+----------------+       +----------------+       +----------------+
|      Exam      |       |     Marks      |       |     Result     |
+----------------+       +----------------+       +----------------+
| id (PK)        |       | id (PK)        |       | id (PK)        |
| name           |       | exam (FK)      |       | exam (FK)      |
| date           |------>| student (FK)   |------>| student (FK)   |
| subjects (M2M) |       | subject (FK)   |       | total_marks    |
+----------------+       | marks          |       | percentage     |
                         +----------------+       | grade          |
                                                  +----------------+

+----------------+       +----------------+       +----------------+
|   Classroom    |       |    TimeSlot    |       |    Timetable   |
+----------------+       +----------------+       +----------------+
| id (PK)        |       | id (PK)        |       | id (PK)        |
| room_no        |       | day            |       | department (FK)|
| capacity       |       | start_time     |       | semester       |
+----------------+       | end_time       |       | subject (FK)   |
                         +----------------+       | faculty (FK)   |
                                                  | classroom (FK) |
                                                  | timeslot (FK)  |
                                                  +----------------+

+----------------+       +----------------+       +----------------+
|     Hostel     |       |      Room      |       |   Allocation   |
+----------------+       +----------------+       +----------------+
| id (PK)        |       | id (PK)        |       | id (PK)        |
| name           |       | hostel (FK)    |------>| room (FK)      |
| capacity       |------>| room_no        |       | student (FK)   |
+----------------+       | capacity       |       | date_allocated |
                         | is_vacant      |       +----------------+
                         +----------------+
```

## 3. Modules

### Implemented Modules

*   **Examination Management:** Marks, grading, and result generation.
*   **Timetable & Scheduling:** Class scheduling, faculty allocation, and timetable generation.
*   **Hostel Management:** Room allocation, mess management, and hostel attendance.
*   **Library Management:** Book issuance, returns, and catalog management.
*   **Transport Management:** Bus routes, student transport records, and fee management.
*   **Placement & Internship Cell:** Company listings, student applications, and placement tracking.
*   **Inventory & Assets Management:** College asset tracking and inventory management.
*   **Payroll Management:** Salary processing, payslip generation, and benefits administration.
*   **Notifications System:** Email, SMS, and in-app notifications.
*   **Document Verification & Certificates:** Generation of bonafide certificates, transfer certificates, and marksheets.
*   **Accounting Ledger & Reports:** Financial accounting, ledger management, and report generation.
*   **Audit Trail & Activity Logs:** Logging user activities for security and auditing purposes.

### Future Roadmap

All modules on the original roadmap have now been implemented. Future work will focus on expanding the existing feature set and improving the user experience.

## 4. Documentation

Detailed documentation is available in the `docs` directory:

*   **`docs/API_SAMPLES.md`**: Provides detailed examples of API requests and responses for all modules.
*   **`docs/TESTING.md`**: A guide on how to run the test suite.

## 5. JWT Refresh Flow + RBAC Middleware Explanation

### JWT Refresh Flow

The authentication system uses JWT with a refresh token mechanism. When a user logs in, they receive an `access_token` and a `refresh_token`. The `access_token` is short-lived (15 minutes) and is used to authenticate API requests. The `refresh_token` is long-lived (7 days) and is used to obtain a new `access_token` when the old one expires.

### Role-Based Access Control (RBAC)

RBAC is enforced using custom permission classes in Django REST Framework. Each user has a `role` field (e.g., 'Admin', 'Faculty', 'Student'). Custom permission classes check the user's role before allowing access to an endpoint.

**Example Permission Class:**

```python
# auth_app/permissions.py
from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'Admin'
```

This permission class can then be added to any view to restrict access to admins only.

## 5. Production Deployment Guide

### Environment Variables

Create a `.env.prod` file with the following variables:

```
MONGO_URI=mongodb+srv://<user>:<password>@<cluster-address>/<database-name>
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,api.your-domain.com
```

### Gunicorn + Nginx

For production, it is recommended to use Gunicorn as the WSGI server and Nginx as a reverse proxy.

**Gunicorn:**

```bash
gunicorn --workers 3 --bind 0.0.0.0:8000 college_erp.wsgi:application
```

**Nginx:**

Create a new Nginx configuration file in `/etc/nginx/sites-available/college_erp`:

```nginx
server {
    listen 80;
    server_name your-domain.com api.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /path/to/your/project;
    }

    location / {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://unix:/path/to/your/project/gunicorn.sock;
    }
}
```

### MongoDB Atlas IP Whitelist

When using MongoDB Atlas, ensure that you whitelist the IP address of your production server to allow incoming connections.

### CI/CD

A simple CI/CD pipeline can be set up using GitHub Actions to automatically deploy the application on push to the `main` branch.

## 6. Testing Coverage + Folder Structure Sample

The project follows a modular structure, with each app having its own dedicated folder.

```
/apps
    /students
    /faculty
    ...
/core
/config
/tests
    /students
        - test_models.py
        - test_views.py
    /faculty
        - test_models.py
        - test_views.py
```

## 7. Contributing + Coding Standards

### Pull Requests

*   Fork the repository.
*   Create a new branch for your feature or bug fix.
*   Make your changes and write tests.
*   Ensure that all tests pass.
*   Submit a pull request with a detailed description of your changes.

### Naming Conventions

*   Branches: `feature/<feature-name>`, `bugfix/<bug-name>`
*   Commits: Use conventional commit messages (e.g., `feat: add student search functionality`).

## 8. API Response Standard Format

All API responses follow a standardized format:

```json
{
    "success": true,
    "data": {
        "id": 1,
        "name": "John Doe",
        "roll_no": "S12345"
    },
    "message": "Student created successfully."
}
```

In case of an error:

```json
{
    "success": false,
    "errors": {
        "roll_no": [
            "Student with this roll no already exists."
        ]
    },
    "message": "Invalid input."
}
```

## 9. Security

*   **Rate Limiting:** API endpoints are rate-limited to prevent abuse.
*   **CSRF:** While JWT is used for authentication, CSRF protection is still enabled for session-based authentication in the Django admin panel.
*   **CORS:** Cross-Origin Resource Sharing (CORS) is configured to only allow requests from whitelisted domains in production.
*   **Password Hashing:** Passwords are hashed using Django's default password hashing algorithm (PBKDF2).
*   **Sensitive Data:** All sensitive data is stored in environment variables and is not hard-coded in the source code.

## 10. Versioning + Roadmap

The project follows semantic versioning (vX.Y.Z).

### Roadmap (Next 3-6 Months)

*   **v1.1.0:** Implement Examination and Timetable modules.
*   **v1.2.0:** Implement Hostel and Library modules.
*   **v1.3.0:** Implement Transport and Placement modules.

## 11. API Endpoints

A full, interactive API documentation is available through Swagger UI at the `/api/docs/` endpoint. The following is a summary of the available endpoints.

### Authentication
-   `POST /api/auth/login/`: User login.
-   `POST /api/auth/register/`: User registration.
-   `POST /api/auth/token/refresh/`: Refresh JWT token.

### Students
-   `GET, POST /api/students/`: List all students or create a new student.
-   `GET, PUT, PATCH, DELETE /api/students/{id}/`: Retrieve, update or delete a student.

### Faculty
-   `GET, POST /api/faculty/`: List all faculty or create a new faculty member.
-   `GET, PUT, PATCH, DELETE /api/faculty/{id}/`: Retrieve, update or delete a faculty member.
-   `GET, POST /api/faculty/leave-requests/`: List all leave requests or create a new one.
-   `GET, PUT, PATCH, DELETE /api/faculty/leave-requests/{id}/`: Retrieve, update or delete a leave request.

### Finance
-   `GET, POST /api/finance/fee-structures/`: List all fee structures or create a new one.
-   `GET, PUT, PATCH, DELETE /api/finance/fee-structures/{id}/`: Retrieve, update or delete a fee structure.
-   `GET, POST /api/finance/fee-payments/`: List all fee payments or create a new one.
-   `GET, PUT, PATCH, DELETE /api/finance/fee-payments/{id}/`: Retrieve, update or delete a fee payment.
-   `GET, POST /api/finance/expenses/`: List all expenses or create a new one.
-   `GET, PUT, PATCH, DELETE /api/finance/expenses/{id}/`: Retrieve, update or delete an expense.

### Admissions
-   `GET, POST /api/admissions/applications/`: List all applications or create a new one.
-   `GET, PUT, PATCH, DELETE /api/admissions/applications/{id}/`: Retrieve, update or delete an application.
-   `GET, POST /api/admissions/admissions/`: List all admissions or create a new one.
-   `GET, PUT, PATCH, DELETE /api/admissions/admissions/{id}/`: Retrieve, update or delete an admission.

### Attendance
-   `GET, POST /api/attendance/subjects/`: List all subjects or create a new one.
-   `GET, PUT, PATCH, DELETE /api/attendance/subjects/{id}/`: Retrieve, update or delete a subject.
-   `GET, POST /api/attendance/attendance/`: List all attendance records or create a new one.
-   `GET, PUT, PATCH, DELETE /api/attendance/attendance/{id}/`: Retrieve, update or delete an attendance record.

### Examination
-   `GET, POST /api/examination/exams/`: List all exams or create a new one.
-   `GET, PUT, PATCH, DELETE /api/examination/exams/{id}/`: Retrieve, update or delete an exam.
-   `GET, POST /api/examination/marks/`: List all marks or create a new one.
-   `GET, PUT, PATCH, DELETE /api/examination/marks/{id}/`: Retrieve, update or delete a marks record.
-   `GET, POST /api/examination/results/`: List all results or create a new one.
-   `GET, PUT, PATCH, DELETE /api/examination/results/{id}/`: Retrieve, update or delete a result.

### Timetable
-   `GET, POST /api/timetable/classrooms/`: List all classrooms or create a new one.
-   `GET, PUT, PATCH, DELETE /api/timetable/classrooms/{id}/`: Retrieve, update or delete a classroom.
-   `GET, POST /api/timetable/timeslots/`: List all time slots or create a new one.
-   `GET, PUT, PATCH, DELETE /api/timetable/timeslots/{id}/`: Retrieve, update or delete a time slot.
-   `GET, POST /api/timetable/timetables/`: List all timetables or create a new one.
-   `GET, PUT, PATCH, DELETE /api/timetable/timetables/{id}/`: Retrieve, update or delete a timetable.

### Hostel
-   `GET, POST /api/hostel/hostels/`: List all hostels or create a new one.
-   `GET, PUT, PATCH, DELETE /api/hostel/hostels/{id}/`: Retrieve, update or delete a hostel.
-   `GET, POST /api/hostel/rooms/`: List all rooms or create a new one.
-   `GET, PUT, PATCH, DELETE /api/hostel/rooms/{id}/`: Retrieve, update or delete a room.
-   `GET, POST /api/hostel/allocations/`: List all allocations or create a new one.
-   `GET, PUT, PATCH, DELETE /api/hostel/allocations/{id}/`: Retrieve, update or delete an allocation.

### Library
-   `GET, POST /api/library/books/`: List all books or create a new one.
-   `GET, PUT, PATCH, DELETE /api/library/books/{id}/`: Retrieve, update or delete a book.
-   `GET, POST /api/library/book-issues/`: List all book issues or create a new one.
-   `GET, PUT, PATCH, DELETE /api/library/book-issues/{id}/`: Retrieve, update or delete a book issue.
-   `GET, POST /api/library/fines/`: List all fines or create a new one.
-   `GET, PUT, PATCH, DELETE /api/library/fines/{id}/`: Retrieve, update or delete a fine.

### Transport
-   `GET, POST /api/transport/vehicles/`: List all vehicles or create a new one.
-   `GET, PUT, PATCH, DELETE /api/transport/vehicles/{id}/`: Retrieve, update or delete a vehicle.
-   `GET, POST /api/transport/routes/`: List all routes or create a new one.
-   `GET, PUT, PATCH, DELETE /api/transport/routes/{id}/`: Retrieve, update or delete a route.
-   `GET, POST /api/transport/allocations/`: List all transport allocations or create a new one.
-   `GET, PUT, PATCH, DELETE /api/transport/allocations/{id}/`: Retrieve, update or delete a transport allocation.

### Inventory
-   `GET, POST /api/inventory/items/`: List all items or create a new one.
-   `GET, PUT, PATCH, DELETE /api/inventory/items/{id}/`: Retrieve, update or delete an item.
-   `GET, POST /api/inventory/suppliers/`: List all suppliers or create a new one.
-   `GET, PUT, PATCH, DELETE /api/inventory/suppliers/{id}/`: Retrieve, update or delete a supplier.

### Payroll
-   `GET, POST /api/payroll/salaries/`: List all salaries or create a new one.
-   `GET, PUT, PATCH, DELETE /api/payroll/salaries/{id}/`: Retrieve, update or delete a salary.
-   `GET, POST /api/payroll/payslips/`: List all payslips or create a new one.
-   `GET, PUT, PATCH, DELETE /api/payroll/payslips/{id}/`: Retrieve, update or delete a payslip.
-   `GET, POST /api/payroll/payslip-entries/`: List all payslip entries or create a new one.
-   `GET, PUT, PATCH, DELETE /api/payroll/payslip-entries/{id}/`: Retrieve, update or delete a payslip entry.

### Placements
-   `GET, POST /api/placements/companies/`: List all companies or create a new one.
-   `GET, PUT, PATCH, DELETE /api/placements/companies/{id}/`: Retrieve, update or delete a company.
-   `GET, POST /api/placements/jobs/`: List all jobs or create a new one.
-   `GET, PUT, PATCH, DELETE /api/placements/jobs/{id}/`: Retrieve, update or delete a job.
-   `GET, POST /api/placements/applications/`: List all applications or create a new one.
-   `GET, PUT, PATCH, DELETE /api/placements/applications/{id}/`: Retrieve, update or delete an application.

### Notifications
-   `GET /api/notifications/`: List all notifications for the current user.
-   `GET /api/notifications/{id}/`: Retrieve a specific notification.
-   `POST /api/notifications/{id}/mark_as_read/`: Mark a notification as read.
-   `POST /api/notifications/mark_all_as_read/`: Mark all notifications as read.

---

This README provides a comprehensive overview of the College ERP backend project. For more details, please refer to the API documentation and the source code.
