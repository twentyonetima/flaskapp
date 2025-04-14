from flask import Blueprint, jsonify, request
from .models import Product
from .crud import get_all_products, create_product, update_product, delete_product

bp = Blueprint("routes", __name__, url_prefix="/api")

@bp.route("/products", methods=["GET"])
def get_products():
    products = get_all_products()
    return jsonify([{
        "id": p.id,
        "name": p.name,
        "category": p.category.name
    } for p in products]), 200

@bp.route("/products", methods=["POST"])
def create_product_route():
    data = request.json
    product = create_product(data["name"], data["category"])
    return jsonify({
        "id": product.id,
        "name": product.name,
        "category": product.category.name
    }), 201

@bp.route("/products/<int:id>", methods=["PUT"])
def update_product_route(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({"message": "Product not found"}), 404

    updated = update_product(product, request.json)
    return jsonify({
        "id": updated.id,
        "name": updated.name,
        "category": updated.category.name
    }), 200

@bp.route("/products/<int:id>", methods=["DELETE"])
def delete_product_route(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({"message": "Product not found"}), 404

    delete_product(product)
    return jsonify({"message": "Deleted"}), 200