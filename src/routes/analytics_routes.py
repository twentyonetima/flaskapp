import json
from flask import Blueprint, request, jsonify, Response
from src.services.analytics_service import get_total_sales, get_top_products
from src.cache import redis_client
from src.utils.date_parser import parse_date

analytics_bp = Blueprint('analytics', __name__, url_prefix="/api")


@analytics_bp.route('/sales/total')
def total_sales():
    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")
    if not start_date_str or not end_date_str:
        return jsonify({"error": "start_date and end_date required"}), 400

    start_date = parse_date(start_date_str)
    end_date = parse_date(end_date_str)

    if not start_date or not end_date:
        return jsonify({"error": "Invalid date format. Use MM.DD.YYYY"}), 400

    cache_key = f"total_sales:{start_date}:{end_date}"
    cached = redis_client.get(cache_key)
    if cached:
        return jsonify({"total_sales": int(cached)}), 200

    total = get_total_sales(start_date, end_date)
    redis_client.setex(cache_key, 300, total)
    return jsonify({"total_sales": total})


@analytics_bp.route('/sales/top-products')
def top_products():
    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")
    limit = int(request.args.get("limit", 5))
    if not start_date_str or not end_date_str:
        return jsonify({"error": "start_date and end_date required"}), 400

    start_date = parse_date(start_date_str)
    end_date = parse_date(end_date_str)

    if not start_date or not end_date:
        return jsonify({"error": "Invalid date format. Use MM.DD.YYYY"}), 400

    cache_key = f"top_products:{start_date}:{end_date}:{limit}"
    cached = redis_client.get(cache_key)
    if cached:
        return Response(cached, content_type="application/json", status=200)

    top = get_top_products(start_date, end_date, limit)
    json_data = json.dumps({"top_products": top})
    redis_client.setex(cache_key, 300, json_data)
    return Response(json_data, content_type="application/json", status=200)