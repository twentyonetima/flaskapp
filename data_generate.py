import random
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from src.database import engine
from src.models import Category, Product, Sale


def generate_sales(product_id):
    today = datetime.now()
    sales = []
    for i in range(6):
        sale_date = today - timedelta(days=random.randint(0, 30))
        sale_amount = random.randint(1, 20)
        sales.append(Sale(product_id=product_id, amount=sale_amount, date=sale_date))
    return sales


def init_data():
    Session = sessionmaker(bind=engine)
    session = Session()

    if session.query(Category).first():
        print("⚠️ Данные уже существуют, пропускаем генерацию.")
        return

    categories = ['Electronics', 'Clothing', 'Books']
    category_objs = [Category(name=cat) for cat in categories]

    session.add_all(category_objs)
    session.commit()

    products_data = {
        'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Smartwatch', 'Headphones'],
        'Clothing': ['T-shirt', 'Jeans', 'Jacket', 'Sweater', 'Shirt'],
        'Books': ['Novel', 'Magazine', 'E-book', 'Biography', 'Textbook']
    }

    for category_name, product_names in products_data.items():
        category = session.query(Category).filter_by(name=category_name).first()
        for product_name in product_names:
            product = Product(name=product_name, category_id=category.id)
            session.add(product)
            session.commit()

            sales = generate_sales(product.id)
            session.add_all(sales)

    session.commit()


if __name__ == "__main__":
    init_data()