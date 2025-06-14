class MessageService:
    def __init__(self, chatbot_service, message_repository):
        self.chatbot_service = chatbot_service
        self.message_repository = message_repository

    def get_messages(self, chat_id: int) -> list[dict]:
        messages = self.message_repository.get_messages_from_chat(chat_id)
        return messages

    def send_message(self, user_id: int, chat_id: int, content: str):
        self.insert_message(user_id, chat_id, content)
        response_message = self.chatbot_service.handle_message({
            "user_id": user_id,
            "chat_id": chat_id,
            "content": content
        })
        return response_message

    def insert_message(self, user_id, chat_id, data):
        content = data['content']
        sender_type = data['sender_type']
        self.message_repository.insert_message(chat_id, user_id, content, sender_type)
        self.delete_messages_after_limit(user_id, chat_id)

    def delete_messages_after_limit(self, user_id, chat_id):
        messages = self.get_messages(chat_id)
        if len(messages) > 10:
            message = messages[0]  # Assuming messages are ordered
            self.delete_message(message['message_id'])
    def delete_message(self, message_id):
        self.message_repository.delete_message(message_id)