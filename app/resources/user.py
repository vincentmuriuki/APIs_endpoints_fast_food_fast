from flask import Flask, make_response
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
       """ Registering new user """
    def post(self):
        args = Signup.parser.parse_args()
        password = args.get('password')
        username = args.get('username')
        email = args.get('email')
        email_format = re.compile(
            r"(^[a-zA-Z0-9_.-]+@[a-zA-Z-]+\.[a-zA-Z-]+$)")
        username_format = re.compile(r"(^[A-Za-z]+$)")
        if not (re.match(username_format, username)):
            # return make_response('message': 'Invalid username'), 400
            return make_response('Username not recgnized! Please Try again!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required!"'})

        elif not (re.match(email_format, email)):
            return make_response{'message': 'Invalid email. Ensure email is of the form example@mail.com'}, 400
        if is_blank(password) or is_blank(username) or is_blank(email):
            # return 'message': 'All fields are required'}, 400
            return make_response('All fields are required! Please Try again!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required!"'})

        username_exists = User.get_user_by_username(username=args['username'])
        email_exists = User.get_user_by_email(email=args['email'])
        if username_exists or email_exists:
            # return {'message': 'User already exists'}, 203
            return make_response('User already exists in the database! Please Try a different username!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required!"'})



        user = User(username=args.get('username'),
                    email=args.get('email'), password=password)
        user = user.save()

        return {'message': 'registration successful, now login', 'user': user}, 201


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
            return {'message': 'All fields are required'}, 400

        user = User.get_user_by_username(username)
        if not user:
            return {'message': 'User unavailable'}, 404
        if user.validate_password(password):
            return {"message": "You are successfully logged in", 'user': user.view()}, 200
        return {"message": "Username or password is wrong."}, 401