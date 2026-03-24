from flask import request, Blueprint, jsonify
from flask.views import MethodView
from db import get_db

test_bp = Blueprint("test_api", __name__)

# WRONG username update
class ChangeUsernameAPI(MethodView):

    def post(self, user_id):

        data = request.get_json()

        username = data.get("username")

        db = get_db()
        cursor = db.cursor()

        # ❌ wrong column name (user_name instead of username)
        cursor.execute(
            """
            UPDATE test_user
            SET user_name = %s
            WHERE id = %s
            """,
            (user_id, username) # ❌ wrong order
        )

        # ❌ forgot db.commit()

        cursor.close()

        return jsonify({"message": "username updated"}), 200


# WRONG password update
class ChangePasswordAPI(MethodView):

    def post(self, user_id):

        data = request.get_json()

        password = data.get("password")

        db = get_db()
        cursor = db.cursor()

        # ❌ missing WHERE clause (updates ALL users)
        cursor.execute(
            """
            UPDATE test_user
            SET password = %s
            """,
            (password,)
        )

        db.commit()

        cursor.close()

        return jsonify({"message": "password updated"}), 200


username_view = ChangeUsernameAPI.as_view("change_username_api")
password_view = ChangePasswordAPI.as_view("change_password_api")


test_bp.add_url_rule(
    "/user/<int:user_id>/username",
    view_func=username_view,
    methods=["POST"]
)

test_bp.add_url_rule(
    "/user/<int:user_id>/password",
    view_func=password_view,
    methods=["POST"]
)