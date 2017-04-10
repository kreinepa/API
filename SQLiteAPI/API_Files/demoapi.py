import os
import flask
import flask_sqlalchemy
import flask_restless
import click
import itsdangerous
from itsdangerous import JSONWebSignatureSerializer
from itsdangerous import Signer


############################################################################
#####################CODE FOR MySQL DATABASE ONLY###########################
############################################################################

#Extra imports for MySQL database:
#from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import relationship, backref

#Replacek database_path with path to your MySQL server within the single quotations
#engine = create_engine('datbase_path', convert_unicode=True, echo=False)
#Base = declarative_base()
#Base.metadata.reflect(engine)

#Replace Table with an existing table within your MySQL Database
#class Table(Base):
#    __table__ = Base.metadata.tables['table']

############################################################################
############################################################################


#Sets the directories to get the correct CSV file for creating the DB
basedir = os.path.dirname(__file__)
parentdir = os.path.dirname(__file__) + os.sep  + '..'

# Create the Flask application and the Flask-SQLAlchemy object.
app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = flask_sqlalchemy.SQLAlchemy(app)

# Create your Flask-SQLALchemy models as usual but with the following two
# (reasonable) restrictions:
#   1. They must have a primary key column of type sqlalchemy.Integer or
#      type sqlalchemy.Unicode.
#   2. They must have an __init__ method which accepts keyword arguments for
#      all columns (the constructor in flask.ext.sqlalchemy.SQLAlchemy.Model
#      supplies such a method, so you don't need to declare a new one).
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)                     #,unique=True                  
    birth_date = db.Column(db.String)

#This is an example of a second table
#class Computer(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   name = db.Column(db.Unicode, unique=True)
#   vendor = db.Column(db.Unicode)
#   purchase_time = db.Column(db.DateTime)
#   owner_id = db.Column(db.Integer, db.ForeignKey('person.id'))
#   owner = db.relationship('Person', backref=db.backref('computers',
#                                                         lazy='dynamic'))


# Create the database tables.
db.create_all()

# Create the Flask-Restless API manager.
manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(Person, methods=['GET', 'POST', 'DELETE'])
#manager.create_api(Computer, methods=['GET'])

# start the flask loop
#app.run()

#Command Line actions
#Decorator takes object below and passes it as an action
@app.cli.command()

#Users must run 'flask initdb' to reflect any changes in the sample database
def initdb():
    #Populates 'flask --help' with information on commandline
    """Create empty database tables"""

    # This creates the table and the schema
    db.drop_all()
    db.create_all()

@app.cli.command()
def load_data():
    """Populate Database talbes with the explicit file"""
    #Inputs the .csv file information into our DB model defined above
    with open(parentdir + os.sep + 'test.csv', 'r') as test:
        for line in test.readlines():
            (name, birth_date) = line.strip().split(',')
            db.engine.execute("INSERT INTO person (name,birth_date) VALUES('{}','{}')"
                              .format(name,birth_date)) 
