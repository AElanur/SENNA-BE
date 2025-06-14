from flask import request, Blueprint, jsonify

from app.auth.decorater import login_required


def create_chat_blueprint(chat_service):
    chat_bp = Blueprint('chat', __name__)

    @chat_bp.route("/chat", methods=["POST"])
    @login_required
    def create_chat(user_id):
        chat_data = request.get_json()
        return jsonify(chat_service.create_chat(chat_data))

    @chat_bp.route("/chat/<int:chat_id>/participants", methods=["GET"])
    @login_required
    def get_chat_participants(user_id, chat_id):
        return jsonify(chat_service.get_chat_participants(chat_id))

    return chat_bp

