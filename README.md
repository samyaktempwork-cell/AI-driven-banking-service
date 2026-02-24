# AI-Driven Production Banking REST Service

## Overview

This project implements a production-ready banking REST service developed using AI-driven development practices.

The objective of this project is to demonstrate:

- Secure authentication using JWT
- Atomic and transaction-safe money transfers
- SQLite-backed relational persistence
- Structured JSON logging for observability
- Health checks and readiness probes
- Docker containerization with multi-stage builds
- Comprehensive unit and integration testing
- Streamlit-based UI demo client
- Postman collection for full API workflow demonstration
- Transparent AI usage documentation

This repository reflects production-grade backend engineering aligned with modern AI/ML system deployment standards.

---

## Key Features

### Authentication
- User signup and login
- Secure password hashing (bcrypt)
- JWT-based authentication
- Protected endpoints

### Account Management
- Create accounts
- Retrieve accounts
- List user-owned accounts
- Ownership validation

### Transactions and Money Transfers
- Atomic database transactions
- Insufficient funds validation
- Transaction history tracking
- Rollback safety on failure

### Observability
- Structured JSON logging
- Log levels (INFO, ERROR, DEBUG)
- Request-level logging
- Error tracking middleware

### Health Monitoring
- `/health/live`
- `/health/ready`
- Database connectivity check
- Graceful shutdown handling

### Testing
- Unit tests for business logic
- Integration tests for API endpoints
- Coverage-driven validation approach
- Edge case validation (invalid auth, insufficient balance, etc.)

### Containerization
- Multi-stage Dockerfile
- docker-compose for local development
- Environment-based configuration
- Production-ready image build

### Demo and API Testing
- Streamlit UI client demonstrating full workflow
- Postman collection with environment variables
- End-to-end transaction flow validation

---

## Architecture

The system follows a layered architecture:

API Layer → Service Layer → Repository Layer → Database

### Project Structure

```
ai-driven-banking-service/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── routers/
│   └── core/
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── ui/
├── postman/
├── docker/
│
├── .env.example
├── requirements.txt
├── docker-compose.yml
├── AI_USAGE_LOG.md
├── SECURITY.md
├── ROADMAP.md
└── README.md
```

This structure ensures:
- Separation of concerns
- Testability
- Maintainability
- Scalability

---

## Technology Stack

- Python 3.11
- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication
- bcrypt
- pytest
- Docker
- docker-compose
- Streamlit

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/<your-username>/ai-driven-banking-service.git
cd ai-driven-banking-service
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Copy `.env.example`:

```bash
cp .env.example .env
```

Configure environment variables as needed.

### 5. Run Application

```bash
uvicorn app.main:app --reload
```

API documentation available at:

```
http://localhost:8000/docs
```

---

## Running with Docker

### Build and Start

```bash
docker-compose up --build
```

Service will run at:

```
http://localhost:8000
```

---

## Running Tests

```bash
pytest --cov=app
```

Coverage report:

```bash
pytest --cov=app --cov-report=term-missing
```

---

## Postman Collection

The `postman/` directory contains:

- Banking API Collection
- Environment configuration
- Preconfigured authentication flow

Workflow includes:
1. Signup
2. Login
3. Create account
4. Deposit
5. Transfer
6. View transactions
7. Health check

---

## Streamlit UI Demo

Run UI:

```bash
streamlit run ui/app.py
```

The UI demonstrates:
- Login
- Account creation
- Transfer
- Transaction history

---

## Security Considerations

- Passwords are hashed using bcrypt
- JWT secret is environment-based
- No secrets committed to repository
- SQLite database excluded from version control
- Input validation via Pydantic models
- Transaction-level atomicity enforced

See `SECURITY.md` for more details.

---

## AI-Driven Development Approach

This project was built using iterative AI-assisted workflows.

The `AI_USAGE_LOG.md` file documents:

- AI tools used
- Prompt iterations
- Architectural decisions
- Debugging assistance
- Areas requiring manual intervention
- Improvements across development phases

The goal was not just to use AI, but to demonstrate effective AI collaboration in production-grade engineering.

---

## Roadmap

Planned future improvements:

- Fraud detection module
- Daily transfer limits
- Card management enhancements
- Role-based access control
- PostgreSQL production migration
- Kubernetes deployment configuration
- CI/CD pipeline integration
- OpenTelemetry tracing
- Metrics dashboard

See `ROADMAP.md` for extended details.

---

## Development Checkpoints

This project follows a 3-day sprint checkpoint model:

- [ ] Core application structure
- [ ] Authentication system
- [ ] Account management
- [ ] Transaction and transfer logic
- [ ] Test suite implementation
- [ ] Structured logging
- [ ] Health endpoints
- [ ] Dockerization
- [ ] UI demo
- [ ] Postman collection
- [ ] AI usage documentation

---

## Design Philosophy

This implementation prioritizes:

- Production-readiness over feature bloat
- Clean architecture over rapid prototyping
- Test-driven validation
- Observability and operational maturity
- Secure-by-default principles
- AI-assisted but engineer-controlled development

---

## License

MIT License

---

## Author

Developed using structured AI-driven engineering methodology to demonstrate production-grade backend capabilities.