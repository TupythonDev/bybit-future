from flask import Blueprint, make_response, request
from app.helpers.services import get_usdt_balance, get_symbol_price, place_order_tp_sl, set_leverage
from app.config import session

routes = Blueprint("routes", __name__)

@routes.route("/home", methods=["GET"])
def home():
    return "Hello, World!"

@routes.route("/balance", methods=["GET"])
def balance():
    res = make_response({"balance":get_usdt_balance(session)})
    return res

@routes.route("/price_cripto", methods=["GET"])
def get_price():
    category = request.args.get("category")
    symbol = request.args.get("symbol")
    return make_response({"price":get_symbol_price(category, symbol, session)})

@routes.route("/place_order", methods=["POST"])
def place_order():
    order = request.json
    return make_response(
        place_order_tp_sl(session, order)
    )

@routes.route("/switch_mode", methods=["POST"])
def switch_mode():
    pass

@routes.route("/set_leverage", methods=["POST"])
def place_leverage():
    leverage = request.json["leverage"]
    category = request.json["category"]
    symbol = request.json["symbol"]
    return make_response(
        set_leverage(leverage["buy"], leverage["sell"], category, symbol, session)
    )
