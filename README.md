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
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
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
 [link](link)


  ## Endpoint 
----------------------------------------------------

  ### GET /members
```bash
  curl -X GET http://127.0.0.1:5000/members
```
get all members from db paginthion 

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
insert member in database 

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
edit any member in database.
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
DELETE  member from db  

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
get all mempackages bers from db paginthion 


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
insert packages in database 

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
DELETE  packages from db  

```bash 
{
  "delete": 1
  "success": true
}

```


 ## Auth0 link 


[https://coffepro.us.auth0.com/authorize?audience=capstoneapi&response_type=token&client_id=dzv5kEK7CtaJ7LL7N5iwSVUF2i0dtaed&redirect_uri=http://localhost:5000/](https://coffepro.us.auth0.com/authorize?audience=capstoneapi&response_type=token&client_id=dzv5kEK7CtaJ7LL7N5iwSVUF2i0dtaed&redirect_uri=http://localhost:5000/)

