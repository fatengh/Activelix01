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
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVpdnp2SHVySVpuS1dGVnltZTdSUiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlcHJvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjM4NDhjZmExYjQxZjAwNjc4MTg4MzciLCJhdWQiOiJjYXBzdG9uZWFwaSIsImlhdCI6MTU5NzUyNzEyMCwiZXhwIjoxNTk3NTM0MzIwLCJhenAiOiJkenY1a0VLN0N0YUo3TEw3TjVpd1NWVUYyaTBkdGFlZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0Om1lbWJlcnMiLCJnZXQ6cGFja2FnZXMiXX0.doxc85CnZyCmVX5GTTXwNZ6HKQQq5ALnrqRI6VYIf9OeBq3Fbt-BfpwHoQnoCqC0qxIqDU1ysDNX7OfvEYp-p2ONrnUh37-xTWVlNL1FmUj_ylXIZR-CFmlVDR7mirGhQrEdvJ40NCvdq_0hxGGydq4i45OdVboS7wE3b28HLRxLP-AJ9uqZ3CFEWPIvO0V2-JAMvfBdnvUFNeudSo90xIWIfhOcXtzk3eFLxBcST_qvi0fVDildP6hwnlBg_c5fM6t4FtzAOwjKBwzT0lDvIFfMvFJykqAnrZJKOrrKYCfHHBpGATNERBt_Gandl-ubi6PsmBRkn2VSNiu0jS4UEQ
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
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVpdnp2SHVySVpuS1dGVnltZTdSUiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlcHJvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjM4NDhhYTQ3NjY4MzAwNjdlYTg3ODAiLCJhdWQiOiJjYXBzdG9uZWFwaSIsImlhdCI6MTU5NzUyNDY5OCwiZXhwIjoxNTk3NTMxODk4LCJhenAiOiJkenY1a0VLN0N0YUo3TEw3TjVpd1NWVUYyaTBkdGFlZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOm1lbWJlcnMiLCJnZXQ6bWVtYmVycyIsImdldDpwYWNrYWdlcyIsInBhdGNoOm1lbWJlcnMiLCJwYXRjaDpwYWNrYWdlcyIsInBvc3Q6bWVtYmVycyJdfQ.X7eu0OM7nniMpdiICsHA3JfULMMTp0W-JBDf2e28uZvPzz6EnkpgwA93undTnIlOSE4XDrTx11ppGCXeLqAIqoFtb-vfqMUW636AW_csKso4sMtVUDmtrL0KDFAAyrrsB8uMGTKHrsaZuZshSzQhEXBLNedrsSYWH4wz8A0IecCtOdVFL-AC4-RhHZIM5NP-OgizwNVI1oREfyD2qoSDrGKc3gl6usu75FoZwullFozo3KIrLMGhfG79cDx_Yfwbs-irP6XTYISczcj8kXxbIGPYPCD8ts8ZpwpPvCu8jfgs2dbuUNK4d2VWKT0gFx_ZheZdm3wNsi1c0HbpztIrvA
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
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVpdnp2SHVySVpuS1dGVnltZTdSUiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlcHJvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjM4NDg1OWZlNDUyNzAwNmQ5MzI0NDIiLCJhdWQiOiJjYXBzdG9uZWFwaSIsImlhdCI6MTU5NzUyNDM1NiwiZXhwIjoxNTk3NTMxNTU2LCJhenAiOiJkenY1a0VLN0N0YUo3TEw3TjVpd1NWVUYyaTBkdGFlZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOm1lbWJlcnMiLCJkZWxldGU6cGFja2FnZXMiLCJnZXQ6bWVtYmVycyIsImdldDpwYWNrYWdlcyIsInBhdGNoOm1lbWJlcnMiLCJwYXRjaDpwYWNrYWdlcyIsInBvc3Q6bWVtYmVycyIsInBvc3Q6cGFja2FnZXMiXX0.CIpC-LaQGPvY8x--DpWmWl3JWjnwIbE7QGYzcdGuKnLgH6V2FfURyo69e1IhQ5hz9RJ8ucxeSgobRKrvF2Wd-Z-l801oMU_HRvnec1Mm8Qpyd0FNdPz5qUZKrm7Wloe9vrcYJdhWn0kI9mSfyugNPz0eqUJe8wI229RALeo1eSmjochtqjOzxtbf9bjK3r3JcX4-fzajM8Gg6mFAauJFowojO5IpEnaKfbMNVU4bdb_8SgRMtR3MEdKs62N-9gxZJcbXJy-mC1VIl82ftsR42Z2Tot-oAVqvNQvIBW9fFB5hwfPIT2SOCR9i0K_1g0u6cHfTKiIcg6G7Qfa1kL9s8g
```