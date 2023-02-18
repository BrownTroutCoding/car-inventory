# create an extra function to check tokens for rightful access to data, and create an encoder for our JSON content.
from functools import wraps
import secrets
from flask import request, jsonify, json
import decimal

from models import User

# checking to see if 'x-access-token' is in our headers for our API calls - we will see what this looks like when 
# we start actually digging in and posting and getting data
def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split(' ')[1]
        if not token:
            return jsonify({'message': 'Token is missing.'}), 401

        try:
            current_user_token = User.query.filter_by(token = token).first()
            print(token)
            print(current_user_token)
        except:
            owner=User.query.filter_by(token=token).first()

            if token != owner.token and secrets.compare_digest(token, owner.token):
                return jsonify({'message': 'Token is invalid'})
        return our_flask_function(current_user_token, *args, **kwargs)
    return decorated

# This checks that the instances of json are decimals, and then changes them into strings that we can use later.
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder,self).default(obj)