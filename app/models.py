# Data Structures to store orders and user data

from datetime import datetime
from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash

class Order():
    def __init__(self):
        self.users = {}
        self.user_count = 0

    def drop(self):
        self.__init__()


db = Order()

class Start():
    def update(self, data):
        for key in data:
            setattr(self, key, data[key])
        setattr(self, 'last_modified', datetime.utcnow().isoformat())
        return self.view()

class User(Start):
    def __init__(self, username, password, email):
        self.id = None
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email
        self.created_at = datetime.utcnow().isoformat()
        self.last_modified = datetime.utcnow().isoformat()

    def save(self):
        setattr(self, 'id', db.user_count + 1)
        db.users.update({self.id: self})
        db.user_count += 1
        return self.view()

    def validate_password(self, password):
        if check_password_hash(self.password, password):
            return True
        return False

    def view(self):
        keys = ['username', 'email', 'id']
        return {key: getattr(self, key) for key in keys}

    def delete(self):
        del db.users[self.id]

    @classmethod
    def get_user_by_email(cls, email):
        for id_ in db.users:
            user = db.users.get(id_)
            if user.email == email:
                return user
        return None

    @classmethod
    def get(cls, id):
        user = db.users.get(id)
        if not user:
            return {'message': 'Invalid Login Credentials!'}
        return user

    @classmethod
    def get_user_by_username(cls, username):
        for id_ in db.users:
            user = db.users.get(id_)
            if user.username == username:
                return user
        return None

def is_blank(var):
    if var.strip() == '':
        return 'All fields are required. Do not leave any field blank!'
    return None



orders = [

    {
        "order_id": 1,
        "name": "Vincent Muriuki",
        "type": "Chicken Curry",
        "price": 500.00,
        "address": "Karen"
    },

    {
        "order_id": 2,
        "name": "Kate Chege",
        "type": "Pizza",
        "price": 800.00,
        "address": "Westlands"
    }

]