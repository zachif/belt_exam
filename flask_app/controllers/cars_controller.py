from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.cars_model import Cars

@app.route('/dashboard')
def dashboard():
    return render_template('logged_in.html', first_name=session['user_name'], user_id=session['id'], cars=Cars.get_cars_sell_names())

@app.route('/new')
def newcar():
    return render_template('create_car.html',user_id=session['id'])

@app.route('/add_car',methods=['POST'])
def createcar():
    data={
        'price' : request.form['price'],
        'model' :request.form['model'],
        'make' :request.form['make'],
        'year' :request.form['year'],
        'description' :request.form['description'],
        'user_id' : session['id']
    }
    valid=Cars.create_car(data)
    if valid:
        return redirect('/dashboard')
    return redirect('/new')

@app.route('/delete/<int:id>')
def deletecar(id):
    data={
        'id': id
    }
    Cars.delete_car(data)
    return redirect('/dashboard')

@app.route('/edit/<int:id>')
def editcar(id):
    data={
        'id': id
    }
    cars=Cars.get_car_by_id(data)
    return render_template('update_car.html',car=cars[0],user_id=session['id'])

@app.route('/update_car/<int:id>',methods=['POST'])
def updatecar(id):
    data={
        'price' : request.form['price'],
        'model' :request.form['model'],
        'make' :request.form['make'],
        'year' :request.form['year'],
        'description' :request.form['description'],
        'id' : id
    }
    valid=Cars.update_car(data)
    if valid:
        return redirect('/dashboard')
    return redirect('/edit/'+str(id))

@app.route('/show/<int:id>')
def showcar(id):
    data={
        'id': id
    }
    cars=Cars.get_car_and_seller(data)
    return render_template('view.html',car=cars[0],user_id=session['id'])
    

@app.route('/purchase/<int:car_id>')
def purchase(car_id):
    data={
        'car_id': car_id,
        'user_id' : session['id']
    }
    Cars.purchase_car(data)
    return redirect('/dashboard')

@app.route('/user/<int:id>')
def purchased(id):
    data={
        'id': id
    }
    car=Cars.get_purchased_cars_by_user(data)
    print('####################################################')
    print(car)
    return render_template('purchased.html', cars=car, first_name=session['user_name'])