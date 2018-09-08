# Data Structures to store 

from datetime import datetime
from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash

class DB():
    """ This class  creates a data structure to store user data in place of a database"""
    def __init__(self):
        self.users = {}
        self.user_count = 0

    def drop(self):
        self.__init__()

""" An instance of the class """
db = DB()

class Start():
    """ Start class to be inherited by User Class"""
    def update(self, data):
        # Validate keys before passing to data.
        for key in data:
            setattr(self, key, data[key])
        setattr(self, 'last_modified', datetime.utcnow().isoformat())
        return self.view()

class User(Start):
    """ This class defines the user data model """
    def __init__(self, username, password, email):
        self.id = None
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email
        self.created_at = datetime.utcnow().isoformat()
        self.last_modified = datetime.utcnow().isoformat()

    def save(self):
        """ Method for saving user registration details """
        setattr(self, 'id', db.user_count + 1)
        db.users.update({self.id: self})
        db.user_count += 1
        return self.view()

    def validate_password(self, password):
        """ Method for validating user password """
        if check_password_hash(self.password, password):
            return True
        return False

    def delete(self):
        """ Method used for deleting a user """
        del db.users[self.id]


    def view(self):
        """ Method to jsonify object user to return a file in json format """
        keys = ['username', 'email', 'id']
        return {key: getattr(self, key) for key in keys}

    @classmethod
    def get_user_by_email(cls, email):
        """ email """
        for id_ in db.users:
            user = db.users.get(id_)
            if user.email == email:
                return user
        return None

    @classmethod
    def get(cls, id):
        """ Id """
        user = db.users.get(id)
        if not user:
            return {'message': 'Invalid Logins.'}
        return user



    @classmethod
    def get_user_by_username(cls, username):
        """ Username """
        for id_ in db.users:
            user = db.users.get(id_)
            if user.username == username:
                return user
        return None

def is_blank(var):
    '''function to check if any required field is blank and notifies user if its so'''
    if var.strip() == '':
        return 'All fields are required'
    return None



orders = [

    {
        "order_id": 1,
        "name": "Vincent Muriuki",
        "type": "Chicken Curry",
        "price": 500.00,
        "address": "Ngong"
    },

    {
        "order_id": 2,
        "name": "Kate Chege",
        "type": "Pizza",
        "price": 800.00,
        "address": "Westlands"
    }

]