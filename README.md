# AI-Driven Production Banking REST Service

## Overview

This project implements a production-ready Banking REST API built using AI-assisted development practices and modern backend engineering standards.

The objective of this implementation is to demonstrate:

- Secure JWT-based authentication  
- Transaction-safe deposit, withdrawal, and transfer operations  
- SQLite-backed relational persistence  
- Structured logging for observability  
- Health and readiness endpoints  
- Docker containerization  
- Unit and integration testing  
- Transparent AI usage documentation  

This repository reflects clean architecture principles and production-aligned backend design.

---

## Key Features

### Authentication

- User signup and login  
- Password hashing using bcrypt  
- JWT-based authentication  
- Protected endpoints using dependency injection  

### Account Management

- Create account  
- List user-owned accounts  
- Ownership validation  
- Balance tracking  

### Transactions

- Deposit  
- Withdraw  
- Transfer between accounts  
- Insufficient funds validation  
- Atomic transaction handling  
- Transaction history tracking  

### Statements

- Generate account statements  
- Date-range filtering  
- Debit/Credit aggregation  
- Closing balance calculation  

### Observability

- Structured logging using Python logging  
- Log levels (INFO, WARNING, ERROR)  
- Transaction event logging  
- Failure event logging  

### Health Monitoring

- `/health/live`  
- `/health/ready`  
- Database connectivity validation  

### Testing

- Pytest-based test suite  
- Authentication tests  
- Transaction flow tests  
- Card lifecycle tests  
- Statement generation tests  
- Edge-case validations  

### Containerization

- Dockerized FastAPI service  
- SQLite persistence  
- Environment-based configuration  
- Reproducible build process  

---

## Architecture

The system follows a layered architecture:

**API Layer → Service Layer → Database Layer**

### Project Structure

```
ai-driven-banking-service/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── routers/
│   └── core/
│
├── tests/
│
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── AI_USAGE_LOG.md
├── SECURITY.md
├── ROADMAP.md
└── README.md
```

This structure ensures:

- Separation of concerns  
- Testability  
- Maintainability  
- Clear ownership boundaries  

---

## Technology Stack

- Python 3.11  
- FastAPI  
- SQLAlchemy  
- SQLite  
- JWT (python-jose)  
- bcrypt  
- pytest  
- Docker  

---

## Local Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

**Windows**
```bash
venv\Scripts\activate
```

**Mac/Linux**
```bash
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Application

```bash
uvicorn app.main:app --reload
```

Swagger UI:

```
http://localhost:8000/docs
```

---

## Docker Setup

### Build and Run

```bash
docker compose down -v
docker compose build --no-cache
docker compose up
```

Application will be available at:

```
http://localhost:8000
```

---

## Running Tests

```bash
pytest -v
```

With coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

---

## Security Considerations

- Passwords hashed using bcrypt  
- JWT secret configured via environment variables  
- Input validation via Pydantic models  
- Database access scoped per user  
- Transaction validation enforced  
- No credentials committed to repository  

See `SECURITY.md` for extended security details.

---

## AI-Driven Development Approach

This project was developed using structured AI-assisted engineering.

AI was used for:

- Architecture planning  
- Code scaffolding  
- Debugging assistance  
- Refactoring suggestions  
- Test case generation  
- Documentation drafting  

All architectural decisions and implementations were manually reviewed and validated.

See `AI_USAGE_LOG.md` for detailed breakdown.

---

## Roadmap

Planned future enhancements:

- Fraud detection module  
- Rate limiting  
- Role-based access control  
- PostgreSQL migration  
- OpenTelemetry integration  
- CI/CD pipeline  
- Metrics dashboard  

See `ROADMAP.md` for detailed roadmap planning.

---

## Design Principles

This implementation prioritizes:

- Production-readiness  
- Clean architecture  
- Secure-by-default design  
- Test-driven validation  
- Observability  
- AI-assisted but engineer-controlled development  

---

## License

MIT License