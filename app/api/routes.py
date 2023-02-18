from flask import Blueprint, request, jsonify, render_template, Response
from helpers import token_required
from models import db, Car, car_schema, cars_schema

api = Blueprint('api',__name__,url_prefix='/api')

# Create
@api.route('/cars',methods=['POST'])
@token_required
def create_car(current_user_token):
    vin = request.json['vin']
    make  =request.json['make']
    model = request.json['model']
    year = request.json['year']
    color = request.json['color']
    user_token = current_user_token.token

    # Check if VIN is already in database
    car = Car.query.get(vin)
    if(car == None):
        car = Car(vin, make, model,year,color, user_token=user_token)
    else:
        car.make = make
        car.model = model
        car.year = year
        car.color = color
        car.user_token = current_user_token.token

    # car = Car(vin, make, model,year,color, user_token=user_token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

#Retrieve cars
@api.route('/cars',methods=['GET'])
@token_required
def get_car(current_user_token):
    collector = current_user_token.token
    cars = Car.query.filter_by(user_token = collector).all()
    response = jsonify(cars_schema.dump(cars))
    return response

# Retrieve single car
@api.route('/cars/<id>',methods=['GET'])
@token_required
def get_single_car(current_user_token,id):
    car = Car.query.get(id)
    response = car_schema.dump(car)
    return jsonify(response)

#Update car
@api.route('/cars/<id>',methods=["POST", "PUT"])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)
    car.make = request.json['make']
    car.model = request.json['model']
    car.year = request.json['year']
    car.color = request.json['color']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

#Delete car
@api.route('/cars/<id>',methods=["DELETE"])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)