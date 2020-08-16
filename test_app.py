import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import db_drop_and_create_all, setup_db, Member, Package, db_drop_and_create_all
from config import bearer_tokens
from sqlalchemy import desc
from datetime import date
from app import create_app
# Create dict with Authorization key and Bearer token as values. 
# Later used by test classes as Header

customer_service_auth_header = {
    'Authorization': bearer_tokens['customer_service']
}

supervisor_auth_header = {
    'Authorization': bearer_tokens['supervisor']
}

manger_auth_header = {
    'Authorization': bearer_tokens['manger']
}


#----------------------------------------------------------------------------#

class ActivelixTestCase(unittest.TestCase):
    """This class represents the  test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = 'postgres://postgres:6210665@localhost:5432/activelix'
        setup_db(self.app, self.database_path)
        db_drop_and_create_all()
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass


#----------------------------------------------------------------------------#
# Tests for /members POST
#----------------------------------------------------------------------------#

    def test_create_new_member(self):
        """Test POST new member."""

        json_create_mamber = {
            'name' : 'manar',
            'phone' : 568796879
        } 

        res = self.client().post('/members', json = json_create_mamber, headers = customer_service_auth_header)
        
       
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.get_json()['success'], True)
        
    
    def test_error_401_new_member(self):
        """ POST new member without Authorization."""

        json_create_mamber = {
            'name' : 'manar',
            'phone' : 568796879
        } 

        res = self.client().post('/members', json = json_create_mamber)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.get_json()['message'], 'unauthorized')

    def test_error_422_create_new_member(self):
        """Error POST new member."""

        json_member_without_name = {
            'phone' : 568796879
        } 

        res = self.client().post('/members', json = json_member_without_name, headers = customer_service_auth_header)
       

        self.assertEqual(res.status_code, 422)
        self.assertEqual(res.get_json()['success'], False)


# Tests for /members GET
#----------------------------------------------------------------------------#

    def test_get_all_members(self):
        """Test GET all members."""
        res = self.client().get('/members?page=1', headers = customer_service_auth_header)
        self.assertEqual(res.status_code, 200)

    def test_error_401_get_all_members(self):
        """ GET all members without Authorization."""
        res = self.client().get('/members?page=1')
        

        self.assertEqual(res.status_code, 401)
        

    def test_error_404_get_members(self):
        """Test Error GET all members."""
        res = self.client().get('/members?page=1125125125', headers = customer_service_auth_header)
       

        self.assertEqual(res.status_code, 404)
        


# Tests for /members PATCH
#----------------------------------------------------------------------------#

    def test_edit_member(self):
        """Test PATCH  members"""
        json_edit_member_with_new_phone = {
            'phone' : 547382045
        } 
        res = self.client().patch('/members/1', json = json_edit_member_with_new_phone, headers = supervisor_auth_header)
       
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    def test_error_400_edit_member(self):
            """ PATCH without json body"""

            res = self.client().patch('/members/12345', headers = supervisor_auth_header)
            

            self.assertEqual(res.status_code, 400)
            

#----------------------------------------------------------------------------#
# Tests for /members DELETE
#----------------------------------------------------------------------------#

    def test_error_401_delete_member(self):
        """Test DELETE existing member without Authorization"""
        res = self.client().delete('/members/1')

        self.assertEqual(res.status_code, 401)
        

    def test_error_403_delete_member(self):
        """ DELETE  member with missing permissions"""
        res = self.client().delete('/members/1', headers = customer_service_auth_header)
        

        self.assertEqual(res.status_code, 403)
        

    def test_delete_member(self):
        """Test DELETE existing member"""
        res = self.client().delete('/members/1', headers = supervisor_auth_header)
        

        self.assertEqual(res.status_code, 200)
        
        

    def test_error_404_delete_member(self):
        """Test DELETE non existing member"""
        res = self.client().delete('/members/43234', headers = supervisor_auth_header)
        

        self.assertEqual(res.status_code, 404)
        


# Tests for /package POST
#----------------------------------------------------------------------------#

    def test_create_new_package(self):
        """Test POST new package."""

        json_create_package = {
            'name' : 'gold',
            'duration' : '4 months',
            'price' : 300
        } 

        res = self.client().post('/packages', json = json_create_package, headers = manger_auth_header)
        

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.get_json()['success'], True)
       

    def test_error_422_create_new_package(self):
        """ Error POST new package."""

        json_create_package_without_name = {
            'duration' : '5 months'
        } 

        res = self.client().post('/packages', json = json_create_package_without_name, headers = manger_auth_header)

        self.assertEqual(res.status_code, 422)
        


# Tests for /package GET
#----------------------------------------------------------------------------#

    def test_get_all_package(self):
        """Test GET all package."""
        res = self.client().get('/packages?page=1', headers = customer_service_auth_header)
        

        self.assertEqual(res.status_code, 200)
        

    def test_error_401_get_all_package(self):
        """Test GET all package without Authorization."""
        res = self.client().get('/packages?page=1')
        

        self.assertEqual(res.status_code, 401)
       

    def test_error_404_get_package(self):
        """Test Error GET all package."""
        res = self.client().get('/packages?page=12345678', headers = customer_service_auth_header)
      

        self.assertEqual(res.status_code, 404)
        


# Tests for /package PATCH
#----------------------------------------------------------------------------#

    def test_edit_package(self):
        """Test PATCH existing package"""
        json_edit_package = {
            'duration' : '5 months'
        } 
        res = self.client().patch('/packages/1', json = json_edit_package, headers = manger_auth_header)
        

        self.assertEqual(res.status_code, 200)
       

    def test_error_400_edit_package(self):
        """Test PATCH with non valid id json body"""
        res = self.client().patch('/packages/1', headers = manger_auth_header)
       

        self.assertEqual(res.status_code, 400)
        
    def test_error_404_edit_package(self):
        """Test PATCH with non valid id"""
        json_edit_package = {
            'duration' : '5 months'
        } 
        res = self.client().patch('/package/123456', json = json_edit_package, headers = manger_auth_header)
       

        self.assertEqual(res.status_code, 404)


# Tests for /packages DELETE
#----------------------------------------------------------------------------#

    def test_error_401_delete_package(self):
        """Test DELETE existing package without Authorization"""
        res = self.client().delete('/packages/1')

        self.assertEqual(res.status_code, 401)

    def test_error_403_delete_package(self):
        """Test DELETE existing movie with wrong permissions"""
        res = self.client().delete('/packages/1', headers = customer_service_auth_header)

        self.assertEqual(res.status_code, 403)

    def test_delete_package(self):
        """Test DELETE existing package"""
        res = self.client().delete('/packages/1', headers = manger_auth_header)
      

        self.assertEqual(res.status_code, 200)
        
        

    def test_error_404_delete_package(self):
        """Test DELETE non existing package"""
        res = self.client().delete('/packages/45678', headers = manger_auth_header) 
       

        self.assertEqual(res.status_code, 404)
        


if __name__ == "__main__":
    unittest.main()
