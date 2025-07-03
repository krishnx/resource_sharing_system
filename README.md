# Resource Sharing System

## Overview

This project is a basic **Resource Sharing System** built with Django and Django REST Framework that supports sharing resources with:

- Individual users
- Groups of users
- Everyone in the system (global sharing)

The system supports efficient access checks, sharing management, and reporting endpoints.

---

## Features

- Users and Groups with many-to-many membership
- Resources with flexible sharing options:
  - Shared with specific users
  - Shared with specific groups
  - Shared globally (everyone)
- API endpoints to:
  - List users who have access to a resource
  - List resources accessible by a user
  - Reporting endpoints for user and resource counts
- Business logic separated into service modules
- Unit tests covering core functionality
- Code style enforced with flake8

---

## Setup

1. **Clone the repository:**

```bash
git clone https://github.com/krishnx/resource_sharing_system.git
cd resource_sharing_system
```

2. **Create and activate a virtual environment::**

```bash
python -m venv env
source env/bin/activate
```

3. **Install dependencies:**

```bash
make install
```

4. **Run migrations:**

```bash
make migrate
```

5. **Create a superuser (optional):**

```bash
python manage.py createsuperuser
```

6. **Run the development server:**

```bash
make runserver
```

7. Running Tests

```bash
make test
```

8. **Check code style:**

```bash
make lint
```

## API Documentation
| Method | Endpoint                     | Description                                |
| ------ | ---------------------------- | ------------------------------------------ |
| GET    | `/resource/<id>/access-list` | List all users who have access to resource |
| GET    | `/user/<id>/resources`       | List all resources accessible by a user    |
| GET    | `/resources/with-user-count` | List all resources with user counts        |
| GET    | `/users/with-resource-count` | List all users with resource counts        |


## CURL commands
1. **List users with access to a resource:**

```bash

curl -X 'GET' \
  'http://localhost:8000/api/resource/1/access-list' \
  -H 'accept: application/json' \
  -H 'X-CSRFTOKEN: PLTW5PiqVs2xjE3OEOip754HnXCOVgGmu96rdu00e2r60ZE34c53ulMW1YHyuGXv'
```


2. **List resources accessible by a user:**

```bash
curl -X 'GET' \
  'http://localhost:8000/api/user/3/resources' \
  -H 'accept: application/json' \
  -H 'X-CSRFTOKEN: PLTW5PiqVs2xjE3OEOip754HnXCOVgGmu96rdu00e2r60ZE34c53ulMW1YHyuGXv'
```

3. **List resources with user counts:**

```bash
curl -X 'GET' \
  'http://localhost:8000/api/resources/with-user-count' \
  -H 'accept: application/json' \
  -H 'X-CSRFTOKEN: PLTW5PiqVs2xjE3OEOip754HnXCOVgGmu96rdu00e2r60ZE34c53ulMW1YHyuGXv'
```

4. **List users with resource counts:**

```bash
curl -X 'GET' \
  'http://localhost:8000/api/users/with-resource-count' \
  -H 'accept: application/json' \
  -H 'X-CSRFTOKEN: PLTW5PiqVs2xjE3OEOip754HnXCOVgGmu96rdu00e2r60ZE34c53ulMW1YHyuGXv'
```