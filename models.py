import os
from sqlalchemy import Column, String, Integer, create_engine, Date, Float, Table, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import date
from config import database_setup



# Database Setup 
#----------------------------------------------------------------------------#


# If run locally, key does not exist, so use locally set database instead.
database_path = os.environ.get('DATABASE_URL', "postgres://{}:{}@{}/{}".format(database_setup["user_name"], database_setup["password"], database_setup["port"], database_setup["database_name_production"]))
db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    #setup a flask application and a SQLAlchemy service
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

def db_drop_and_create_all():
    #drops the database tables and starts fresh 
    db.drop_all()
    db.create_all()
    db_init_records()

def db_init_records():
    #init test records

    new_member = (Member(
        name = 'faten',
        gender = 'Male',
        phone = 568796876
        ))

    new_package = (Package(
        name = 'pronse',
        duration = '3 month',
        price = 200
        ))


    new_member.insert()
    new_package.insert()
    db.session.commit()


# Participation N:N 
#----------------------------------------------------------------------------#



# members Model 
#----------------------------------------------------------------------------#

class Member(db.Model):  
  __tablename__ = 'members'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  gender = Column(String, nullable=False) 
  phone = Column(Integer, nullable=False)   

  def __repr__(self):
    return f'<Member {self.id} {self.name}>'

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
      'gender': self.gender, 
      'phone': self.phone 
    }


# packages Model 
#----------------------------------------------------------------------------#

class Package(db.Model):  
  __tablename__ = 'packag'

  id = Column(Integer, primary_key=True)
  name = Column(String(80), unique=True, nullable=False)
  duration = Column(String, nullable=False)
  price = Column(Integer, nullable=False) 

  def __repr__(self):
    return f'<Package {self.id} {self.name}>'


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
      'duration': self.duration,
      'price': self.price
    }
