from flask import request, Blueprint, jsonify
from app.auth.decorater import login_required


def create_user_blueprint(user_service):
    user_bp = Blueprint('user', __name__)

    @user_bp.route("/user", methods=["POST"])
    def create_user():
        user_data = request.get_json()
        response = user_service.create_user(user_data)
        return jsonify(response)

    @user_bp.route("/user/login", methods=["POST"])
    def login_user():
        user_data = request.get_json()
        response = user_service.login_user(user_data)
        return jsonify(response)

    @user_bp.route("/user/logout", methods=["POST"])
    @login_required
    def logout_user(user_id):
        response = user_service.logout_user(user_id)
        return jsonify(response)

    return user_bp


