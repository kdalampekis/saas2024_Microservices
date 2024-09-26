# NTUA ECE SAAS 2024 PROJECT
  
## TEAM (4)


# Τίτλος Εφαρμογής
SolveMyProblemApp

# Solve My Problem App

## Description

**Solve My Problem App** is a comprehensive microservices-based web application designed to facilitate the submission, management, and resolution of complex computational problems. Tailored for administrators and authorized users, the app streamlines the entire workflow from problem submission to result analysis, ensuring efficient handling of various problem types such as Vehicle Routing Problem (VRP), Linear Programming Problem (LP), N-Queens Problem (NQ), Bin Packing Problem (BP), and Mixed-Integer Programming Problem (MIP).

## Key Features

- **User Authentication & Management**: Secure login system for administrators, leveraging token-based authentication and Google OAuth integration for seamless access control.
- **Problem Submission Service**: Allows users to submit diverse computational problems, associating each submission with relevant metadata and solver models.
- **Credit Management**: Tracks and manages user credits, ensuring that each problem submission deducts the appropriate cost based on the problem type.
- **Computation Engine**: Executes submitted problems using specialized solvers, handling the computational workload efficiently.
- **Results Management**: Provides detailed results and execution status for each submission, enabling users to view, edit, run, and delete submissions as needed.
- **Analytics & Logging**: Monitors application performance and user interactions, offering insights through comprehensive analytics dashboards.
- **Frontend Interface**: User-friendly web interface built with modern frontend technologies, facilitating easy navigation and interaction with all services.

## Technologies Used

- **Backend**:
    - **Django & Django REST Framework**: Robust framework for building scalable APIs and managing backend logic.
    - **PostgreSQL**: Reliable relational database for data storage and management.
    - **Docker**: Containerization for consistent deployment across different environments.
- **Frontend**:
    - **React**: Dynamic and responsive user interface for an enhanced user experience.
- **Authentication**:
    - **Django Allauth**: Integration for social authentication, including Google OAuth.
- **Testing**:
    - **Apache JMeter**: Comprehensive stress testing to ensure application reliability under heavy load.

## Installation

```bash
git clone https://yourproject.git
cd yourproject
pip install -r requirements.txt
docker-compose up --build 
```

### Usage
Navigate to the problem submission page, select the problem type, enter the required details, and submit. The system will deduct the corresponding credit cost and process the problem using the computation engine.



### Additional Information

- Be sure to replace placeholder URLs and paths like `https://yourproject.git` with actual links to your repository and any other specific data that pertains to your project.
- You might want to expand the **Installation** section with more specific instructions if your setup process requires more steps (like setting up Docker containers, etc.).
- The **Usage** section can be expanded based on the specific functionalities and user interactions your application supports.

This README provides a solid base that explains what the application does, how to get started, and how to contribute, which are the primary pieces of information potential users and contributors would look for.
