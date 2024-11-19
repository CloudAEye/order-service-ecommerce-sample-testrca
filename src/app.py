from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import requests

from src.config import PRODUCT_SERVICE_URL
from src.models import db
from src.service import OrderService

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)

jwt = JWTManager(app)


@app.before_request
def create_tables():
    # The following line will remove this handler, making it
    # only run on the first request
    app.before_request_funcs[None].remove(create_tables)
    db.create_all()


@app.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    try:
        user_id = get_jwt_identity()
        data = request.json
        product_id = data['product_id']
        quantity = data['quantity']

        # Get the JWT token from the current request
        access_token = request.headers.get('Authorization').split(' ')[1]

        headers = {'Authorization': f'Bearer {access_token}'}
        product_response = requests.get(f'{PRODUCT_SERVICE_URL}/products/{product_id}', headers=headers)

        # Check if the product exists and has enough stock
        if product_response.status_code != 200:
            return jsonify(product_response.json()), product_response.status_code
        # Check if stock available => if not throw error about insufficient stock
        product = product_response.json()
        if product['quantity'] < quantity:
            return jsonify({'message': 'Insufficient stock'}), 400

        # Create new order
        new_order = OrderService().create_order(user_id=user_id, product_id=product_id, quantity=quantity)

        # Update the product stock on product service
        updated_stock = product['quantity'] - quantity
        product_update_response = requests.put(f'{PRODUCT_SERVICE_URL}/products/{product_id}', json={'quantity': updated_stock}, headers=headers)
        if product_update_response.status_code != 200:
            return jsonify({'message': 'Failed to update product quantity'}), product_update_response.status_code

        # Return response
        return jsonify({'id': new_order.id, 'status': new_order.status}), 201
    except Exception as e:
        return jsonify({'message': e}), 400


@app.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    try:
        user_id = get_jwt_identity()
        # List all orders placed by the user
        result = OrderService().get_all_orders(user_id=user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': e}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5002)
