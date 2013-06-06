Rapidsms.org Website
====================

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

    git clone git://github.com/rapidsms/rapidsms.org.git
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

Exit the virtualenv and reactivate it to activate the settings just changed::

    deactivate
    workon website

Create the Postgres database and run the initial syncdb/migrate::

    createdb -E UTF-8 website
    python manage.py syncdb
    python manage.py migrate

You should now be able to run the development server::

    python manage.py runserver


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
