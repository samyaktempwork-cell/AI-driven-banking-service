# Security Architecture

## Authentication Model
- JWT-based access tokens
- Stateless authentication
- Token expiration

## Password Handling
- bcrypt hashing
- No plaintext storage

## Authorization Controls
- Account ownership validation
- Route-level protection using dependency injection

## Threat Model

### Prevented Threats
- Unauthorized account access
- Balance manipulation
- Overdraft exploitation
- Token forgery (signed JWT)

### Known Constraints
- SQLite is not horizontally scalable
- No rate limiting (future roadmap)

## Secrets Management
- Environment-based configuration
- .env excluded from repository