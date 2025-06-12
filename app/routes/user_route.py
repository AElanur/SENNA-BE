from flask import request, Blueprint, jsonify


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

    return user_bp

