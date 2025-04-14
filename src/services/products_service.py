from src.models import Product, Category
from src.database import db_session
from src.cache import redis_client
from src.schemas import ProductResponseSchema

def get_all_products():
    return Product.query.all()

def create_product(name, category_name):
    category = Category.query.filter_by(name=category_name).first()
    if not category:
        category = Category(name=category_name)
        db_session.add(category)
        db_session.commit()
    product = Product(name=name, category=category)
    db_session.add(product)
    db_session.commit()
    return product

def update_product(product, data):
    if data.get('name') is not None:
        product.name = data['name']

    if data.get('category') is not None:
        category = Category.query.filter_by(name=data['category']).first()
        if not category:
            category = Category(name=data['category'])
            db_session.add(category)
            db_session.commit()
        product.category = category

    db_session.commit()
    return product

def delete_product(product):
    db_session.delete(product)
    db_session.commit()

def refresh_products_cache():
    products = Product.query.all()
    response = [
        ProductResponseSchema(id=p.id, name=p.name, category=p.category.name)
        for p in products
    ]
    json_data = "[" + ",".join(p.model_dump_json() for p in response) + "]"
    redis_client.setex("all_products", 300, json_data)