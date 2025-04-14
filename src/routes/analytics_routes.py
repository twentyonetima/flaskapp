from flask import Blueprint, request, jsonify
from src.services.analytics_service import get_total_sales, get_top_products

analytics_bp = Blueprint('analytics', __name__, url_prefix="/api")


@analytics_bp.route('/sales/total')
def total_sales():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    if not start_date or not end_date:
        return jsonify({"error": "start_date and end_date required"}), 400
    total = get_total_sales(start_date, end_date)
    return jsonify({"total_sales": total})


@analytics_bp.route('/sales/top-products')
def top_products():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    limit = int(request.args.get("limit", 5))
    if not start_date or not end_date:
        return jsonify({"error": "start_date and end_date required"}), 400
    top = get_top_products(start_date, end_date, limit)
    return jsonify({"top_products": top})