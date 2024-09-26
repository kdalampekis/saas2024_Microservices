# Authentication Service

## Description

The Authentication Service is responsible for managing all user authentication processes within the application. This includes user login, session management, and third-party authentication integrations such as Google OAuth.

## Features

- **User Authentication**: Manages the authentication process for both traditional and social media logins.
- **Session Management**: Ensures secure management of user sessions across the application.
- **OAuth Integration**: Supports OAuth for seamless integration with services like Google for user authentication.

## Technology Stack

- **Django & Django REST Framework**: For creating RESTful APIs.
- **PostgreSQL**: Database for storing user credentials and session information.
- **Redis**: Used for storing session states for scalability and performance.
- **Docker**: Containerization of the service for easy deployment.

## Getting Started

### Prerequisites

- Python 3.8+
- Docker
- Redis server

### Installation

Clone the repository and set up the local development environment:

```bash
git clone https://example.com/authentication-service.git
cd authentication-service
pip install -r requirements.txt
docker build -t authentication-service .
docker run -p 8004:8004 authentication-service

