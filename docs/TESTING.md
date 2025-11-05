# Testing Guide

This document provides instructions on how to run the test suite for the College ERP system.

## Running the Tests

To run the full test suite, use the following command:

```bash
python -m pytest
```

This will discover and run all the tests in the project.

## Sample Output

A successful test run will look something like this:

```
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-8.4.2, pluggy-1.6.0
django: version: 5.2.7, settings: college_erp.test_settings (from ini)
rootdir: /app
configfile: pytest.ini
plugins: django-4.11.1
collected 79 items

admissions/tests.py ....
attendance/tests.py ......
auth_app/test_auth.py ..
examination/tests.py ..........
faculty/tests.py .......
finance/tests.py ......
hostel/tests.py .....
library/tests.py .....
notifications/tests.py ....
payroll/tests.py ......
placements/tests.py .....
students/test_students.py ..
students/tests.py ......
timetable/tests.py ......
transport/tests.py .....

=============================== warnings summary ===============================
admissions/tests.py::AdmissionsTests::test_create_admission
  /home/jules/.pyenv/versions/3.12.12/lib/python3.12/site-packages/drf_yasg/views.py:100: DeprecationWarning: SwaggerJSONRenderer & SwaggerYAMLRenderer's `format` has changed to not include a `.` prefix, please silence this warning by setting `SWAGGER_USE_COMPAT_RENDERERS = False` in your Django settings and ensure your application works (check your URLCONF and swagger/redoc URLs).
    warnings.warn(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================== 79 passed, 1 warning in 189.20s (0:03:09) ===================
```
