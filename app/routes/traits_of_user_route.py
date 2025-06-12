from flask import Blueprint

def create_traits_of_user_blueprint(traits_of_user_service):
    traits_of_user_bp = Blueprint('trait', __name__)

    @traits_of_user_bp.route("/user/<int:user_id>", methods=["GET"])
    def get_traits_of_user(user_id) -> list[dict]:
        return traits_of_user_service.get_traits_of_user(user_id)

    return traits_of_user_bp