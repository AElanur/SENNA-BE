class MessageService:
    def __init__(self, chatbot_service, message_repository):
        self.chatbot_service = chatbot_service
        self.message_repository = message_repository

    def get_messages(self, chat_id: int) -> list[dict]:
        messages = self.message_repository.get_messages_from_chat(chat_id)
        if len(messages) > 10:
            message = next(iter(messages))
            self.delete_message(message['message_id'])
        return messages

    def send_message(self, data):
        self.insert_message(data)
        response_message = self.chatbot_service.handle_message(data)

        return response_message

    def insert_message(self, data):
        self.message_repository.insert_message(data)

    def update_message(self):
        pass

    def delete_message(self, message_id):
        self.message_repository.delete_message(message_id)