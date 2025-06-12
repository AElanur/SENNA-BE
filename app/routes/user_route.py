from flask import request, Blueprint, jsonify


def create_user_blueprint(user_service):
    user_bp = Blueprint('user', __name__)

    @user_bp.route("/user", methods=["POST"])
    def create_user():
        user_data = request.get_json()
        user_id = user_service.create_user(user_data)
        return jsonify(user_id)


    return user_bp

