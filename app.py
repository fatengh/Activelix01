import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import db_drop_and_create_all, setup_db, Member, Package, Participation
from config import pagination

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
  '''create and configure the app'''
  
  # Create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)


  # db_drop_and_create_all() # uncomment this if you want to start a new database on app refresh

  #----------------------------------------------------------------------------#
  # CORS (API configuration)
  #----------------------------------------------------------------------------#

  
  # CORS Headers 


  #----------------------------------------------------------------------------#
  # Custom Functions
  #----------------------------------------------------------------------------#


  #----------------------------------------------------------------------------#
  #  API Endpoints
  #  ----------------------------------------------------------------
  #  NOTE:  For explanation of each endpoint, please have look at the README.md file. 
  #         DOC Strings only contain short description and list of test classes 
  #----------------------------------------------------------------------------#

  #----------------------------------------------------------------------------#
  # Endpoint /memberss GET/POST/DELETE/PATCH
  #----------------------------------------------------------------------------#
  @app.route('/members', methods=['GET'])
  @requires_auth('get:members')
  def get_members(payload):
    try:
      return jsonify({
        'success': True,
        'members': paginate_response(request, Member.query.order_by(Member.id).all())
      })
    except:
      abort(422)

  @app.route('/members', methods=['POST'])
  @requires_auth('post:members')
  def insert_members(payload):
    body = request.json
    name = body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', None)

    # Abort 400 if the name in the request matches any of the saved Member names
    if name in list(map(Member.get_name, Member.query.all())):
      abort(400, 'This name is already taken. Please provide a new name and try again.')

    # Abort 400 if any fields are missing
    if any(arg is None for arg in [name, age, gender]) or '' in [name, age, gender]:
      abort(400, 'name, age and gender are required fields.')

    # Create and insert a new member
    new_member = member(name=name, age=age, gender=gender)
    new_member.insert()

    # Return the newly created member
    return jsonify({
      'success': True,
      'members': [Member.query.get(new_member.id).format()]
    })
     
  @app.route('/members/<member_id>', methods=['PATCH'])
  @requires_auth('patch:members')
  def edit_members(payload, member_id):
    member = Member.query.get(member_id)

    # Abort 404 if the member was not found
    if member is None:
      abort(404)

    body = request.json
    name = body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', None)

    # Abort 400 if any fields are missing
    if any(arg is None for arg in [name, age, gender]) or '' in [name, age, gender]:
      abort(400, 'name, age and gender are required fields.')

    # Update the member with the requested fields
    member.name = name
    member.age = age
    member.gender = gender
    member.update()

    # Return the updated member
    return jsonify({
      'success': True,
      'members': [Member.query.get(member_id).format()]
    })


  @app.route('/members/<member_id>', methods=['DELETE'])
  @requires_auth('delete:members')
  def delete_members(payload, member_id):
    member = Member.query.get(member_id)

    # Abort 404 if the member was not found
    if member is None:
      abort(404)

    # Delete the member
    member.delete()

    return jsonify({
      'success': True,
      'delete': member_id
    })

  #----------------------------------------------------------------------------#
  # Endpoint /packages GET/POST/DELETE/PATCH
  #----------------------------------------------------------------------------#
  @app.route('/packages', methods=['GET'])
  @requires_auth('get:packages')
  def get_packages(payload):
      return jsonify({
      'success': True,
      'packages': paginate_response(request, Package.query.order_by(Package.id).all())
      })

  @app.route('/packages', methods=['POST'])
  @requires_auth('post:packages')
  def insert_packages(payload):
    body = request.json
    title = body.get('title', None)
    release_date = body.get('release_date', None)

    # Abort 400 if the title in the request matches any of the saved Package titles
    if title in list(map(Package.get_title, Package.query.all())):
      abort(400, 'This title is already taken. Please provide a new title and try again.')

    # Abort 400 if any fields are missing
    if any(arg is None for arg in [title, release_date]) or '' in [title, release_date]:
      abort(400, 'title and release_date are required fields.')

    # Create and insert a new Package
    new_package = Package(title=title, release_date=release_date)
    new_package.insert()

    # Return the newly created package
    return jsonify({
      'success': True,
      'packages': [Package.query.get(new_package.id).format()]
    })


  @app.route('/packages/<package_id>', methods=['PATCH'])
  @requires_auth('patcht:packages')
  def edit_packages(payload, package_id):
    package = Package.query.get(package_id)

    # Abort 404 if the package was not found
    if package is None:
      abort(404)

    body = request.json
    title = body.get('title', None)
    release_date = body.get('release_date', None)

    # Abort 400 if any fields are missing
    if any(arg is None for arg in [title, release_date]) or '' in [title, release_date]:
      abort(400, 'title and release_date are required fields.')

    # Update the package with the requested fields
    package.title = title
    package.release_date = release_date
    package.update()

    # Return the updated package
    return jsonify({
      'success': True,
      'packages': [Package.query.get(package_id).format()]
    })
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

  #----------------------------------------------------------------------------#
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
    app.run(host='0.0.0.0', port=8080, debug=True)