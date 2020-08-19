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


CUSTOMER_SERVICE = ("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVpdnp2SHVySVpuS1dGVnltZTdSUiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlcHJvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjNkODUyNThmMThhYTAwNjg5ZGNlMmUiLCJhdWQiOiJjYXBzdG9uZWFwaSIsImlhdCI6MTU5Nzg2NzQ5MywiZXhwIjoxNTk3ODc0NjkzLCJhenAiOiJkenY1a0VLN0N0YUo3TEw3TjVpd1NWVUYyaTBkdGFlZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0Om1lbWJlcnMiLCJnZXQ6cGFja2FnZXMiXX0.fCX-MPm2CNYKUTNcp2HAvwI4dgbMgIgRMdgw07aPbdoQI8RGPIRPKVGB1zyc-cbcbmaS98l8httJOOCKwQJv_n_KvvDP58BQcJ72xAQVkCK6ZMtXlBdX9cVYcGeRSnDL8cKqhq4laIjkwFnJeVbo8H3wPbS8MhxjGJcRMBeF5HplxfmuWMP46gQ4jsExRiqlD5kGRw-MmsdJiKJHJGg2MMhHv0fczNAPl2BmgaoMz8fI_fVmHh7kmDN4-MYBZ9Nr0TAAzxlRR0GAIlBolgeakOVusGoWlL6yiVmPbCVxEFgUlkNCX2718OkJCD-T8m1PepB1Xo-Kh9g4mQkGofo6nw")
SUPERVISOR= ("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVpdnp2SHVySVpuS1dGVnltZTdSUiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlcHJvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjNkODU2N2IyMzAzMDAwNjcwNGYzNmYiLCJhdWQiOiJjYXBzdG9uZWFwaSIsImlhdCI6MTU5Nzg2ODA2MCwiZXhwIjoxNTk3ODc1MjYwLCJhenAiOiJkenY1a0VLN0N0YUo3TEw3TjVpd1NWVUYyaTBkdGFlZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOm1lbWJlcnMiLCJnZXQ6bWVtYmVycyIsImdldDpwYWNrYWdlcyIsInBhdGNoOm1lbWJlcnMiLCJwYXRjaDpwYWNrYWdlcyIsInBvc3Q6bWVtYmVycyJdfQ.Lf45ZV9pDrtGiBXtYoY0v8sjGcKzJsf7dH1PcR6C7X-Lr8V02R-cd8kHfDNs2_lttpoqqEEwKaPv0MAbiOOe39IpmRf_s_dU5GrQmfdSnY6FceZ8YIWYzslBDdX-1b9w51ppuL7gDLDDXJWExxI4bZ8V-4U0urh9LcclQUh5aMGZ3WfD1_djzgLhDh8Ifbwpvm6dMAnj0m480j9N6QUCXoCevdXLHLOZD0wUBCToZd-NPhYbFn4ycjBJXCI0QVoNw5z4mxmRTBv16PgCoZqw0G61-WA19TBn0Hl1QFCjup8dREd1iYPfq9WUvqY4sxTdupGBdicgWK5bghsxW4pwIQ")
MANGER= ("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVpdnp2SHVySVpuS1dGVnltZTdSUiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlcHJvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjNkODU5MmZlNDUyNzAwNmQ5MzcyMDUiLCJhdWQiOiJjYXBzdG9uZWFwaSIsImlhdCI6MTU5Nzg2ODg3MiwiZXhwIjoxNTk3ODc2MDcyLCJhenAiOiJkenY1a0VLN0N0YUo3TEw3TjVpd1NWVUYyaTBkdGFlZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOm1lbWJlcnMiLCJkZWxldGU6cGFja2FnZXMiLCJnZXQ6bWVtYmVycyIsImdldDpwYWNrYWdlcyIsInBhdGNoOm1lbWJlcnMiLCJwYXRjaDpwYWNrYWdlcyIsInBvc3Q6bWVtYmVycyIsInBvc3Q6cGFja2FnZXMiXX0.G0tCu0s-waE_rrKYp5QC2gZmWQ5MxKeeVgtLxMBuRkN0dD4Wxfg95l1t7ugZ0eyOpg4avh1bdRGu1530kfT4oCxPL0L2ljGSHCrBc5Q9y9ANsqaa6kuUa-084tI_caxhOlASdR5b0EXGkaUVH6ot9Kfq5r264EbU7MFmHgzGXSzgUHFcmja13KFaOFw7Ze5OJuyay2XEkjxrOacs3g3kKiJU9AOe6hznwF3mVH7TOPReNxbnjqIrooutR7bTPXW-DxX-ZGJIAPKEEDJc3C1agyx9hqKQ_ZxRQ9mQeJzPtulkcL1v7upuTyt_oUvfR2FuzG4bwQnuxdK6S3xXsQ2tIw")



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
