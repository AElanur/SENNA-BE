from flask import request, Blueprint, jsonify


def create_chat_blueprint(chat_service):
    chat_bp = Blueprint('chat', __name__)

    @chat_bp.route("/chat", methods=["POST"])
    def create_chat():
        chat_data = request.get_json()
        return jsonify(chat_service.create_chat(chat_data))
    return chat_bp