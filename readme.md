# Simple api for maintaining a employee database
This repo contains the source code for a simple api to maintain employee database. 
It sends email triggers whenever the a new device is associated/disassociated
### How to use 
-Before proceeding make sure all requirements are installed. <br>
-You can install all requirements by using `pip install -r requirements.txt`.<br>

#### Run it on local system
- `git clone https://github.com/theimperium20/sqllite-flask-api.git`
- Run `python3 employee_details.py` on powershell or terminal

#### Endpoints 
- GET /api/v1/employees `-- Expects - None` `-- Returns all records of employees`
- GET /api/v1/employees/id `-- Expects - employee id` `Returns details of the employee`
- POST /api/v1/employees `--Expects {"device_id": value, "email": "value", "firstname": "value","lastname": "value"}` `-- Returns the inserted records`
- PUT /api/v1/employees/id `-- Expects {"device_id": value, "email": "value", "firstname": "value","lastname": "value"}` `--Returns the updated records`
-PATCH /api/v1/employees/device/id `--Expects id {"device_id":value}` `--Returns the updated records`
-PATCH /api/v1/employees/email/id `--Expects id {"email":"value"}` `--Returns the updated records`


