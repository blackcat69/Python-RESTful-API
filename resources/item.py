from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('price',
		type=float,
		required=True,
		help="This field cannot be left blank."
	)
	parser.add_argument('store_id',
		type=int,
		required=True,
		help="Every item must have a store id."
	)

	@jwt_required()	# add this decorator to any method you want authorised via the session token
	def get(self, name):
		try:
			item = ItemModel.find_by_name(name)
		except:
			return {"message": "An error occurred trying to get the item"}, 500
		if item:
			return item.json()
		return {"message": "Item not found."}, 404
		
	def post(self, name):

		if ItemModel.find_by_name(name):
			return {'message': "An item with name '{}' already exists.".format(name)}, 400		

		data = Item.parser.parse_args()

		item = ItemModel(name, **data)

		try:
			item.save_to_db()
		except:  # 500 status code is an internal server error 
			return {"message": "An error occurred trying to insert the item."}, 500

		return item.json(), 201		# 201 is CREATED http status code
					
	def delete(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()
		
		return {'message': 'Item deleted'}
	
	def put(self, name):
		data = Item.parser.parse_args()
		
		item = ItemModel.find_by_name(name)
				
		if item is None:
			item = ItemModel(name, **data)
		else:
			item.price = data['price']

		try:
			item.save_to_db()
		except:  # 500 status code is an internal server error 
			return {"message": "An error occurred trying to update the item."}, 500

		return item.json()
		
		
class ItemList(Resource):
	def get(self):
		return {'items': [item.json() for item in ItemModel.query.all()]}		
		
		