# Custom Auth & RBAC System (Django)

**Test Assignment Implementation:** The full task description can be found [here (pastebin)](https://pastebin.com/LjS4MZyk).

## Tech Stack
* **Language:** Python 3.12
* **Framework:** Django 6.0
* **Database:** PostgreSQL
* **Authentication:** PyJWT (Custom JWT tokens)
* **Frontend:** Django Templates + Bootstrap 5
* **Package Manager:** uv
* **Extra:** dj-database-url, python-dotenv, ruff


## System Logic

### 1. Authentication (JWT in Cookies)
This project uses custom JWT tokens instead of standard Django sessions.
* When a user logs in (using **Email** and Password), the system generates `access` and `refresh` tokens.
* These tokens are stored in the user's browser **Cookies**.
* A custom `JWTAuthenticationMiddleware` checks every request. It reads the token from the cookie, decodes it, and identifies the user.
* If a user deletes their account, the profile is "soft-deleted" (`is_active = False`) and the cookies are immediately revoked.

### 2. Authorization (Role-Based Access Control)

Access to specific views is managed by a custom `@check_permission` decorator based on four main database models:
* **User:** The custom user model.
* **Role:** e.g., `admin`, `course author`, `mentor`, `student`, `guest`. Every user has one role. Default is `guest`.
* **Resource:** The business object (mocks/dicts) (e.g., `course`, `lesson`, `solution`).
* **Permission:**  table that links a Role to a Resource with boolean flags (`can_read`, `can_create`, `can_update`, `can_delete`).

## Installation & Setup

This project uses `uv` for fast package management. It also includes a `Makefile` to make commands easier.

**1. Clone the repository and install dependencies:**
```bash
make build
```

**2. Apply migrations and load base data:**
```bash
make migrations
uv run manage.py loaddata permissions.json
```

*(Note: `permissions.json` contains pre-configured roles, resources, and rules required for the system demonstration).*

**3. Run the development server:**
```bash
make local-start
```
The application will be available at http://127.0.0.1:8000/ or http://localhost:8000/