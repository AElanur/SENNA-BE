from flask import request, Blueprint

from app.auth.decorater import login_required


def create_message_blueprint(message_service):
    message_bp = Blueprint('message', __name__)

    @message_bp.route("/chats/<int:chat_id>/get-messages", methods=["GET"])
    @login_required
    def get_messages(user_id, chat_id) -> list[dict]:
        return message_service.get_messages(chat_id)

    @message_bp.route("/chats/<int:chat_id>/send-message", methods=["POST"])
    @login_required
    def send_message(user_id, chat_id):
        data = request.get_json()
        return message_service.send_message(user_id, chat_id, data)

    return message_bp