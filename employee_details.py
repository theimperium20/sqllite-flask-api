
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os
import subprocess
# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'employee_db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)


# Init ma
ma = Marshmallow(app)

# Employee Class/Model
class Employee(db.Model):
  employee_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
  firstname = db.Column(db.String(80))
  lastname = db.Column(db.String(80))
  device_id = db.Column(db.Integer, unique=True)
  email = db.Column(db.String(200), unique=True)
  

  def __init__(self, firstname, lastname, device_id, email):
    #self.employee_id = employee_id
    self.firstname = firstname
    self.lastname = lastname
    self.device_id = device_id
    self.email = email

db.create_all()

# Employee Schema
class EmployeeSchema(ma.Schema):
  class Meta:
    fields = ('employee_id', 'firstname', 'lastname', 'device_id', 'email')
    
# Init schema
employee_schema = EmployeeSchema(strict=True)
employees_schema = EmployeeSchema(many=True, strict=True)

#Add new employee
@app.route('/api/v1/employee', methods=['POST'])
def add_employee():
  firstname = request.json['firstname']
  lastname = request.json['lastname']
  device_id = request.json['device_id']
  email = request.json['email']

  new_employee = Employee(firstname, lastname, device_id,email)

  db.session.add(new_employee)
  db.session.commit()
  
  return employee_schema.jsonify(new_employee)


# Get All Employees
@app.route('/api/v1/employee', methods=['GET'])
def get_employees():
  all_employees = Employee.query.all()
  result = employees_schema.dump(all_employees)
  return jsonify(result.data)


# Get Employee by ID
@app.route('/api/v1/employee/<employee_id>', methods=['GET'])
def get_employee():
  employee = Employee.query.get(employee_id)
  
  result = employee_schema.dump(employee)
  return jsonify(result.data)


# Update a Employee
@app.route('/api/v1/employee/<employee_id>', methods=['PUT'])
def update_employee(employee_id):
  employee = Employee.query.get(employee_id)
  
  
  firstname = request.json['firstname']
  lastname = request.json['lastname']
  device_id = request.json['device_id']
  email = request.json['email']

  employee.firstname = firstname
  employee.lastname = lastname
  employee.device_id = device_id
  employee.email = email

  db.session.commit()
  
  change = employee.firstname + ',' + employee.email
  wr = open('changes.txt', 'w')
  wr.write(change)
  wr.close()  

  subprocess.Popen(["python","send_trigger.py"]) #Run email script in the background
  return employee_schema.jsonify(employee)

#Update Device ID of Employee using Employee ID
@app.route('/api/v1/employee/device/<employee_id>', methods=['PATCH'])
def update_device_employee(employee_id):
  employee = Employee.query.get(employee_id)
  device_id = request.json['device_id']

  

  db.session.commit()
  
  change = employee.firstname + ',' + employee.email
  wr = open('changes.txt', 'w')
  wr.write(change)
  wr.close() 

  subprocess.Popen(["python","send_trigger.py"])   #Run email script in the background
  return employee_schema.jsonify(employee)

#Update Email ID of Employee using Employee ID
@app.route('/api/v1/employee/email/<employee_id>', methods=['PATCH'])
def update_email_employee(employee_id):
  employee = Employee.query.get(employee_id)

  email = request.json['email']

  employee.email = email

  db.session.commit()

  return employee_schema.jsonify(employee)

# Delete Employee
@app.route('/api/v1/employee/<employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
  employee = Employee.query.get(employee_id)
  db.session.delete(employee)
  db.session.commit()

  return employee_schema.jsonify(employee)

# Run Server
if __name__ == '__main__':
  app.run(debug=True)
  db.create_all()