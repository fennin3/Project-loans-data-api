# Project Loans Data API
Test Task

## Problem Description
Develop a simple Django REST API that will have endpoints to get the data collected from an external source

## Endpoints
* /api/countries - return the list of countries
* /api/sectors - return the list of sectors
* /api/projects - return the list of projects’ titles
* /api/loans - return the list of loans (basically that table but in JSON format)
* /docs/ - API Documentation
* /playground/ - API Documentation 


## Technologies Used
* Python
    - Django
    - Django Rest Framework
    - Selenium
* SQLite
* Docker
* Chrome Browser
* Chrome Driver

## Architectural Consideration
1. All the fields of the ```Loan``` model are charfields with ```max_length``` of 255 to accomodate the the scraped data easily.

## Setup Instructions
To run this project
1. Clone project
2. Create .env file in the root directory of the project to store your SECRET_KEY. The file must contain this ```SECRET_KEY=your-secret-key```
3. Download and install docker
4. Build and run docker container with a single command: 
```
docker-compose up —build
```

## Running migrations
Open a new terminal and run:
```
docker ps
docker exec -it <CONTAINER_NAME> bash
python manage.py makemigrations loan_app
python manage.py migrate
```
## Running script to pull data and popuplate the database(run in the container's bash terminal)
```
python populate_data.py
```
