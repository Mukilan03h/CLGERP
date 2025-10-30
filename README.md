# College ERP Backend

This is the backend for the College ERP system, built with Django, Django REST Framework, and MongoDB.

## Features

*   **Authentication:** JWT-based authentication with roles (Admin, Faculty, Student, Accountant, AdmissionOfficer).
*   **Student Information:** Manage student records, including personal details, academic information, and documents.
*   **Faculty Management:** Manage faculty records, including personal details, subjects, and leave requests.
*   **Finance Management:** Manage fee structures and payment records.
*   **Admission Management:** Manage admission applications and merit lists.
*   **Attendance Management:** Manage attendance records and subjects.
*   **API Documentation:** Swagger UI for API documentation.
*   **Containerization:** Docker and Docker Compose for easy deployment.

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

### API Documentation

The API documentation is available at `http://localhost:8000/api/docs/`.

### Running the Tests

To run the tests, run the following command:
```bash
pytest
```
