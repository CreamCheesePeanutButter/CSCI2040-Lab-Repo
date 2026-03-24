from flask import request, Blueprint, jsonify, session
from flask.views import MethodView
from db import get_db
from tracker.user import User
from datetime import datetime

user_bp = Blueprint('user_api', __name__)

class UserAPI(MethodView):

        def get(self, user_id):
            db = get_db()

            cursor = db.cursor(dictionary=True)

            cursor.execute("SELECT * FROM user WHERE userID = %s", (user_id,))

            users = cursor.fetchall() #store all user data
            cursor.close()
            print(users)
            return jsonify({
                "users": [
                    {
                        "id": user['userID'],
                        "email": user['email'],
                        "first_name": user['first_name'],
                        "last_name": user['last_name'],
                        "username": user['username'],
                        "available_funds": user['available_funds']
                    } for user in users
                ]
            }), 200

user_view = UserAPI.as_view('user_api')
# this piece of code is for getting user information.

user_bp.add_url_rule(
    '/user/<int:user_id>/info',
    view_func=user_view,
    methods=['GET']
)
### Example of the what the API will return
# {
#   "users": [
#     {
#       "available_funds": 0.0,
#       "email": "jdoe@example.com",
#       "first_name": "John",
#       "id": 1,
#       "last_name": "Doe",
#       "username": "jdoe"
#     }
#   ]
# }
####

#####################ADD FUNDS API#####################
class UserFundsAPI(MethodView):

    def post(self, user_id):
        data = request.get_json()
        amount = data.get('amount')

        if amount is None:
            return jsonify({"message": "Missing amount"}), 400

        db = get_db()
        cursor = db.cursor()

        cursor.execute("UPDATE user SET available_funds = available_funds + %s WHERE userID = %s", (amount, user_id))
        db.commit()
        cursor.close()

        return jsonify({"message": "Funds added successfully"}), 200
    
user_funds_view = UserFundsAPI.as_view('user_funds_api')
user_bp.add_url_rule(
    '/user/<int:user_id>/add-funds',
    view_func=user_funds_view,
    methods=['POST']
)

###########################Buy stock 


class BuyTradeAPI(MethodView):

    def post(self, user_id):

        data = request.get_json()

        num_share = data.get("num_share")
        stock_key = data.get("stock_key")

        if not num_share or not stock_key:
            return jsonify({"message": "Missing data"}), 400

        db = get_db()
        cursor = db.cursor(dictionary=True)

        # get stock price
        cursor.execute(
            "SELECT current_price FROM stock WHERE stock_key = %s",
            (stock_key,)
        )

        stock = cursor.fetchone()

        if not stock:
            return jsonify({"message": "Stock not found"}), 404

        price = stock["current_price"]
        total_cost = price * num_share

        # get user funds
        cursor.execute(
            "SELECT available_funds FROM user WHERE userID = %s",
            (user_id,)
        )

        user_data = cursor.fetchone()

        if not user_data:
            return jsonify({"message": "User not found"}), 404

        if user_data["available_funds"] < total_cost:
            return jsonify({"message": "Not enough funds"}), 400

        # deduct funds
        cursor.execute(
            "UPDATE user SET available_funds = available_funds - %s WHERE userID = %s",
            (total_cost, user_id)
        )

        # store trade
        cursor.execute(
            """
            INSERT INTO TradeTable (userID, stock_symbol, price, number_of_shares, transaction_date, transaction_type)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (user_id, stock_key, price, num_share, datetime.now(), "BUY")
        )

        db.commit()
        cursor.close()

        return jsonify({
            "message": "Stock purchased",
            "price": price,
            "shares": num_share,
            "total_cost": total_cost
        }), 200
    
user_buy_view = BuyTradeAPI.as_view('buy_stock_api')
user_bp.add_url_rule(
    '/user/<int:user_id>/buy',
    view_func=user_buy_view,
    methods=['POST']
)
    

class SellTradeAPI(MethodView):

    def post(self, user_id):

        data = request.get_json()

        num_share = data.get("num_share")
        stock_key = data.get("stock_key")

        if not num_share or not stock_key:
            return jsonify({"message": "Missing data"}), 400

        db = get_db()
        cursor = db.cursor(dictionary=True)

        # check how many shares user owns
        cursor.execute(
            """
            SELECT SUM(number_of_shares) as total_shares
            FROM TradeTable
            WHERE userID = %s AND stock_symbol = %s
            """,
            (user_id, stock_key)
        )

        result = cursor.fetchone()

        owned_shares = result["total_shares"] if result["total_shares"] else 0

        if owned_shares < num_share:
            return jsonify({
                "message": "Not enough shares to sell",
                "owned_shares": owned_shares
            }), 400

        # get current stock price
        cursor.execute(
            "SELECT current_price FROM stock WHERE stock_key = %s",
            (stock_key,)
        )

        stock = cursor.fetchone()

        if not stock:
            return jsonify({"message": "Stock not found"}), 404

        price = stock["current_price"]

        total_value = price * num_share

        # add funds back to user
        cursor.execute(
            """
            UPDATE user
            SET available_funds = available_funds + %s
            WHERE userID = %s
            """,
            (total_value, user_id)
        )

        # record sell trade (negative quantity)
        cursor.execute(
            """
            INSERT INTO TradeTable (userID, stock_symbol, price, number_of_shares, transaction_date, transaction_type)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (user_id, stock_key, price, -num_share, datetime.now(), "SELL")
        )

        db.commit()
        cursor.close()

        return jsonify({
            "message": "Stock sold",
            "price": price,
            "shares_sold": num_share,
            "total_value": total_value,
            "remaining_shares": owned_shares - num_share
        }), 200
    
user_sell_view = SellTradeAPI.as_view('sell_stock_api')
user_bp.add_url_rule(
    '/user/<int:user_id>/sell',
    view_func=user_sell_view,
    methods=['POST']
)
