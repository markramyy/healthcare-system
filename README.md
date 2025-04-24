# Healthcare Management System

A comprehensive healthcare management system built with Django, Docker, and Kubernetes.

## Features

- Patient Management
- Electronic Health Records (EHR)
- Appointment Scheduling
- Billing Management
- Monitoring and Logging (Prometheus & Grafana)
- Multi-environment Support (Development & Production)
- Kubernetes-based Deployment
- High Availability & Scalability

## Prerequisites

- Docker and Docker Compose
- Kubernetes cluster (minikube, kind, or cloud provider)
- kubectl and kustomize
- Python 3.11+
- PostgreSQL 15+
- Redis 7+

## Project Structure

```
.
├── config/                 # Django project configuration
├── healthcare_ms/         # Main application code
├── k8s/                   # Kubernetes configurations
│   ├── base/             # Base Kubernetes manifests
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── database.yaml
│   │   └── redis.yaml
│   └── overlays/         # Environment-specific configurations
│       ├── dev/          # Development environment
│       └── prod/         # Production environment
├── monitoring/           # Monitoring configurations
│   ├── prometheus/      # Prometheus configuration
│   └── grafana/         # Grafana dashboards
├── requirements/         # Python dependencies
├── Dockerfile           # Docker configuration
├── docker-compose.dev.yml  # Development environment
└── docker-compose.prod.yml # Production environment
```

## Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd healthcare-system
```

2. Create and activate a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements/base.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

## Docker Development

1. Build and start the development environment:
```bash
docker-compose -f docker-compose.dev.yml up --build
```

2. Access the application at http://localhost:8000

## Kubernetes Deployment

### Prerequisites

1. Ensure you have a Kubernetes cluster running
2. Install kubectl and kustomize
3. Configure kubectl to point to your cluster

### Development Environment

1. Build and push the Docker image:
```bash
docker build -t your-registry/healthcare-system:latest .
docker push your-registry/healthcare-system:latest
```

2. Deploy to development environment:
```bash
kubectl apply -k k8s/overlays/dev
```

3. Access the application:
   - Web: http://localhost:30080
   - Grafana: http://localhost:3000 (admin/admin)
   - Prometheus: http://localhost:9090

### Production Environment

1. Set required environment variables:
```bash
export POSTGRES_PASSWORD=your-secure-password
export SECRET_KEY=your-secure-secret-key
```

2. Deploy to production environment:
```bash
kubectl apply -k k8s/overlays/prod
```

3. Access the application:
   - Web: Through LoadBalancer IP/URL
   - Grafana: http://localhost:3000 (admin/admin)
   - Prometheus: http://localhost:9090

### Environment Differences

#### Development
- Single replica
- NodePort service type
- Debug mode enabled
- Lower resource limits
- Development-specific secrets

#### Production
- Multiple replicas (3)
- LoadBalancer service type
- Debug mode disabled
- Higher resource limits
- Production-specific secrets
- More aggressive health checks

## Monitoring

The system includes comprehensive monitoring with Prometheus and Grafana:

- Prometheus: http://localhost:9090
  - Collects metrics from all services
  - Stores time-series data
  - Provides alerting capabilities

- Grafana: http://localhost:3000 (admin/admin)
  - Visualizes metrics
  - Custom dashboards
  - Alert notifications

## Testing

1. Run unit tests:
```bash
python manage.py test
```

2. Run integration tests:
```bash
python manage.py test healthcare_ms.tests.integration
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.