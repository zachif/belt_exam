from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash

db = 'cars_schema'

class Cars:
    def __init__(self, data):
        self.id=data['id']
        self.price=data['price']
        self.model=data['model']
        self.make=data['make']
        self.year=data['year']
        self.description=data['description']
        self.user_id=data['user_id']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']

    @classmethod
    def get_cars_sell_names(cls):
        print("###################################################")
        return connectToMySQL(db).query_db("SELECT * FROM cars JOIN users ON cars.user_id=users.id")
    
    @classmethod
    def create_car(cls,data):
        valid=True
        if not data['price'] or float(data['price'])< 1:
            flash("Price can't be 0.")
            valid=False
        if len(data['model']) < 1:
            flash("Model feild can't be left blank")
            valid=False
        if len(data['make']) < 1:
            flash("Make feild can't be left blank")
            valid=False
        if not data['year'] or int(data['year']) < 1:
            flash("Year can't be 0.")
            valid=False
        if len(data['description']) < 1:
            flash("Description feild can't be left blank")
            valid=False
        if valid:
            connectToMySQL(db).query_db("INSERT INTO cars (price, model, make, year, description, user_id) VALUES (%(price)s, %(model)s, %(make)s, %(year)s, %(description)s,%(user_id)s)",data)
            return valid
        
    @classmethod
    def delete_car(cls,data):
        connectToMySQL(db).query_db("DELETE FROM cars WHERE id=%(id)s",data)

    @classmethod
    def get_car_by_id(cls,data):
        return connectToMySQL(db).query_db("SELECT * FROM cars WHERE id=%(id)s",data)
    
    @classmethod
    def update_car(cls,data):
        valid=True
        if not data['price'] or float(data['price'])< 1:
            flash("Price can't be 0.")
            valid=False
        if len(data['model']) < 1:
            flash("Model feild can't be left blank")
            valid=False
        if len(data['make']) < 1:
            flash("Make feild can't be left blank")
            valid=False
        if not data['year'] or int(data['year']) < 1:
            flash("Year can't be 0.")
            valid=False
        if len(data['description']) < 1:
            flash("Description feild can't be left blank")
            valid=False
        if valid:
            connectToMySQL(db).query_db("UPDATE cars SET price=%(price)s, model=%(model)s ,make=%(make)s ,year=%(year)s ,description=%(description)s WHERE id=%(id)s",data)
            return valid
        
    @classmethod
    def get_car_and_seller(cls, data):
        return connectToMySQL(db).query_db("SELECT * FROM cars JOIN users ON cars.user_id=users.id WHERE cars.id=%(id)s",data)
    
    @classmethod
    def purchase_car(cls, data):
        print('#######################################################')
        connectToMySQL(db).query_db("UPDATE cars SET sold=1 WHERE id=%(car_id)s",data)
        connectToMySQL(db).query_db("INSERT INTO purchasd_cars (car_id, user_id) VALUES (%(car_id)s,%(user_id)s)", data)

    @classmethod
    def get_purchased_cars_by_user(cls,data):
        return connectToMySQL(db).query_db("SELECT * FROM purchasd_cars JOIN cars ON purchasd_cars.car_id = cars.id WHERE purchasd_cars.user_id=%(id)s", data)
