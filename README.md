<h1 align="center">IT Inventory</h1>

<h3 align="center">A modern CMDB application for hardware device management in small organizations</h3>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#prerequisites">Prerequisites</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#tech-stack">Tech Stack</a>
</p>

<br>

## Overview

IT Inventory is a Configuration Management Database (CMDB) application designed to replace Excel-based inventory management systems. It provides a comprehensive solution for managing hardware devices across multiple businesses within an organization.

### Key Features

- **Multi-tenant Business Management**: Each user can create and manage their own businesses
- **Role-based Access Control**: Business owners have full CRUD access, others have read-only access
- **Device Inventory Management**: Track hardware devices with detailed information
- **Supplier Management**: Shared supplier database accessible to all users
- **Organization Structure**: Hierarchical organization with business units
- **Automated Reports**: Generate inventory reports and analytics
- **File Upload Support**: Import device data via Excel files
- **Real-time Notifications**: Celery-based background task processing

### User Roles & Permissions

- **Superuser**: First registered user who creates the organization
- **Staff Users**: Can manage only their own businesses and devices
- **Shared Access**: Supplier section is editable by all users

## Tech-Stack:

- ![Django](https://img.shields.io/badge/Django-4.2+-092E20?style=for-the-badge&logo=django)
- ![Python](https://img.shields.io/badge/Python-3.11+-3670A0?style=for-the-badge&logo=python)
- ![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite)
- ![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis)
- ![JavaScript](https://img.shields.io/badge/JavaScript-ECDB6F?style=for-the-badge&logo=javascript)
- ![Bootstrap](https://img.shields.io/badge/Bootstrap-850EF6?style=for-the-badge&logo=bootstrap)
- ![HTML5](https://img.shields.io/badge/HTML5-F17545?style=for-the-badge&logo=html5)
- ![CSS3](https://img.shields.io/badge/CSS3-2964F2?style=for-the-badge&logo=css3)

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+**
- **Docker & Docker Compose** (for Redis)
- **Git**
- **Virtual Environment** (recommended)

## Installation

### Windows

1. **Clone the repository**

   ```powershell
   git clone https://github.com/tonytech83/Inventory.git
   cd Inventory
   ```

2. **Create and activate virtual environment**

   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**

   ```powershell
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:

   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///db.sqlite3
   REDIS_URL=redis://localhost:6379/0
   ```

5. **Run database migrations**

   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```powershell
   python manage.py createsuperuser
   ```

### Linux (Debian/Ubuntu)

1. **Install system dependencies**

   ```bash
   sudo apt update
   sudo apt install -y git python3-pip python3.11-venv build-essential \
     python3-dev libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev \
     libopenjp2-7-dev libtiff5-dev libwebp-dev tcl8.6-dev tk8.6-dev
   ```

2. **Clone the repository**

   ```bash
   git clone https://github.com/tonytech83/Inventory.git
   cd Inventory
   ```

3. **Create and activate virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   Create a `.env` file in the project root:

   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///db.sqlite3
   REDIS_URL=redis://localhost:6379/0
   ```

6. **Run database migrations**

   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

7. **Create superuser (optional)**
   ```bash
   python3 manage.py createsuperuser
   ```

## Running the Application

### Start Required Services

1. **Start Redis and Redis-Insight**
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```

### Windows

2. **Start the Django development server**

   ```powershell
   python manage.py runserver
   ```

3. **Start Celery worker (in a new terminal)**

   ```powershell
   celery -A inventory worker --loglevel=info --concurrency=2 -P solo
   ```

4. **Start Celery beat scheduler (in another terminal)**
   ```powershell
   celery -A inventory beat --loglevel=info
   ```

### Linux

2. **Start the Django development server**

   ```bash
   python3 manage.py runserver &
   ```

3. **Start Celery worker (in a new terminal)**

   ```bash
   celery -A inventory worker --loglevel=info --concurrency=2 -P solo &
   ```

4. **Start Celery beat scheduler (in another terminal)**
   ```bash
   celery -A inventory beat --loglevel=info &
   ```

### Access the Application

- **Main Application**: http://localhost:8000
- **Admin Interface**: http://localhost:8000/admin
- **Redis Insight**: http://localhost:8001

## Usage

1. **First Time Setup**: The first user to register becomes a superuser
2. **Create Organization**: Set up your organization structure
3. **Add Businesses**: Create business units within your organization
4. **Manage Devices**: Add and track hardware devices
5. **Manage Suppliers**: Add supplier information (shared across all users)

## Project Structure

```
inventory/
├── accounts/          # User authentication and profiles
├── business/          # Business management
├── devices/           # Device inventory management
├── organization/      # Organization structure
├── reports/           # Reporting and analytics
├── suppliers/         # Supplier management
├── common/            # Shared utilities and views
├── core/              # Core mixins and validators
├── templates/         # HTML templates
├── staticfiles/       # CSS, JS, and static assets
└── mediafiles/        # User uploaded files
```

## 🔧 Configuration

### Environment Variables

| Variable       | Description                | Default                    |
| -------------- | -------------------------- | -------------------------- |
| `DEBUG`        | Enable debug mode          | `True`                     |
| `SECRET_KEY`   | Django secret key          | Required                   |
| `DATABASE_URL` | Database connection string | `sqlite:///db.sqlite3`     |
| `REDIS_URL`    | Redis connection string    | `redis://localhost:6379/0` |

### Database

The application uses SQLite by default for development. For production, consider using PostgreSQL:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/inventory
```

## Documentation

For detailed project documentation, see the [full description](./description/description.md).

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Anton Petrov**

- GitHub: [@tonytech83](https://github.com/tonytech83)

---

<h6 align="center">Made by Anton Petrov</h6>
