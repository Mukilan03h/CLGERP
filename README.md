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

### Future Roadmap

*   **Library Management:** Book issuance, returns, and catalog management.
*   **Transport Management:** Bus routes, student transport records, and fee management.
*   **Placement & Internship Cell:** Company listings, student applications, and placement tracking.
*   **Inventory & Assets Management:** College asset tracking and inventory management.
*   **Notifications System:** Email, SMS, and in-app notifications.
*   **Document Verification & Certificates:** Generation of bonafide certificates, transfer certificates, and marksheets.
*   **Accounting Ledger & Reports:** Financial accounting, ledger management, and report generation.
*   **Audit Trail & Activity Logs:** Logging user activities for security and auditing purposes.

## 4. JWT Refresh Flow + RBAC Middleware Explanation

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

### Examination

*   `GET, POST /api/examination/exams/`
*   `GET, PUT, PATCH, DELETE /api/examination/exams/{id}/`
*   `GET, POST /api/examination/marks/`
*   `GET, PUT, PATCH, DELETE /api/examination/marks/{id}/`
*   `GET, POST /api/examination/results/`
*   `GET, PUT, PATCH, DELETE /api/examination/results/{id}/`

### Timetable

*   `GET, POST /api/timetable/classrooms/`
*   `GET, PUT, PATCH, DELETE /api/timetable/classrooms/{id}/`
*   `GET, POST /api/timetable/timeslots/`
*   `GET, PUT, PATCH, DELETE /api/timetable/timeslots/{id}/`
*   `GET, POST /api/timetable/timetables/`
*   `GET, PUT, PATCH, DELETE /api/timetable/timetables/{id}/`

### Hostel

*   `GET, POST /api/hostel/hostels/`
*   `GET, PUT, PATCH, DELETE /api/hostel/hostels/{id}/`
*   `GET, POST /api/hostel/rooms/`
*   `GET, PUT, PATCH, DELETE /api/hostel/rooms/{id}/`
*   `GET, POST /api/hostel/allocations/`
*   `GET, PUT, PATCH, DELETE /api/hostel/allocations/{id}/`

### Payroll

*   `GET, POST /api/payroll/salaries/`
*   `GET, PUT, PATCH, DELETE /api/payroll/salaries/{id}/`
*   `GET, POST /api/payroll/payslips/`
*   `GET, PUT, PATCH, DELETE /api/payroll/payslips/{id}/`
*   `GET, POST /api/payroll/payslip-entries/`
*   `GET, PUT, PATCH, DELETE /api/payroll/payslip-entries/{id}/`

### Placements

*   `GET, POST /api/placements/companies/`
*   `GET, PUT, PATCH, DELETE /api/placements/companies/{id}/`
*   `GET, POST /api/placements/jobs/`
*   `GET, PUT, PATCH, DELETE /api/placements/jobs/{id}/`
*   `GET, POST /api/placements/applications/`
*   `GET, PUT, PATCH, DELETE /api/placements/applications/{id}/`

### Notifications

*   `GET /api/notifications/`
*   `GET /api/notifications/{id}/`
*   `POST /api/notifications/{id}/mark_as_read/`
*   `POST /api/notifications/mark_all_as_read/`

### Documents & Certificates

*   `GET, POST /api/documents/user-documents/`
*   `GET, PUT, PATCH, DELETE /api/documents/user-documents/{id}/`
*   `POST /api/documents/user-documents/{id}/verify/`
*   `POST /api/documents/user-documents/{id}/reject/`
*   `GET, POST /api/documents/certificates/`
*   `GET, PUT, PATCH, DELETE /api/documents/certificates/{id}/`

---

This README provides a comprehensive overview of the College ERP backend project. For more details, please refer to the API documentation and the source code.
