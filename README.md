# WeDelivery

WeDelivery is a modern delivery tracking and management system built with Flask and PostgreSQL. It allows customers to track their packages and businesses to join the delivery network.

## Features

- **Package Tracking**: Real-time package status updates for customers.
- **Business Registration**: Easy lead generation form for new business partners.
- **Admin Dashboard**: Internal dashboard for managing packages and leads.
- **API Integration**: Webhook endpoint for external shop integrations.

## Tech Stack

- **Backend**: Python, Flask, SQLAlchemy
- **Database**: PostgreSQL with `psycopg2`
- **Containerization**: Docker, Docker Compose
- **Orchestration**: Kubernetes / OpenShift
- **Frontend**: HTML, CSS (Bootstrap), Jinja2 templates

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
   - **Admin Dashboard**: [http://localhost:5000/admin/dashboard](http://localhost:5000/admin/dashboard)

## Project Structure

```
wedone/
├── app.py              # Main Flask application entry point
├── models.py           # Database models (Package, Lead)
├── Dockerfile          # instructions for building the app image
├── docker-compose.yml  # Local development orchestration
├── requirements.txt    # Python dependencies
├── k8s/                # Kubernetes/OpenShift deployment manifests
├── static/             # Static assets (CSS, JS, images)
└── templates/          # HTML templates
```

## API Endpoints

- `GET /`: Home page
- `POST /track`: Track a package by ID
- `GET/POST /join-us`: Join form for businesses
- `GET /admin/dashboard`: Admin view
- `POST /api/v1/webhook`: Endpoint for receiving order updates (JSON)
- `GET /api/health`: Health check endpoint

## Deployment (OpenShift / Kubernetes)

The `k8s/` directory contains standard manifests for deployment.

1. **Apply configurations:**
   ```bash
   oc apply -f k8s/
   ```

2. **Verify Pods:**
   ```bash
   oc get pods
   ```
