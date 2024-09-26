# Credit Management Service

## Description

The Credit Management Service is responsible for handling all operations related to user credits within the Solve My Problem App. This service tracks credit allocations, deductions for services used, and provides reporting on credit usage.

## Features

- **Credit Allocation**: Manages the initial allocation of credits to new users and adjustments to existing users.
- **Credit Deduction**: Automates the deduction of credits when users submit problems that incur a cost.
- **Credit Reporting**: Offers detailed reports and logs of credit transactions for users and administrators.

## Technology Stack

- **Python/Django**: Provides the backend framework for handling business logic.
- **Django REST Framework**: Manages API creation for front-end communication.
- **PostgreSQL**: Stores credit-related data and transaction logs securely.
- **Docker**: Ensures consistent environments for deployment.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose
- PostgreSQL installed and running

### Installation

Clone the repository and set up the environment:

```bash
git clone https://example.com/credit-management.git
cd credit-management
pip install -r requirements.txt
docker build -t credit-management-service .
docker run -p 8002:8002 credit-management-service

