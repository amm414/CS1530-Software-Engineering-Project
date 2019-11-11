# CS1530-Software-Engineering-Project
The Repository for Code and Documentation for the CS1530 class.

Get FLASK installed:

https://timmyreilly.azurewebsites.net/python-flask-windows-development-environment-setup/


Good Tutorial on FLASK:

https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

Chapters 1-5 are good for now.


### Running Locally:

1. Follow this tutorial to install Python and Flask (https://timmyreilly.azurewebsites.net/python-flask-windows-development-environment-setup/)

2. Setup Virtual Environment using the command "mkvirtualenv {name-of-env}" where the {name-of-env} represents whatever name you wish to call this virtual environment.

3. Use the virtual environment by the command "workon {name-of-env}" and navigate to the directory where source code is/will be located. Then, enter "setprojectdir ." to specify this as working directory location. This means whenever virtual environment is started (through the 'workon' command) it will automatically navigate to this directory.

4. Use the 'pip install' commands to install 'flask' and 'flask_sqlalchemy' individually.

5. Run the 'export FLASK=craigversity.py' (NOTE: replace 'export' with 'set' for WINDOWS). Followed by 'flask run' to initialize application.

6. Open browser and navigate to URL: 'localhost:5000' and be amazed!!

7. If you need to initialize the database, run 'flask initdb' when the application is not running, and after you 'set' or 'export' the FLASK (part 5 above).

* NOTE: To turn on 'development mode' to allow changes to be loaded without restarting the flask application: before running 'flask run'; enter 'export FLASK_ENV=development' (remember to replace 'export' with 'set' for WINDOWS)
