# Python Console E-Commerce Application

A modular, console-based E-Commerce application built with Python and a MySQL database backend. The project is designed using a clean, layered architecture separating controllers, services, repositories, and domain models.

## Project Architecture

```text
project/
│
├── README.md               # Project documentation
├── requirements.txt        # Package dependencies
├── schema.sql              # MySQL DDL script
│
├── src/
│   ├── app.py              # Application entry point
│   ├── models.py           # Database-free Domain Models (Product, Cart, User, etc.)
│   │
│   ├── controller/         # User Inputs & Console Menus (Basic validation)
│   │   ├── __init__.py
│   │   ├── customer_controller.py
│   │   ├── product_controller.py
│   │   ├── cart_controller.py
│   │   ├── order_controller.py
│   │   └── auth_controller.py
│   │
│   ├── service/            # Core Business Logic & Validations
│   │   ├── __init__.py
│   │   ├── customer_service.py
│   │   ├── product_service.py
│   │   ├── cart_service.py
│   │   ├── order_service.py
│   │   └── auth_service.py
│   │
│   ├── repo/               # SQL Queries & Connection Helpers (DAO Layer)
│   │   ├── __init__.py
│   │   ├── customer_repository.py
│   │   ├── product_repository.py
│   │   ├── cart_repository.py
│   │   ├── order_repository.py
│   │   └── database.py
│   │
│   └── utils/              # Utilities (Logging, backups, inputs)
│       ├── __init__.py
│       ├── logger.py
│       ├── backup.py
│       └── inputs.py
│
└── tests/                  # Unit Test Suite
    ├── __init__.py
    ├── test_auth.py
    ├── test_cart.py
    └── test_order.py
```

---

## Configuration

By default, the application connects to a MySQL database with the following details:
- **Host**: `localhost`
- **Port**: `3306`
- **User**: `root`
- **Password**: `1234`
- **Database**: `ecommerce_db` (Created automatically if it does not exist)

To customize credentials, set the following environment variables:
```powershell
$env:DB_HOST="your-host"
$env:DB_USER="your-username"
$env:DB_PASSWORD="your-password"
$env:DB_PORT="3306"
```

---

## Running the Application

Ensure your virtual environment is active and run `src/app.py`:

```powershell
.\myvenv\Scripts\activate
python src/app.py
```

---

## Running Unit Tests

Run the test suite using `pytest` inside the virtual environment:

```powershell
python -m pytest
```
