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


CUSTOMER_SERVICE = ("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVpdnp2SHVySVpuS1dGVnltZTdSUiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlcHJvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjM4NDhjZmExYjQxZjAwNjc4MTg4MzciLCJhdWQiOiJjYXBzdG9uZWFwaSIsImlhdCI6MTU5NzUyNzEyMCwiZXhwIjoxNTk3NTM0MzIwLCJhenAiOiJkenY1a0VLN0N0YUo3TEw3TjVpd1NWVUYyaTBkdGFlZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0Om1lbWJlcnMiLCJnZXQ6cGFja2FnZXMiXX0.doxc85CnZyCmVX5GTTXwNZ6HKQQq5ALnrqRI6VYIf9OeBq3Fbt-BfpwHoQnoCqC0qxIqDU1ysDNX7OfvEYp-p2ONrnUh37-xTWVlNL1FmUj_ylXIZR-CFmlVDR7mirGhQrEdvJ40NCvdq_0hxGGydq4i45OdVboS7wE3b28HLRxLP-AJ9uqZ3CFEWPIvO0V2-JAMvfBdnvUFNeudSo90xIWIfhOcXtzk3eFLxBcST_qvi0fVDildP6hwnlBg_c5fM6t4FtzAOwjKBwzT0lDvIFfMvFJykqAnrZJKOrrKYCfHHBpGATNERBt_Gandl-ubi6PsmBRkn2VSNiu0jS4UEQ")
SUPERVISOR= ("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVpdnp2SHVySVpuS1dGVnltZTdSUiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlcHJvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjM4NDhhYTQ3NjY4MzAwNjdlYTg3ODAiLCJhdWQiOiJjYXBzdG9uZWFwaSIsImlhdCI6MTU5NzUyNDY5OCwiZXhwIjoxNTk3NTMxODk4LCJhenAiOiJkenY1a0VLN0N0YUo3TEw3TjVpd1NWVUYyaTBkdGFlZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOm1lbWJlcnMiLCJnZXQ6bWVtYmVycyIsImdldDpwYWNrYWdlcyIsInBhdGNoOm1lbWJlcnMiLCJwYXRjaDpwYWNrYWdlcyIsInBvc3Q6bWVtYmVycyJdfQ.X7eu0OM7nniMpdiICsHA3JfULMMTp0W-JBDf2e28uZvPzz6EnkpgwA93undTnIlOSE4XDrTx11ppGCXeLqAIqoFtb-vfqMUW636AW_csKso4sMtVUDmtrL0KDFAAyrrsB8uMGTKHrsaZuZshSzQhEXBLNedrsSYWH4wz8A0IecCtOdVFL-AC4-RhHZIM5NP-OgizwNVI1oREfyD2qoSDrGKc3gl6usu75FoZwullFozo3KIrLMGhfG79cDx_Yfwbs-irP6XTYISczcj8kXxbIGPYPCD8ts8ZpwpPvCu8jfgs2dbuUNK4d2VWKT0gFx_ZheZdm3wNsi1c0HbpztIrvA")
MANGER= ("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVpdnp2SHVySVpuS1dGVnltZTdSUiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlcHJvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjM4NDg1OWZlNDUyNzAwNmQ5MzI0NDIiLCJhdWQiOiJjYXBzdG9uZWFwaSIsImlhdCI6MTU5NzUyNDM1NiwiZXhwIjoxNTk3NTMxNTU2LCJhenAiOiJkenY1a0VLN0N0YUo3TEw3TjVpd1NWVUYyaTBkdGFlZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOm1lbWJlcnMiLCJkZWxldGU6cGFja2FnZXMiLCJnZXQ6bWVtYmVycyIsImdldDpwYWNrYWdlcyIsInBhdGNoOm1lbWJlcnMiLCJwYXRjaDpwYWNrYWdlcyIsInBvc3Q6bWVtYmVycyIsInBvc3Q6cGFja2FnZXMiXX0.CIpC-LaQGPvY8x--DpWmWl3JWjnwIbE7QGYzcdGuKnLgH6V2FfURyo69e1IhQ5hz9RJ8ucxeSgobRKrvF2Wd-Z-l801oMU_HRvnec1Mm8Qpyd0FNdPz5qUZKrm7Wloe9vrcYJdhWn0kI9mSfyugNPz0eqUJe8wI229RALeo1eSmjochtqjOzxtbf9bjK3r3JcX4-fzajM8Gg6mFAauJFowojO5IpEnaKfbMNVU4bdb_8SgRMtR3MEdKs62N-9gxZJcbXJy-mC1VIl82ftsR42Z2Tot-oAVqvNQvIBW9fFB5hwfPIT2SOCR9i0K_1g0u6cHfTKiIcg6G7Qfa1kL9s8g")



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

        res = self.client().post('/members', json = json_create_mamber,  headers={'Authorization': f'Bearer {CUSTOMER_SERVICE}'})
        data = json.loads(res.data)
       
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        
    
    def test_error_401_new_member(self):
        """ POST new member without Authorization."""

        json_create_mamber = {
            'name' : 'manar',
            'phone' : 568796879
        } 

        res = self.client().post('/members', json = json_create_mamber)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], 'unauthorized')

    def test_error_422_create_new_member(self):
        """Error POST new member."""

        json_member_without_name = {
            'phone' : 568796879
        } 

        res = self.client().post('/members', json = json_member_without_name, headers={'Authorization': f'Bearer {CUSTOMER_SERVICE}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)


# Tests for /members GET
#----------------------------------------------------------------------------#

    def test_get_all_members(self):
        """Test GET all members."""
        res = self.client().get('/members?page=1', headers={'Authorization': f'Bearer {CUSTOMER_SERVICE}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_error_401_get_all_members(self):
        """ GET all members without Authorization."""
        res = self.client().get('/members?page=1')
        data = json.loads(res.data)
        

        self.assertEqual(res.status_code, 401)
        

    def test_error_404_get_members(self):
        """Test Error GET all members."""
        res = self.client().get('/members?page=1125125125', headers={'Authorization': f'Bearer {CUSTOMER_SERVICE}'})
        data = json.loads(res.data)
       

        self.assertEqual(res.status_code, 404)
        


# Tests for /members PATCH
#----------------------------------------------------------------------------#

    def test_edit_member(self):
        """Test PATCH  members"""
        json_edit_member_with_new_phone = {
            'phone' : 547382045
        } 
        res = self.client().patch('/members/1', json = json_edit_member_with_new_phone, headers={'Authorization': f'Bearer {SUPERVISOR}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_error_400_edit_member(self):
            """ PATCH without json body"""

            res = self.client().patch('/members/12345', headers={'Authorization': f'Bearer {SUPERVISOR}'})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 400)
            

#----------------------------------------------------------------------------#
# Tests for /members DELETE
#----------------------------------------------------------------------------#

    def test_error_401_delete_member(self):
        """Test DELETE existing member without Authorization"""
        res = self.client().delete('/members/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

        

    def test_error_403_delete_member(self):
        """ DELETE  member with missing permissions"""
        res = self.client().delete('/members/1', headers={'Authorization': f'Bearer {CUSTOMER_SERVICE}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        

    def test_delete_member(self):
        """Test DELETE existing member"""
        res = self.client().delete('/members/1', headers={'Authorization': f'Bearer {SUPERVISOR}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        
        

    def test_error_404_delete_member(self):
        """Test DELETE non existing member"""
        res = self.client().delete('/members/43234', headers={'Authorization': f'Bearer {SUPERVISOR}'})
        data = json.loads(res.data)

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

        res = self.client().post('/packages', json = json_create_package, headers={'Authorization': f'Bearer {MANGER}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
       

    def test_error_422_create_new_package(self):
        """ Error POST new package."""

        json_create_package_without_name = {
            'duration' : '5 months'
        } 

        res = self.client().post('/packages', json = json_create_package_without_name, headers={'Authorization': f'Bearer {MANGER}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        


# Tests for /package GET
#----------------------------------------------------------------------------#

    def test_get_all_package(self):
        """Test GET all package."""
        res = self.client().get('/packages?page=1', headers={'Authorization': f'Bearer {CUSTOMER_SERVICE}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        

    def test_error_401_get_all_package(self):
        """Test GET all package without Authorization."""
        res = self.client().get('/packages?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
       

    def test_error_404_get_package(self):
        """Test Error GET all package."""
        res = self.client().get('/packages?page=12345678', headers={'Authorization': f'Bearer {CUSTOMER_SERVICE}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        


# Tests for /package PATCH
#----------------------------------------------------------------------------#

    def test_edit_package(self):
        """Test PATCH existing package"""
        json_edit_package = {
            'duration' : '5 months'
        } 
        res = self.client().patch('/packages/1', json = json_edit_package, headers={'Authorization': f'Bearer {MANGER}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
       

    def test_error_400_edit_package(self):
        """Test PATCH with non valid id json body"""
        res = self.client().patch('/packages/1', headers={'Authorization': f'Bearer {MANGER}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        
    def test_error_404_edit_package(self):
        """Test PATCH with non valid id"""
        json_edit_package = {
            'duration' : '5 months'
        } 
        res = self.client().patch('/package/123456', json = json_edit_package, headers={'Authorization': f'Bearer {MANGER}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)


# Tests for /packages DELETE
#----------------------------------------------------------------------------#

    def test_error_401_delete_package(self):
        """Test DELETE existing package without Authorization"""
        res = self.client().delete('/packages/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_error_403_delete_package(self):
        """Test DELETE existing movie with wrong permissions"""
        res = self.client().delete('/packages/1', headers={'Authorization': f'Bearer {CUSTOMER_SERVICE}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)

    def test_delete_package(self):
        """Test DELETE existing package"""
        res = self.client().delete('/packages/1', headers={'Authorization': f'Bearer {MANGER}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        
        

    def test_error_404_delete_package(self):
        """Test DELETE non existing package"""
        res = self.client().delete('/packages/45678', headers={'Authorization': f'Bearer {MANGER}'}) 
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        


if __name__ == "__main__":
    unittest.main()
