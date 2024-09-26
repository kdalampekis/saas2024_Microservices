# User Management Service

## Description

This microservice handles all aspects of user data, including registration, authentication, and user profile management. It integrates authentication mechanisms and provides endpoints for user operations.

## Features

- **User Registration**: Allows new users to register to the platform.
- **User Authentication**: Handles user login and token generation.
- **User Profile Management**: Supports updating user profiles and password changes.

## Technology Stack

- Django REST Framework for the API layer
- PostgreSQL for database storage
- Docker for containerization
- Uses Django's built-in authentication mechanisms

## Getting Started

### Prerequisites

- Docker
- Python 3.8+
- PostgreSQL running on the default port

### Installation

```bash
git clone https://example.com/user-management.git
cd user-management
pip install -r requirements.txt
docker build -t user-management-service .
docker run -p 8000:8000 user-management-service
```

### API Endpoints
POST /users/: Register a new user
POST /login/: Authenticate a user and return a token
GET /users/{id}/: Fetch a user's profile
