Rapidsms.org Website
====================

.. image::
   https://api.travis-ci.org/rapidsms/rapidsms.org.png?branch=master
   :alt: Build Status
   :target: https://travis-ci.org/rapidsms/rapidsms.org

Below you will find basic setup and deployment instructions for the
Rapidsms.org website project. To begin you should have the following
applications installed on your local development system:

- Python >= 2.6 (2.7 recommended)
- `pip >= 1.1 <http://www.pip-installer.org/>`_
- `virtualenv >= 1.7 <http://www.virtualenv.org/>`_
- `virtualenvwrapper >= 3.0 <http://pypi.python.org/pypi/virtualenvwrapper>`_
- Postgres >= 8.4 (9.1 recommended)
- git >= 1.7

The deployment uses SSH with agent forwarding so you'll need to enable agent
forwarding if it is not already by adding ``ForwardAgent yes`` to your SSH
config.


Getting Started
---------------

If you are cloning the repo, you will also need to initialize submodules from
the root project directory::

    git clone git://github.com/rapidsms/rapidsms.org.git website/
    cd website/
    git submodule init
    git submodule update

Whenever you pull down from the repository, make sure to run ``git submodule
update``.

To setup your local environment you should create a virtualenv and install the
necessary requirements::

    mkvirtualenv --distribute website
    $VIRTUAL_ENV/bin/pip install -r $PWD/requirements/dev.txt

Then create a local settings file and set your ``DJANGO_SETTINGS_MODULE`` to
use it::

    cp website/settings/local.example.py website/settings/local.py
    echo "export DJANGO_SETTINGS_MODULE=website.settings.local" >> $VIRTUAL_ENV/bin/postactivate
    echo "unset DJANGO_SETTINGS_MODULE" >> $VIRTUAL_ENV/bin/postdeactivate

You will also need to set a >=50 length secret key, as the settings files pulls the
SECRET_KEY from the local environment::
    echo "export SECRET_KEY=somethinglongerthan50chars" >> $VIRTUAL_ENV/bin/postactivate
    echo "unset SECRET_KEY" >> $VIRTUAL_ENV/bin/postdeactivate

Exit the virtualenv and reactivate it to activate the settings just changed::

    deactivate
    workon website

Create the Postgres database and run the initial syncdb/migrate::

    createdb -E UTF-8 rapidsms_website
    python manage.py syncdb
    python manage.py migrate

Configure your application on Github. Visit the "Applications" section of your
Github account settings, and create a new application.

* **Name**: You can use any name for the application.
* **URL**: The URL of your site. For local testing, use ``http://localhost:8000``.
* **Callback URL**: Add the *absolute path* to "/users/login/github/callback/"
  as the callback URL.

Add the Github-generated Client ID (``GITHUB_KEY``) and Client Secret
(``GITHUB_SECRET``) to your `local_settings.py` file, and run::

    python manage.py setup_github

You should now be able to run the development server::

    python manage.py runserver

Solr Install & Configuration
-----------------------------

Rapidsms.org utilizes `Solr <http://lucene.apache.org/solr/>`_  for the search
backend. In order to utilize search locally, you will need to install and configure
Solr::

    ./scripts/solr-install.sh

This will install Solr in the root of the repository. To run Solr::

    ./scripts/solr-run.sh

If you make changes to the `Haystack <http://haystacksearch.org/>`_ indices, you
will need to rebuild the Solr schema. Due to an existing Haystack `issue <https://github.com/toastdriven/django-haystack/pull/706>`_, there
is a helper script to do this as well::

    ./scripts/solr-rebuild-schema.sh

After running the script, you will need to restart Solr.

Lastly, you will need to build the initial search index::

    python manage.py rebuild_index

Deployment
----------

You can deploy changes to a particular environment with the ``deploy``
command. This takes an optional branch name to deploy. If the branch is not
given, it will use the default branch defined for this environment in
``env.branch``::

    fab staging deploy
    fab staging deploy:new-feature

New requirements or South migrations are detected by parsing the VCS changes
and will be installed/run automatically.

Running the tests
-----------------

You can run the tests via::

    python manage.py test packages projects users

To check the test coverage you should have `coverage <https://pypi.python.org/pypi/coverage>`_
installed and run::

    # Install coverage
    pip install coverage
    # Run tests with coverage
    coverage run --source=website manage.py test packages projects users
    # Show the coverage report with missing lines
    coverage report -m --omit="*/tests/*,*/migrations/*,*/settings/*,"
