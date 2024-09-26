### 2. Problem Submission Service

# Problem Submission Service

## Description

Manages the submission and initial processing of problems. It validates submissions and routes them to the appropriate computation services.

## Features

- **Submit Problems**: Users can submit problems to be solved.
- **Validate Submissions**: Ensures that submissions meet predefined criteria.
- **Route Problems**: Sends problems to the specific computational service required.

## Technology Stack

- Django REST Framework
- RabbitMQ for message queuing
- PostgreSQL

## Getting Started

### Prerequisites

- Python 3.8+
- Docker

### Installation

```bash
git clone https://example.com/problem-submission.git
cd problem-submission
pip install -r requirements.txt
docker build -t problem-submission-service .
docker run -p 8001:8001 problem-submission-service