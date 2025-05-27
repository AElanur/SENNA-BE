from flask import request
from . import message_bp
from service.message_service import MessageService

message_service = MessageService()

@message_bp.route("/send-message", methods=["POST"])
def send_message() -> str:
    content = request.get_json()
    return message_service.send_message()

@message_bp.route("/edit-message/<int:message_id>", method=["PUT"])
def edit_message():
    message_id = request.get_json()
    return message_service.update_message()

@message_bp.route("/delete-message/<int:message_id>", method=["DELETE"])
def delete_message():
    message_id = request
    return message_service.delete_message()