
<!-- ABOUT THE PROJECT -->
## About The Project

Project is about to scrap finanacial data and insert available data to database. Also you can list available financial history that is stored in our DB.

### Built With

This section should list any major technologies that used in this project.
* [Python](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [Docker Compose](https://docker.com)
* [Postgresql](https://www.postgresql.org/)
* [Nginx](https://www.nginx.com/)





<!-- GETTING STARTED -->
## Getting Started

This is an example of how you will set up this project locally and run it locally.
To get a local copy up and running follow these simple example steps.



### Prerequisites

* Featuring needs
    - docker-compose version 1.22.0
    - Docker version 20.10.6

### Installation

First clone the repo to the local machine and run the following commands


1. First clone the repo to the local machine and run the following commands
    ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
2. build the docker compose file with docker-compose
    ```sh
   sudo docker-compose build
   ```
3. Run the docker-compose
   ```sh
   sudo docker-compose up -d
   ```
4. Create the tables of the model to database (initially tables are not created)
   ```sh
   sudo docker-compose run web /usr/local/bin/python create_db.py
   ```



<!-- USAGE EXAMPLES -->
## Usage

When you finish installion of the project, now instatallion is ready to user.
First tables of the database is empty, we need to populate the tables with the POST

Insert Data – POST  http://localhost:8000/yahoofinance/api/v1.0/insert_history

Request body:
            {
                "company_name": "PD",
            }

it will return 200 with a proper description message, if data inserted

If you want to extract already entries you need to GET

Retreive Data – GET http://localhost:8000/yahoofinance/api/v1.0/history/list

Request Body:
            {
                "company_name": "PD",
            }

if company history is available in DB. it will return populated entries

