# College ERP Backend

This is the backend for the College ERP system, built with Django, Django REST Framework, and MongoDB.

## Features

*   **Authentication:** JWT-based authentication with roles (Admin, Faculty, Student, Accountant, AdmissionOfficer).
*   **Student Information:** Manage student records, including personal details, academic information, and documents.
*   **Faculty Management:** Manage faculty records, including personal details, subjects, and leave requests.
*   **Finance Management:** Manage fee structures and payment records.
*   **Admission Management:** Manage admission applications and merit lists.
*   **Attendance Management:** Manage attendance records and subjects.
*   **Course & Curriculum Management:** Manage programs, courses, and syllabi.
*   **API Documentation:** Swagger UI for API documentation.
*   **Containerization:** Docker and Docker Compose for easy deployment.

## Project Architecture

The backend is built using a modular architecture, with each core feature separated into its own Django app. This promotes separation of concerns and makes the codebase easier to maintain and scale.

The project uses a standardized API response middleware to ensure that all API responses follow a consistent JSON format.

## Data Models

### Authentication

*   **User:** Stores user information, including username, password, email, and role.

### Student Information

*   **Department:** Stores department information, including name and code.
*   **Student:** Stores student information, including name, roll number, department, semester, guardian information, and documents.

### Faculty Management

*   **Faculty:** Stores faculty information, including name, department, designation, and subjects.
*   **LeaveRequest:** Stores leave request information, including faculty, start date, end date, reason, and status.

### Finance Management

*   **FeeStructure:** Stores fee structure information, including department, semester, and amount.
*   **PaymentRecord:** Stores payment record information, including student, date, mode, amount, and status.

### Admission Management

*   **ApplicationForm:** Stores admission application information, including student information, score, status, and documents.
*   **MeritList:** Stores merit list information, including department, rank, and student reference.

### Attendance Management

*   **Subject:** Stores subject information, including name, code, and semester.
*   **Attendance:** Stores attendance information, including date, subject, student, and status.

### Course & Curriculum Management

*   **Program:** Stores program information, including name, code, and duration.
*   **Course:** Stores course information, including name, code, program, credits, and semester.
*   **Syllabus:** Stores syllabus information, including course and content.

## User Roles & Permissions

The backend uses a role-based access control system to restrict access to certain API endpoints based on the user's role. The available roles are:

*   **Admin:** Full access to all API endpoints.
*   **Faculty:** Limited to their subjects and related data.
*   **Student:** Limited to their own data.
*   **Accountant:** Limited to finance-related data.
*   **AdmissionOfficer:** Limited to admission-related data.

## Getting Started

### Prerequisites

*   Docker
*   Docker Compose

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/college-erp-backend.git
    ```
2.  Create a `.env` file in the root directory and add the following environment variables:
    ```
    MONGO_URI=mongodb+srv://<user>:<password>@<cluster-address>/<database-name>
    SECRET_KEY=your-secret-key
    DEBUG=True
    ```
3.  Build and run the Docker containers:
    ```bash
    docker-compose up --build
    ```
4.  The application will be available at `http://localhost:8000`.

## API Documentation

The API documentation is available at `http://localhost:8000/api/docs/`.

## API Endpoints

### Authentication

*   `POST /api/auth/register/`: Register a new user.
*   `POST /api/auth/login/`: Log in a user and get a JWT token.
*   `POST /api/auth/token/refresh/`: Refresh a JWT token.
*   `GET /api/auth/me/`: Get the current user's profile.

### Student Information

*   `GET /api/students/`: Get a list of all students.
*   `POST /api/students/`: Create a new student.
*   `GET /api/students/{id}/`: Get a student by their ID.
*   `PATCH /api/students/{id}/`: Update a student by their ID.
*   `DELETE /api/students/{id}/`: Delete a student by their ID.
*   `GET /api/students/roll/{roll_no}/`: Get a student by their roll number.

### Faculty Management

*   `GET /api/faculty/`: Get a list of all faculty.
*   `POST /api/faculty/`: Create a new faculty member.
*   `GET /api/faculty/{id}/`: Get a faculty member by their ID.
*   `PATCH /api/faculty/{id}/`: Update a faculty member by their ID.
*   `DELETE /api/faculty/{id}/`: Delete a faculty member by their ID.
*   `GET /api/faculty/leave-requests/`: Get a list of all leave requests.
*   `POST /api/faculty/leave-requests/`: Create a new leave request.
*   `GET /api/faculty/leave-requests/{id}/`: Get a leave request by its ID.
*   `PATCH /api/faculty/leave-requests/{id}/`: Update a leave request by its ID.
*   `DELETE /api/faculty/leave-requests/{id}/`: Delete a leave request by its ID.

