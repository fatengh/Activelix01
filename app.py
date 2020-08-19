import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import db_drop_and_create_all, setup_db, Member, Package
import json
from flask_migrate import Migrate


DEFAULT_OFFSET = 1
DEFAULT_LIMIT = 20
# Get a list of paginated questions
def paginate_response(request, selection):
  offset = request.args.get('offset', DEFAULT_OFFSET, type=int)
  limit = request.args.get('limit', DEFAULT_LIMIT, type=int)
  start =  (offset - 1) * limit
  end = start + limit

  formatted_selection = [item.format() for item in selection]
  paginated_selection = formatted_selection[start:end]

  return paginated_selection

def create_app(test_config=None):
  '''create app and configure it'''
  
 
  app = Flask(__name__)
  db = SQLAlchemy(app)
  migrate = Migrate(app)
  setup_db(app)
  CORS(app)
  db_drop_and_create_all() # uncomment this if you want to start a new database on app refresh

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response
  #  API Endpoints
  #----------------------------------------------------------------------------#
  @app.route('/')
  def index():
    return ("WELCOME TO ACTIVELIX COMPANY")

  
  # memberss GET/POST/DELETE/PATCH
  #----------------------------------------------------------------------------#
  @app.route('/members', methods=['GET'])#
  @requires_auth('get:members')
  def get_members(payload):
    try:
      return jsonify({
        'success': True,
        'members': paginate_response(request, Member.query.order_by(Member.id).all())
      })
    except:
      abort(422)
 #------------------------------------------------
  @app.route('/members', methods=['POST'])
  @requires_auth('post:members')
  def insert_members(payload):
    body = request.json

    if not body:
          abort(400, {'message': 'request does not contain a valid JSON body.'})

    name = body.get('name', None)
    phone = body.get('phone', None)

    # Set gender to value or to 'Other' if not given
    gender = body.get('gender', 'Other')

    # abort if one of these are missing with appropiate error message
    if not name:
      abort(422, {'message': 'no name provided.'})

    if not phone:
      abort(422, {'message': 'no phone provided.'})

    # Create new instance of Actor & insert it.
    new_member = (Member(
          name = name, 
          phone = phone,
          gender = gender
          ))
    new_member.insert()

    return jsonify({
      'success': True,
      'created': [Member.query.get(new_member.id).format()]
    })

 #------------------------------------------------   
  @app.route('/members/<member_id>', methods=['PATCH'])
  @requires_auth('patch:members')
  def edit_members(payload, member_id):
    member = Member.query.get(member_id)

    # member was not found
    if member is None:
      abort(404)

    body = request.json
    name = body.get('name', None)
    age = body.get('age', None)
    phone = body.get('phone', None)

    # Abort 400 if any fields are missing
    if any(arg is None for arg in [name, age, phone]) or '' in [name, age, phone]:
      abort(400, 'name, age and phone are required fields.')

    # Update the member 
    member.name = name
    member.age = age
    member.phone = phone
    member.update()

    # Return the updated member
    return jsonify({
      'success': True,
      'members': [Member.query.get(member_id).format()]
    })

 #------------------------------------------------
  @app.route('/members/<member_id>', methods=['DELETE'])
  @requires_auth('delete:members')
  def delete_members(payload, member_id):
    member = Member.query.get(member_id)

    #  member was not found
    if member is None:
      abort(404)

    # Delete the member
    member.delete()

    return jsonify({
      'success': True,
      'delete': member_id
    })

  
  # packages GET/POST/DELETE/PATCH
  #----------------------------------------------------------------------------#
  @app.route('/packages', methods=['GET'])
  @requires_auth('get:packages')
  def get_packages(payload):
      return jsonify({
      'success': True,
      'packages': paginate_response(request, Package.query.order_by(Package.id).all())
      })
#------------------------------------------------
  @app.route('/packages', methods=['POST'])
  @requires_auth('post:packages')
  def insert_packages(payload):
    body = request.json
    name = body.get('name', None)
    duration = body.get('duration', None)
    price = body.get('price', None)

    if any(arg is None for arg in [name, duration, price]) or '' in [name, duration, price]:
      abort(400, 'name , duration and price are required fields.')

    new_package = Package(name=name, duration=duration, price=price)
    new_package.insert()

    return jsonify({
      'success': True,
      'packages': [Package.query.get(new_package.id).format()]
    })

#------------------------------------------------
  @app.route('/packages/<package_id>', methods=['PATCH'])
  @requires_auth('patch:packages')
  def edit_packages(payload, package_id):
    body = request.json
    if not package_id:
      abort(400, {'message': 'please append an package id to the request url.'})

    if not body:
      abort(400, {'message': 'request does not contain a valid JSON body.'})

    
    package_to_update = Package.query.filter(Package.id == package_id).one_or_none()

    if not package_to_update:
      abort(404, {'message': 'packagewith id {} not found in database.'.format(package_id)})

    
    name = body.get('name', package_to_update.name)
    duration = body.get('duration', package_to_update.duration)
    price = body.get('price',package_to_update.price)

    
    package_to_update.name = name
    package_to_update.duration = duration
    package_to_update.price = price

    
    package_to_update.update()

    return jsonify({
      'package': [Package.query.get(package_id).format()],
      'success': True,
      
    })
   #------------------------------------------------
  @app.route('/packages/<package_id>', methods=['DELETE'])
  @requires_auth('delete:packages')
  def delete_packages(payload, package_id):
    package = Package.query.get(package_id)

    # Abort 404 if the package was not found
    if package is None:
      abort(404)

    # Delete the package
    package.delete()

    return jsonify({
      'success': True,
      'delete': package_id
    })


  # Error Handlers
  #----------------------------------------------------------------------------#

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
                      "success": False, 
                      "error": 422,
                      "message": ("unprocessable")
                      }), 422

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
                      "success": False, 
                      "error": 400,
                      "message": ("bad request")
                      }), 400

  @app.errorhandler(404)
  def ressource_not_found(error):
      return jsonify({
                      "success": False, 
                      "error": 404,
                      "message": ("resource not found")
                      }), 404

  @app.errorhandler(AuthError)
  def authentification_failed(AuthError): 
      return jsonify({
                      "success": False, 
                      "error": AuthError.status_code,
                      "message": AuthError.error['description']
                      }), AuthError.status_code


  # After every endpoint has been created, return app
  return app

app = create_app()

if __name__ == '__main__':
    app.run()
