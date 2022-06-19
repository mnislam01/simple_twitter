# Simple Twitter

## Installation
1. Clone this repository: `git@github.com:mnislam01/simple_twitter.git`
2. cd into `simple_twitter`
3. Build: `docker-compose build`
4. Run: `docker-compose up`


## Create superuser
CMD: `docker-compose run twitter sh`

CMD: `python manage.py createsuperuser`

## Run tests
CMD: `docker-compose run twitter pytest`

## Admin page:
Navigate: `http://0.0.0.0:8000/admin`

## Swagger:
Navigate: `http://0.0.0.0:8000/api/swagger/`