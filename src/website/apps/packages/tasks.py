from celery import task


@task
def update_package(package):
    """Updates a single package from pypi.

        args: takes a packages instance as a single argument.
    """
    package.update_from_pypi()
    package.save()


@task
def update_packages():
    """Updates all active packages."""

    from .models import Package

    packages = Package.objects.active_packages()
    for package in packages:
        packages.update_from_pypi()
