To run with docker-compose:
Run:

docker-compose build
docker-compose up

then go to http://127.0.0.1:5050/ to access PGAdmin

login: admin@admin.com
password: admin

To migrate the DBs, run:

docker-compose run app alembic revision --autogenerate -m "New Migration"
docker-compose run app alembic upgrade head




To run locally:

docker-compose build
docker-compose up

Stop the 'app' container
then run "uvicorn main:app --reload"