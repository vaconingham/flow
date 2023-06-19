# Flow File Prcessor
(In Pogress)


### Background

#### Context
D0010 flow files that are received via SFTP and store the revevant meter-point data in the database. A new service that can import these files and allows their information to be accessed via the web by support staff is required. Files will be imported via the command-line. 

#### Problem
Currently we have to manually create the data for flow files in the database. This is slow, redundant, and prone to errors.

#### Current behaviour
There is no way to automatically process D0010 files and store the relevant meter-point data information.

#### Expected behaviour
Users will be able to use django-admin commands to process D0010 files, automatically storing the relevant data for each meter-point in a local SQLite database.


### Getting started

1. Clone the project and create/activate a virtual environment.
2. Install project dependencies in requirements.txt
3. Run makemigrations and migrate
4. Run tests `python manage.py test`
5. Run `python manage.py d0010 --help` for information.
6. You may test the command by running `python manage.py flows/samples/d0010.txt`
7. Run `python manage.py runserver` and visit the Django admin console 
to verify the entries have been created.

ATTENTION: You will need to create environment variables with a SECRET_KEY, or manually change the SECRET_KEY in the settings file to test the project.


### Outstading work
    
- Field formatting and validation should match the JXXXX code.
- Populate with further information i.e. address, organisation, status, timestamps, etc.
- Reconsider what should happen on_delete.
- Check field constraints and consider appropriate primary keys.
- Enforce choices list in model fields.
- Implement registers.
- Admin console requires configuration for improved searching, editing, and ordering.
- Complete flow data points.


### Improvemnents

The current implementation only deals with D0010 files, and only processes the flows found in the sample file. Further development is required to ensure this command can properly accomodate all types of flow files and flow items.
