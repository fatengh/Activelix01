# Activelix

Activelix is a platform provide streaming channels as packages. 

## Models
 - class packages (name , duration , price)
 - class Members (id , name , gender, phone(56784932)) 
- Relationship between them m:m

## Endpoints
- Two GET requests (packages,Members)
- Two POST requests (packages,Members)
- Two PATCH requests (packages,Members)
- Two DELETE requests (packages,Members)

## Roles
- custemr servier (Get packages,Members)
- supervisor (Get packages,Members\ patch packages,Members\ post Members\delete  packages)
- manger (All permissions)

 ## Start Project locally
  
- virtual envairomant
```bash
python3 -m venv ./venv
source ./venv/bin/activate
```
- Install the dependencies
```bash
pip install -r requirements.txt
```
- Install the dependencies
```bash
pip install -r requirements.txt
```
- database set up 
```bash

python manage.py db init
python manage.py db migrate
python manage.py db upgrade

```
- run the server 
```bash
flask run
```
- To tests
```bash
python3 test_app.py
```

 ## Herohu URL
 [https://activelix01.herokuapp.com/](https://activelix01.herokuapp.com/)


  ## Endpoint 
----------------------------------------------------

  ### GET /members
```bash
  curl -X GET http://127.0.0.1:5000/members
```
1- get all members from db paginthion 
2- need Permission
```bash 
{
  "members": [
    {
      "gender": "Male", 
      "id": 1, 
      "name": "faten", 
      "phone": 568796876
    }, 
    {
      "gender": "female", 
      "id": 2, 
      "name": "rawia", 
      "phone": 568793
    }
  ], 
  "success": true
}

```

### POST /members

```bash 
curl http://127.0.0.1:5000/members -H "Content-Type: application/json" -X POST -d '{"name":"manar","gender":"female","phone":"676543”}'
```
1-insert member in database 
2- need Permission

```bash 
{
  "created": [
    {
      "gender": "female", 
      "id": 2, 
      "name": "lama", 
      "phone": 7865379
    }
  ], 
  "success": true
}

  ### PATCH /members/1


```bash 
curl http://127.0.0.1:5000/members/1 -H "Content-Type: application/json" -X POST -d '{"name":"faten","gender":"male","phone":"55555”}'
```
1- edit any member in database.
2- need Permission

```bash 
{
  
  "members": [
    {
      "gender": "Male", 
      "id": 1, 
      "name": "faten", 
      "phone": 55555
    }, 
    'success': true
```


  ### DELETE /members/1
```bash
  curl -X DELETE http://127.0.0.1:5000/members/1
```
1-DELETE  member from db 
2- need Permission 

```bash 
{
  "delete": 1
  "success": true
}

```



### GET /packages

```bash
  curl -X GET http://127.0.0.1:5000/packages
```
1- get all mempackages bers from db paginthion 
2- need Permission

```bash 
{
  "packages": [
    {
      "duration": "3 months", 
      "id": 1, 
      "name": "gold", 
      "price": 200
    }
  ], 
  "success": true
}

```
### POST /packages

```bash 
curl http://127.0.0.1:5000/packages -H "Content-Type: application/json" -X POST -d '{"name":"silver","duration":"6months","price":"500”}'
```
1- insert packages in database 
2- need Permission

```bash 
{
  "packages": [
     {
      "duration": "6months", 
      "id": 2, 
      "name": "silver", 
      "price": 500
    }
  ], 
  "success": true
}
```

### PATCH /packages/2

```bash 
curl http://127.0.0.1:5000/packages/2 -H "Content-Type: application/json" -X POST -d '{"name":"silver","duration":"5months","price":"500”}'
```
edit any member in database.
```bash 
{
  
  "package": [
   {
      "duration": "5months", 
      "id": 2, 
      "name": "silver", 
      "price": 500
    }, 
    'success': true
```
 ### DELETE /packages/1
```bash
  curl -X DELETE http://127.0.0.1:5000/packages/1
```
1- DELETE  packages from db  
2- need Permission
```bash 
{
  "delete": 1
  "success": true
}

```


 ## Auth0 link 


[https://coffepro.us.auth0.com/authorize?audience=capstoneapi&response_type=token&client_id=dzv5kEK7CtaJ7LL7N5iwSVUF2i0dtaed&redirect_uri=http://localhost:5000/](https://coffepro.us.auth0.com/authorize?audience=capstoneapi&response_type=token&client_id=dzv5kEK7CtaJ7LL7N5iwSVUF2i0dtaed&redirect_uri=http://localhost:5000/)

### auth0 roles 
1- custemr servier

"permissions"
    "get:members",
    "get:packages"

token 
```bash 
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVpdnp2SHVySVpuS1dGVnltZTdSUiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlcHJvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjNkODUyNThmMThhYTAwNjg5ZGNlMmUiLCJhdWQiOiJjYXBzdG9uZWFwaSIsImlhdCI6MTU5Nzg2NzQ5MywiZXhwIjoxNTk3ODc0NjkzLCJhenAiOiJkenY1a0VLN0N0YUo3TEw3TjVpd1NWVUYyaTBkdGFlZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0Om1lbWJlcnMiLCJnZXQ6cGFja2FnZXMiXX0.fCX-MPm2CNYKUTNcp2HAvwI4dgbMgIgRMdgw07aPbdoQI8RGPIRPKVGB1zyc-cbcbmaS98l8httJOOCKwQJv_n_KvvDP58BQcJ72xAQVkCK6ZMtXlBdX9cVYcGeRSnDL8cKqhq4laIjkwFnJeVbo8H3wPbS8MhxjGJcRMBeF5HplxfmuWMP46gQ4jsExRiqlD5kGRw-MmsdJiKJHJGg2MMhHv0fczNAPl2BmgaoMz8fI_fVmHh7kmDN4-MYBZ9Nr0TAAzxlRR0GAIlBolgeakOVusGoWlL6yiVmPbCVxEFgUlkNCX2718OkJCD-T8m1PepB1Xo-Kh9g4mQkGofo6nw
```

2- supervisor 

"permissions"
    "delete:members",
    "get:members",
    "get:packages",
    "patch:members",
    "patch:packages",
    "post:members"

```bash  
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVpdnp2SHVySVpuS1dGVnltZTdSUiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlcHJvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjNkODU2N2IyMzAzMDAwNjcwNGYzNmYiLCJhdWQiOiJjYXBzdG9uZWFwaSIsImlhdCI6MTU5Nzg2ODA2MCwiZXhwIjoxNTk3ODc1MjYwLCJhenAiOiJkenY1a0VLN0N0YUo3TEw3TjVpd1NWVUYyaTBkdGFlZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOm1lbWJlcnMiLCJnZXQ6bWVtYmVycyIsImdldDpwYWNrYWdlcyIsInBhdGNoOm1lbWJlcnMiLCJwYXRjaDpwYWNrYWdlcyIsInBvc3Q6bWVtYmVycyJdfQ.Lf45ZV9pDrtGiBXtYoY0v8sjGcKzJsf7dH1PcR6C7X-Lr8V02R-cd8kHfDNs2_lttpoqqEEwKaPv0MAbiOOe39IpmRf_s_dU5GrQmfdSnY6FceZ8YIWYzslBDdX-1b9w51ppuL7gDLDDXJWExxI4bZ8V-4U0urh9LcclQUh5aMGZ3WfD1_djzgLhDh8Ifbwpvm6dMAnj0m480j9N6QUCXoCevdXLHLOZD0wUBCToZd-NPhYbFn4ycjBJXCI0QVoNw5z4mxmRTBv16PgCoZqw0G61-WA19TBn0Hl1QFCjup8dREd1iYPfq9WUvqY4sxTdupGBdicgWK5bghsxW4pwIQ
```

3- manger 

"permissions": 
    "delete:members",
    "delete:packages",
    "get:members",
    "get:packages",
    "patch:members",
    "patch:packages",
    "post:members",
    "post:packages"

```bash 
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVpdnp2SHVySVpuS1dGVnltZTdSUiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlcHJvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjNkODU5MmZlNDUyNzAwNmQ5MzcyMDUiLCJhdWQiOiJjYXBzdG9uZWFwaSIsImlhdCI6MTU5Nzg2ODg3MiwiZXhwIjoxNTk3ODc2MDcyLCJhenAiOiJkenY1a0VLN0N0YUo3TEw3TjVpd1NWVUYyaTBkdGFlZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOm1lbWJlcnMiLCJkZWxldGU6cGFja2FnZXMiLCJnZXQ6bWVtYmVycyIsImdldDpwYWNrYWdlcyIsInBhdGNoOm1lbWJlcnMiLCJwYXRjaDpwYWNrYWdlcyIsInBvc3Q6bWVtYmVycyIsInBvc3Q6cGFja2FnZXMiXX0.G0tCu0s-waE_rrKYp5QC2gZmWQ5MxKeeVgtLxMBuRkN0dD4Wxfg95l1t7ugZ0eyOpg4avh1bdRGu1530kfT4oCxPL0L2ljGSHCrBc5Q9y9ANsqaa6kuUa-084tI_caxhOlASdR5b0EXGkaUVH6ot9Kfq5r264EbU7MFmHgzGXSzgUHFcmja13KFaOFw7Ze5OJuyay2XEkjxrOacs3g3kKiJU9AOe6hznwF3mVH7TOPReNxbnjqIrooutR7bTPXW-DxX-ZGJIAPKEEDJc3C1agyx9hqKQ_ZxRQ9mQeJzPtulkcL1v7upuTyt_oUvfR2FuzG4bwQnuxdK6S3xXsQ2tIw
```