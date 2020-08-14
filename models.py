import os
from sqlalchemy import Column, String, Integer, create_engine, Date, Float
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import date
from config import database_setup

#----------------------------------------------------------------------------#
# Database Setup 
#----------------------------------------------------------------------------#

# Use Production Database.
# If run locally, key does not exist, so use locally set database instead.
database_path = os.environ.get('DATABASE_URL', "postgres://{}:{}@{}/{}".format(database_setup["user_name"], database_setup["password"], database_setup["port"], database_setup["database_name_production"]))

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    '''binds a flask application and a SQLAlchemy service'''
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

def db_drop_and_create_all():
    '''drops the database tables and starts fresh
    can be used to initialize a clean database
    '''
    db.drop_all()
    db.create_all()
    db_init_records()

def db_init_records():
    '''this will initialize the database with some test records.'''

    new_member = (Member(
        name = 'faten',
        gender = 'Male',
        age = 25
        ))

    new_package = (Package(
        title = 'faten first Package',
        release_date = date.today()
        ))

    new_participation = Participation.insert().values(
        Package_id = new_package.id,
        member_id = new_member.id,
        member_fee = 500.00
    )

    new_member.insert()
    new_package.insert()
    db.session.execute(new_participation) 
    db.session.commit()

#----------------------------------------------------------------------------#
# Participation Junction Object N:N 
#----------------------------------------------------------------------------#

# Instead of creating a new Table, the documentation recommends to create a association table
Participation = db.Table('Participation', db.Model.metadata,
    db.Column('Package_id', db.Integer, db.ForeignKey('packages.id')),
    db.Column('Member_id', db.Integer, db.ForeignKey('members.id')),
    db.Column('member_fee', db.Float)
)

#----------------------------------------------------------------------------#
# members Model 
#----------------------------------------------------------------------------#

class Member(db.Model):  
  __tablename__ = 'members'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  gender = Column(String) #//
  age = Column(Integer)   #//

  def __init__(self, name, gender, age):
    self.name = name
    self.gender = gender
    self.age = age

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name' : self.name,
      'gender': self.gender, #//
      'age': self.age #//
    }

#----------------------------------------------------------------------------#
# packages Model 
#----------------------------------------------------------------------------#

class Package(db.Model):  
  __tablename__ = 'packages'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  release_date = Column(Date) #//
  members = db.relationship('member', secondary=Participation, backref=db.backref('Participation', lazy='joined'))

  def __init__(self, title, release_date) :
    self.title = title
    self.release_date = release_date

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title' : self.title,
      'release_date': self.release_date
    }