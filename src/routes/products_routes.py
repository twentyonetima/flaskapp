import logging
import json
from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from src.models import Product
from src.services.products_service import get_all_products, create_product, update_product, delete_product, refresh_products_cache
from src.schemas import ProductResponseSchema, ProductCreateSchema, ProductUpdateSchema
from src.cache import redis_client

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

product_bp = Blueprint("products", __name__, url_prefix="/api")


def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            logger.error(f"Error during {request.method} {request.path}: {str(e)}")
            return jsonify({"error": e.errors()}), 400
        except Exception as e:
            logger.error(f"Error during {request.method} {request.path}: {str(e)}")
            return jsonify({"error": str(e)}), 500
    wrapper.__name__ = func.__name__
    return wrapper

@product_bp.route("/products", methods=["GET"])
@handle_exceptions
def get_products():
    cache_key = "all_products"
    cached = redis_client.get(cache_key)

    if cached:
        products = json.loads(cached)
        return jsonify(products), 200

    products = get_all_products()
    response = [
        ProductResponseSchema(id=p.id, name=p.name, category=p.category.name).model_dump()
        for p in products
    ]

    redis_client.setex(cache_key, 300, json.dumps(response))
    return jsonify(response), 200

@product_bp.route("/products", methods=["POST"])
@handle_exceptions
def create_product_route():
    if not request.json:
        return jsonify({"error": "No data provided"}), 400

    data = ProductCreateSchema(**request.json)
    product = create_product(name=data.name, category_name=data.category)
    refresh_products_cache()
    return jsonify({
        "id": product.id,
        "name": product.name,
        "category": product.category.name
    }), 201

@product_bp.route("/products/<int:id>", methods=["PUT"])
@handle_exceptions
def update_product_route(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    data = ProductUpdateSchema(**request.json)
    updated = update_product(product, data.model_dump())
    refresh_products_cache()
    return jsonify({
        "id": updated.id,
        "name": updated.name,
        "category": updated.category.name
    }), 200

@product_bp.route("/products/<int:id>", methods=["DELETE"])
@handle_exceptions
def delete_product_route(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    delete_product(product)
    refresh_products_cache()
    return jsonify({"message": "Deleted"}), 200