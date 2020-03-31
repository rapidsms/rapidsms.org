Rapidsms.org Website
===============================

.. image::
   https://api.travis-ci.org/rapidsms/rapidsms.org.png?branch=master
   :alt: Build Status
   :target: https://travis-ci.org/rapidsms/rapidsms.org

Below you will find basic setup and deployment instructions for the rapidsms_org
project. To begin you should have the following applications installed on your
local development system::

- Python >= 3.8
- `pip <http://www.pip-installer.org/>`_ >= 19
- `virtualenv <http://www.virtualenv.org/>`_ >= 1.10
- `virtualenvwrapper <http://pypi.python.org/pypi/virtualenvwrapper>`_ >= 16.0
- Postgres >= 12
- git >= 12.7


Getting Started
----------------------------------

First clone the repository from Github and switch to the new directory::

    git clone git@github.com:rapidsms/rapidsms.org.git
    cd rapidsms.org

To setup your local environment you should create a virtualenv and install the
necessary requirements::

    pipenv shell
    pipenv sync --dev

Create an .env file in the project home copying .env-template file and fill it properly::

    cp .env-template .env


Create the Postgres database and run the initial migrate, which will also execute any required migrations::

    createdb -E UTF-8 rapidsms_website
    python manage.py migrate

You should now be able to run the development server::

    python manage.py runserver


Create images
----------------------------------
create docker image and push on github::

    update version in Makefile
    make release


Run docker-compose
----------------------------------
run docker-compose using images::

    docker-compose pull
    docker-compose up


Running the tests
----------------------------------

You can run the tests via::

    python manage.py test src/
