# CS1530-Software-Engineering-Project
The Repository for Code and Documentation for the CS1530 class.

## CraigVersity

This web application was designed for a software engineering class at the University of Pittsburgh as a 5-man group. This application mirrors Craigslist in that it is a location for buyers and sellers to meet to proceed with transactions. We focus on creating a Craigslist for universities where the users have an account associated with the university (like email). 

This app is a prototype with a focus on the software design lifecycle (waterfall to be more precise). We designed, planned, created mockups, estimated cost/time, and implemented a primitive version to showcase to our class and professor. 

An online demo of this application can be found at [Andrew’s personal website here]( https://andrew-morgan-website.herokuapp.com/craigversity).
 

## Getting it to run locally

Get FLASK installed:

https://timmyreilly.azurewebsites.net/python-flask-windows-development-environment-setup/


Good Tutorial on FLASK:

https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

Chapters 1-5 are good for now.


### Running Locally:

1. Follow this tutorial to install Python and Flask (https://timmyreilly.azurewebsites.net/python-flask-windows-development-environment-setup/)

2. Setup Virtual Environment using the command "mkvirtualenv {name-of-env}" where the {name-of-env} represents whatever name you wish to call this virtual environment.

3. Use the virtual environment by the command "workon {name-of-env}" and navigate to the directory where source code is/will be located. Then, enter "setprojectdir ." to specify this as working directory location. This means whenever virtual environment is started (through the 'workon' command) it will automatically navigate to this directory.

4. Use the 'pip install' commands to install 'flask' and 'flask_sqlalchemy' and 'flask_socketio' individually.

5. Run the 'export FLASK=craigversity.py' (NOTE: replace 'export' with 'set' for WINDOWS). Then, setup the database using the 'flask initdb' command.

6. Run the application server by entering 'python craigversity' (this assumes craigversity.py is within your current directory)

7. Open browser and navigate to URL: 'localhost:5000' and be amazed!!


* NOTE: 'flask run' does not work with the sockets. Therefore, we must run it with the 'python craigversity.py' command
