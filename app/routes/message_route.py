from flask import request, Blueprint

def create_message_blueprint(message_service):
    message_bp = Blueprint('message', __name__)

    @message_bp.route("/get-messages/<int:chat_id>", methods=["GET"])
    def get_messages(chat_id) -> list[dict]:
        return message_service.get_messages(chat_id)

    @message_bp.route("/send-message", methods=["POST"])
    def send_message() -> str:
        user_message = request.get_json()
        return message_service.send_message(user_message["content"])

    @message_bp.route("/edit-message/<int:message_id>", methods=["PUT"])
    def edit_message():
        message_id = request.get_json()
        return message_service.update_message()

    @message_bp.route("/delete-message/<int:message_id>", methods=["DELETE"])
    def delete_message():
        message_id = request
        return message_service.delete_message()

    return message_bp