### Finance Management

*   `GET /api/finance/structure/`: Get a list of all fee structures.
*   `POST /api/finance/structure/`: Create a new fee structure.
*   `GET /api/finance/structure/{id}/`: Get a fee structure by its ID.
*   `PATCH /api/finance/structure/{id}/`: Update a fee structure by its ID.
*   `DELETE /api/finance/structure/{id}/`: Delete a fee structure by its ID.
*   `GET /api/finance/payment/`: Get a list of all payment records.
*   `POST /api/finance/payment/`: Create a new payment record.
*   `GET /api/finance/payment/{id}/`: Get a payment record by its ID.
*   `PATCH /api/finance/payment/{id}/`: Update a payment record by its ID.
*   `DELETE /api/finance/payment/{id}/`: Delete a payment record by its ID.
*   `GET /api/finance/student/{student_id}/`: Get a student's fee records.

### Admission Management

*   `GET /api/admissions/apply/`: Get a list of all admission applications.
*   `POST /api/admissions/apply/`: Create a new admission application.
*   `GET /api/admissions/{id}/`: Get an admission application by its ID.
*   `PATCH /api/admissions/{id}/`: Update an admission application by its ID.
*   `DELETE /api/admissions/{id}/`: Delete an admission application by its ID.
*   `GET /api/admissions/status/{id}/`: Get the status of an admission application.
*   `POST /api/admissions/verify/{id}/`: Verify an admission application.
*   `GET /api/admissions/merit-list/`: Get a list of all merit lists.
*   `POST /api/admissions/merit-list/`: Create a new merit list.
*   `GET /api/admissions/merit-list/{id}/`: Get a merit list by its ID.
*   `PATCH /api/admissions/merit-list/{id}/`: Update a merit list by its ID.
*   `DELETE /api/admissions/merit-list/{id}/`: Delete a merit list by its ID.

### Attendance Management

*   `GET /api/attendance/subjects/`: Get a list of all subjects.
*   `POST /api/attendance/subjects/`: Create a new subject.
*   `GET /api/attendance/subjects/{id}/`: Get a subject by its ID.
*   `PATCH /api/attendance/subjects/{id}/`: Update a subject by its ID.
*   `DELETE /api/attendance/subjects/{id}/`: Delete a subject by its ID.
*   `GET /api/attendance/mark/`: Get a list of all attendance records.
*   `POST /api/attendance/mark/`: Create a new attendance record.
*   `GET /api/attendance/{id}/`: Get an attendance record by its ID.
*   `PATCH /api/attendance/{id}/`: Update an attendance record by its ID.
*   `DELETE /api/attendance/{id}/`: Delete an attendance record by its ID.
*   `GET /api/attendance/student/{student_id}/`: Get a student's attendance records.
*   `GET /api/attendance/report/{semester}/`: Get a semester-wise attendance report.

### Course & Curriculum Management

*   `GET /api/academics/programs/`: Get a list of all programs.
*   `POST /api/academics/programs/`: Create a new program.
*   `GET /api/academics/programs/{id}/`: Get a program by its ID.
*   `PATCH /api/academics/programs/{id}/`: Update a program by its ID.
*   `DELETE /api/academics/programs/{id}/`: Delete a program by its ID.
*   `GET /api/academics/courses/`: Get a list of all courses.
*   `POST /api/academics/courses/`: Create a new course.
*   `GET /api/academics/courses/{id}/`: Get a course by its ID.
*   `PATCH /api/academics/courses/{id}/`: Update a course by its ID.
*   `DELETE /api/academics/courses/{id}/`: Delete a course by its ID.
*   `GET /api/academics/syllabi/`: Get a list of all syllabi.
*   `POST /api/academics/syllabi/`: Create a new syllabus.
*   `GET /api/academics/syllabi/{id}/`: Get a syllabus by its ID.
*   `PATCH /api/academics/syllabi/{id}/`: Update a syllabus by its ID.
*   `DELETE /api/academics/syllabi/{id}/`: Delete a syllabus by its ID.

## Running the API Endpoints

You can use a tool like `curl` or Postman to interact with the API endpoints.

### Example: Register a new user

```bash
curl -X POST http://localhost:8000/api/auth/register/ -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpassword", "email": "test@example.com", "first_name": "Test", "last_name": "User", "role": "Student"}'
```

### Example: Log in a user

```bash
curl -X POST http://localhost:8000/api/auth/login/ -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpassword"}'
```

## Running the Tests

To run the tests, run the following command:
```bash
pytest
```
