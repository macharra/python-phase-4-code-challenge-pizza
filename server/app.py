#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response,jsonify
from flask_restful import Api, Resource


import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)





@app.route('/')
def index():
    body = {'message': 'Challenge'}
    return make_response(body)

@app.route('/restaurants', methods=['GET'])
def restaurants():
    
    restaurants = Restaurant.query.all()
    body = [restaurant.to_dict() for restaurant in restaurants]
    return jsonify(body), 200
@app.route('/restaurants/<int:id>',methods=['GET'])
def get_restaurant_by_id(id):
    restaurant = Restaurant.query.filter_by(id=id).first()
    if restaurant is None:
        return jsonify({"error":"Restaurant not found"}), 404
    else:
        body = restaurant.to_dict()
        return jsonify(body), 200
       


@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = db.session.get(Restaurant, id)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204
    else:
        body = {'message': f'Restaurant {id} not found.'}
    return jsonify(body), 404
@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([p.to_dict(only=('id', 'name', 'ingredients')) for p in pizzas]),200


@app.route('/restaurants/<int:restaurant_id>/pizzas', methods=['POST'])
def create_restaurant_pizza(restaurant_id):
    restaurant = Restaurant.query.filter_by(id=restaurant_id).first()
    if restaurant:
        pizza_name = request.json.get('name')
        pizza_ingredients = request.json.get('ingredients')
        pizza = Pizza(name=pizza_name, ingredients=pizza_ingredients)
        db.session.add(pizza)
        db.session.commit()
        restaurant_pizza = RestaurantPizza(restaurant=restaurant, pizza=pizza, price=0)
        db.session.add(restaurant_pizza)
        db.session.commit()
        body = {'message': f'Pizza {pizza_name} added to restaurant {restaurant.name}.'}
        status = 201
    else:
        body = {'message': f'Restaurant {restaurant_id} not found.'}
        status = 404
    return jsonify(body), status



if __name__ == "__main__":
    app.run(port=5555, debug=True)