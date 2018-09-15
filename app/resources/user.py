from flask import Flask, jsonify
from flask_restful import Resource, reqparse
import re

from app.models import User, is_blank


class Signup(Resource):
    """
    SignUp new User
    parse user details
    """
    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True,
                        help='Please imput the username', type=str)
    parser.add_argument('email', required=True,
                        help='Please input the email', type=str)
    parser.add_argument('password', required=True,
                        help='Please imput the password', type=str)

    def post(self):
        """ Registering new user """
        args = Signup.parser.parse_args()
        password = args.get('password')
        username = args.get('username')
        email = args.get('email')

        email_format = re.compile(
            r"(^[a-zA-Z0-9_.-]+@[a-zA-Z-]+\.[a-zA-Z-]+$)")
        username_format = re.compile(r"(^[A-Za-z]+$)")

        if not (re.match(username_format, username)):
            return jsonify({'message': 'Invalid username'}), 400
        elif not (re.match(email_format, email)):
            return jsonify({'message': 'Invalid email. Ensure email is of the form example@mail.com'}), 400
        if len(username) < 4:
            return ({'message': 'Username should be atleast 4 characters'}), 400
        if is_blank(password) or is_blank(username) or is_blank(email):
            return jsonify({'message': 'All fields are required'}), 400
        if len(password) < 8:
            return jsonify({'message': 'Password should be atleast 8 characters'}), 400

        username_exists = User.get_user_by_username(username=args['username'])
        email_exists = User.get_user_by_email(email=args['email'])

        if username_exists or email_exists:
            return {'message': 'User already exists'}, 203

        user = User(username=args.get('username'),
                    email=args.get('email'), password=password)
        user = user.save()

        return jsonify({'message': 'registration successful, now login', 'user': user}), 201


class Login(Resource):
    """ User Log In """
    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True,
                        help='Username cannot be blank', type=str)
    parser.add_argument('password', required=True,
                        help='Password cannot be blank')

    def post(self):
        """ Log In method """
        args = Login.parser.parse_args()
        username = args["username"]
        password = args["password"]
        if is_blank(username) or is_blank(password) == '':
            return jsonify({'message': 'All fields are required'}), 400

        user = User.get_user_by_username(username)
        if not user:
            return {'message': 'User unavailable'}, 404
        if user.validate_password(password):
            return jsonify({"message": "You are successfully logged in", 'user': user.view()}), 200
        return jsonify({"message": "Username or password is wrong."}), 401