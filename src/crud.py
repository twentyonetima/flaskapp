from src.models import Product, Category
from src.database import db_session

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

    if 'name' in data:
        product.name = data['name']

    if 'category' in data:
        category = Category.query.filter_by(name=data['category']).first()
        if not category:
            category = Category(name=data['category'])
            db_session.add(category)

        product.category = category

    db_session.commit()
    return product

def delete_product(product):
    db_session.delete(product)
    db_session.commit()