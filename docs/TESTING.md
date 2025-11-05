# Testing

This document provides instructions for running the test suite and a summary of the latest test run.

## Running the Test Suite

To run the full test suite, use the following command from the root of the project:

```bash
pytest
```

## Test Results

Here is a summary of the latest test run:

```
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-8.4.2, pluggy-1.6.0
django: version: 5.2.7, settings: college_erp.test_settings (from ini)
rootdir: /app
configfile: pytest.ini
plugins: django-4.11.1
collected 32 items

auth_app/tests.py ..                                                     [  6%]
examination/tests.py .......                                             [ 28%]
hostel/tests.py ......                                                   [ 46%]
library/tests.py .....                                                   [ 62%]
students/tests.py ..                                                     [ 68%]
timetable/tests.py .....                                                 [ 84%]
transport/tests.py .....                                                 [100%]

=============================== warnings summary ===============================
auth_app/tests.py::test_user_registration
  /home/jules/.pyenv/versions/3.12.12/lib/python3.12/site-packages/drf_yasg/views.py:100: DeprecationWarning: SwaggerJSONRenderer & SwaggerYAMLRenderer's `format` has changed to not include a `.` prefix, please silence this warning by setting `SWAGGER_USE_COMPAT_RENDERERS = False` in your Django settings and ensure your application works (check your URLCONF and swagger/redoc URLs).
    warnings.warn(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================== 32 passed, 1 warning in 1.39s =========================
```
