================================
PayFast package for django-oscar
================================

Welcome to the Django Oscar Payfast development docs. This project is still under development. Please see the
TODO list pre release directives.

Project structure
------------------

:/payfast: The payfast source code
:/sandbox: A sandbox django oscar instance to demonstrate integration into the checkout flow
:/tests: Unit and integrated tests to run against the payfast source

Testing
-------
This project is tested against multiple python versions using tox and pytest.
Running the test suite:

- Clone the repository: git clone https://github.com/zengoma/django-oscar-payfast.git django-oscar-payfast
- Always make sure you are on the development branch: git checkout -b develop
- It is highly recommended that you now create and activate your python virtual environment
- Run the following command from the project root to setup the development sandbox: make install
- You can run the "``py.test``" command to run the test suite against your currently installed python version.
- Run "``tox``" from the command line to run the test suite against multiple python versions.
- If you would like to see the payfast integration in action run "`sandbox/manage.py runserver 0.0.0.0:80`" and visit http://localhost in your web browser. You need to run on port 80 otherwise the payfast demo gateway will throw a return url error.

License
-------

The package is released under the `MIT license`_.

.. _`MIT license`: https://github.com/zengoma/django-oscar-payfast/blob/develop/LICENSE


Pre release TODOS
------------------

- Finish writing unit and integrated tests
- Finish off the sample implementation in the Django oscar sandbox
- Build Full documentation using sphinx (and autodoc for doctrings)
- Setup pipeline on Travis CI
- Merge first tagged release with master branch
- Push sphinx docs to readthedocs.io or amazon S3 (managed by Travis CI)
- Publish the package on PyPI (managed by Travis CI)ion in action