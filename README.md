# Overview
This repository contains a Dockerized Django application interfaced with a MySQL database. It is designed to facilitate quick setup via Docker and Docker Compose.


# Prerequisites

To use this project, you must have the following installed:
- Docker (https://docs.docker.com/get-docker/)
- Docker Compose (https://docs.docker.com/compose/install/)

# Setup Instructions

### 1. Clone the Repository
To get started, clone this repository to your local machine:

```bash
git  clone https://github.com/souma125/social_network.git
## go to application directory
cd social_network
```

### 2. Environment Configuration

If code base does not contain `.env` file, create a `.env` file at root folder and add following variables: 
```bash
# Database configuration
DATABASE_NAME=socialNetworkDB
DATABASE_USER=root
DATABASE_PASSWORD=password
DATABASE_PORT=3306

# Application port
APPLICATION_PORT=8000
```
### 3. Check Port Availability
Ensure **db and application ports**, those are declared at `.env` file are available on your machine. Syntax may look like below on linux:
```bash
# Check MySQL port
lsof -i :3306

# Check application port
lsof -i :8000
```
If either command outputs any information, it means the port is currently in use, and you will either need to free up the port or configure the application to use different ports.

### 4. Running Docker Compose
With your `.env` file in place and ports confirmed available, you can launch the containers:
```bash
docker-compose up --build -d
# or
docker-compose up -d
```
This command builds/pulls the images if they don't exist and starts the containers in detached mode. After the completion of both database and application deployment, the application waits for the database to go live. Then, it checks for migrations. If migrations are required, they will start automatically and immediately. After that, the application will go live. 

### 5. Accessing the Application
Once the containers are running, your Django application should be accessible on: `http://localhost:8000`. You can adjust the `APPLICATION_PORT` in the `.env` file if you need to use a different port.

### 6. Stopping the Application
```bash
docker-compose down
```
### 7. Troubleshooting
Troubleshoot due to any kinds of error occurred on `db` or `application` you can access log via below command
```bash
# for application
docker-compose logs web
# for db
docker-compose logs db
``` 
### 8. Conclusion
This guide provides detailed instructions for setting up and running the `Social Network Django application` using Docker and Docker Compose. If you encounter any issues, refer to the troubleshooting section or reach out for support.

Make sure to replace `[YOUR REPOSITORY URL HERE]` and `[YOUR REPOSITORY DIRECTORY NAME]` with the actual URL of your Git repository and the name of the directory into which your project will be cloned. This README is designed to give users all the information they need to get your application up and running.