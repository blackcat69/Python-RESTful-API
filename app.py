# a simple Flask RESTful app
# Flask RESTful does jasonify automatically
# to setup env
# virtualenv venv --python=python3.7
# source venv/bin/activate
# deactivate to close the venv

import os

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

# from security import authenticate, identity
from resources.user import UserRegister, User, UserLogin
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
# Heroku db env variable or sqlite for local backup
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db') 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'daren_cox_69'		# app.config['JWT_SECRET_KEY']
api = Api(app)

# jwt = JWT(app, authenticate, identity)  # creates endpoint /auth
jwt = JWTManager(app)  # does not create an endpoint

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
	if identity == 1:  # instead of hard-coding this, you should read from a config file
		return {'is_admin": True'}
	return {'is_admin": False'}

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')	
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':
	from db import db
	db.init_app(app)
#	app.run(port=5000, debug=True)
	app.run(port=5000)


