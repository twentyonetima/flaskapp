from sqlalchemy import func
from src.database import db_session
from src.models import Sale, Product


def get_total_sales(start_date, end_date):
    total = db_session.query(
        func.sum(Sale.amount)
    ).filter(
        Sale.date >= start_date,
        Sale.date <= end_date
    ).scalar()
    return total or 0


def get_top_products(start_date, end_date, limit):
    result = db_session.query(
        Product.name,
        func.sum(Sale.amount).label("total_amount")
    ).join(Sale).filter(
        Sale.date >= start_date,
        Sale.date <= end_date
    ).group_by(Product.id).order_by(
        func.sum(Sale.amount).desc()
    ).limit(limit).all()

    return [{"product": i[0], "total_amount": i[1]} for i in result]