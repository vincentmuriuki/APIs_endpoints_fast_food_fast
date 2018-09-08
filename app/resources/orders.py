from flask import Flask, request
from flask_restful import Resource, reqparse


from app.models import orders


class Orders(Resource):
    """ Method to retrieve all orders """

    def get(self):
        return {'orders': orders}, 200


class Order(Resource):

    """ Create Request parsing interface for price """

    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="Please fill out this field"
    )
    parser.add_argument(
        'type',
        type=str,
        required=True,
        help="Please fill out this field"
    )
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="Please fill out this field"
    )
    parser.add_argument(
        'address',
        type=str,
        required=True,
        help="Please fill out this field"
    )

    """ GET a specific Order method """

    def get(self, order_id):
        order = next(filter(lambda x: x['order_id'] == order_id, orders), None)
        return {'order': order}, 200 if order else 404

    """ (POST) Place a new Order method """

    def post(self, order_id):
        if next(filter(lambda x: x['order_id'] == order_id, orders), None):
            return {'message': "The order '{}' already exists.".format(order_id)}, 400

        data = Order.parser.parse_args()

        order = {
            'order_id': order_id,
            'name': data['name'],
            'type': data['type'],
            'price': data['price'],
            'address': data['address']
        }
        orders.append(order)
        return order, 201

    """ Function to update the status of a specific order method """

    def put(self, order_id):

        data = Order.parser.parse_args()

        order = next(filter(lambda x: x['order_id'] == order_id, orders), None)
        if order is None:
            order = {
                'order_id': order_id,
                'name': data['name'],
                'type': data['type'],
                'price': data['price'],
                'address': data['address']
            }
            orders.append(order), 201
        else:
            order.update(data), 200
        return order

    """ Function to delete a specific from the orders list """

    def delete(self, order_id):
        global orders
        orders = list(filter(lambda x: x['order_id'] != order_id, orders))
        return {'message': 'Order deleted'}, 200