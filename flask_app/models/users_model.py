from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_bcrypt import Bcrypt
from flask import flash
import re

bcrypt=Bcrypt(app)
EMAIL= re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
db = 'cars_schema'

class Users:
    def __init__(self, data):
        self.id=data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']

    @classmethod
    def get_user_by_id(cls, data):
        return connectToMySQL(db).query_db("SELECT first_name FROM users WHERE id = %(id)s;", data)

    @classmethod
    def register_user(cls,data):
        valid=True
        if len(data['first_name']) < 3:
            flash("First name must be atleast 3 characters.")
            valid=False
        if len(data['last_name']) < 3:
            flash("Last name must be atleast 3 characters.")
            valid=False
        if not EMAIL.match(data['email']):
            flash("You must use a valid email address.")
            valid=False
        if connectToMySQL(db).query_db('SELECT email FROM users WHERE email = %(email)s', data):
            flash("An account with this email address already exists.")
            valid=False
        if len(data['password']) < 8:
            flash("The passwords must be atleast 8 characters.")
            valid=False
        if data['password'] != data['confirm_password']:
            flash("Passwords don't match.")
            valid=False
        if valid:
            data['password'] = bcrypt.generate_password_hash(data['password'])
            print(data["password"])
            result=connectToMySQL(db).query_db("INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)",data)
            print('_________________________________________________________')
            print(result)
            return valid
        
    @classmethod
    def login_user(cls, data):
        valid = True
        if not connectToMySQL(db).query_db('SELECT email FROM users WHERE email = %(email)s', data):
            flash("Your password or email doesn't match.")
            valid=False
        print(connectToMySQL(db).query_db('SELECT password FROM users WHERE email = %(email)s', data))
        if valid and not bcrypt.check_password_hash((connectToMySQL(db).query_db('SELECT password FROM users WHERE email = %(email)s', data))[0]['password'],data['password']):
            flash("Your password or email doesn't match.") 
            valid=False
        if valid:
            return (connectToMySQL(db).query_db('SELECT id FROM users WHERE email = %(email)s', data))[0]['id']
        return valid