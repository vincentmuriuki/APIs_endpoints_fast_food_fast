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

