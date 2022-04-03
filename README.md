Library Management System

Step 1: Install python3.8
Step 2: Install pip3
Step 3: python -m pip install Django
Step 4: create adminuser using following command inside project
        python manage.py createsuperuser

Step 5: python manage.py runserver


Other commands

Reset migration

1. Remove the all migrations files within your project

        Go through each of your projects apps migration folder and remove everything inside, except the __init__.py file.

        Or if you are using a unix-like OS you can run the following script (inside your project dir):

        find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
        find . -path "*/migrations/*.pyc"  -delete
        rm .\library\__pycache__\* 
        rm .\library\migrations\__pycache__\*
        rm .\library\migrations\0001_initial.py

2. Drop the current database, or delete the db.sqlite3 if it is your case.
3. Create the initial migrations and generate the database schema:

        python manage.py makemigrations
        python manage.py migrate

And you are good to go.
