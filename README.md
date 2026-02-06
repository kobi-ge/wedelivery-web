# WeDelivery

WeDelivery is a modern delivery tracking and management system built with Flask and PostgreSQL. It allows customers to track their packages and businesses to join the delivery network.

## Features

- **User Authentication**: Secure registration and login system with Flask-Login
- **Business Dashboard**: Protected dashboard for authenticated business clients
- **Package Tracking**: Real-time package status updates for customers
- **Business Registration**: Easy lead generation form for new business partners
- **Admin Dashboard**: Internal dashboard for managing packages and leads
- **API Integration**: Webhook endpoint for external shop integrations

## Tech Stack

- **Backend**: Python, Flask, SQLAlchemy, Flask-Login
- **Database**: PostgreSQL with `psycopg2`
- **Authentication**: Werkzeug password hashing, session-based auth
- **Containerization**: Docker, Docker Compose
- **Orchestration**: Kubernetes / OpenShift
- **Frontend**: HTML, Tailwind CSS, Bootstrap 5, Jinja2 templates

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your machine.

### Local Development

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd wedone
   ```

2. **Start the services:**
   ```bash
   docker-compose up --build
   ```
   This command starts both the Flask web application and the PostgreSQL database.

3. **Access the application:**
   - **Main Site**: [http://localhost:5000](http://localhost:5000)
   - **Register**: [http://localhost:5000/register](http://localhost:5000/register)
   - **Login**: [http://localhost:5000/login](http://localhost:5000/login)
   - **Dashboard** (protected): [http://localhost:5000/dashboard](http://localhost:5000/dashboard)
   - **Admin Dashboard**: [http://localhost:5000/admin/dashboard](http://localhost:5000/admin/dashboard)

## Project Structure

```
wedone/
├── app.py              # Main Flask application entry point
├── models.py           # Database models (User, Package, Lead)
├── Dockerfile          # Docker image build instructions
├── docker-compose.yml  # Local development orchestration
├── requirements.txt    # Python dependencies (Flask, Flask-Login, etc.)
├── k8s/                # Kubernetes/OpenShift deployment manifests
├── static/             # Static assets (CSS, JS, images)
└── templates/          # HTML templates
    ├── index.html      # Landing page with package tracking
    ├── login.html      # User login page
    ├── register.html   # User registration page
    ├── dashboard.html  # Protected user dashboard
    ├── join.html       # Business lead form
    └── admin.html      # Admin panel
```

## API Endpoints

### Public Routes
- `GET /`: Home page
- `POST /track`: Track a package by ID
- `GET/POST /register`: User registration
- `GET/POST /login`: User login
- `GET/POST /join-us`: Business lead form

### Protected Routes (Authentication Required)
- `GET /dashboard`: User dashboard
- `GET /logout`: Logout current user
- `GET /admin/dashboard`: Admin view

### API Routes
- `POST /api/v1/webhook`: Webhook for order updates (JSON)
- `GET /api/health`: Health check endpoint

## Deployment (OpenShift / Kubernetes)

The `k8s/` directory contains standard manifests for deployment.

### Build and Push Docker Image

```bash
# Build the image
docker build -t kobigdocker/wedelivery:v2 .

# Push to Docker Hub
docker push kobigdocker/wedelivery:v2
```

### Deploy to OpenShift

1. **Login to OpenShift:**
   ```bash
   oc login --token=<your-token> --server=<your-server>
   ```

2. **Apply configurations:**
   ```bash
   oc apply -f k8s/
   ```

3. **Verify Pods:**
   ```bash
   oc get pods
   oc get route
   ```

### Live Production URL

🌐 **WeDelivery Live**: https://wedone-api-kobiger-redhat-dev.apps.rm2.thpm.p1.openshiftapps.com

**Authentication Endpoints:**
- Register: `/register`
- Login: `/login`
- Dashboard: `/dashboard`
