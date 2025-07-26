from flask import Blueprint, jsonify, request
from models import db, Product
from flask_login import current_user, login_required

api = Blueprint('api', __name__)

cart = {}

@api.route('/api/cart', methods=['GET', 'POST'])
@login_required
def api_cart():
    user_id = str(current_user.id)
    if request.method == 'POST':
        data = request.get_json()
        product_id = str(data.get('product_id'))
        cart.setdefault(user_id, []).append(product_id)
        return jsonify({"message": "Item added to cart"}), 200
    return jsonify({"cart": cart.get(user_id, [])})

@api.route('/api/checkout', methods=['POST'])
@login_required
def api_checkout():
    user_id = str(current_user.id)
    cart[user_id] = []
    return jsonify({"message": "Checkout successful"}), 200
