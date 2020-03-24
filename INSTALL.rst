Get Started
====================


Prerequisites
--------------------
* Postgres
* RabbitMQ


Getting Started
---------------------
pipenv install
pipenv shell


Setup static files
---------------------

git submodule update --remote --merge

cd website/static/flat-ui
git checkout 2.0.0

python manage.py collectstatic

