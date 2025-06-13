
class ChatService:
    def __init__(self, chatbot, chat_repository):
        self.chatbot = chatbot
        self.chat_repository = chat_repository

    def create_chat(self, chatbot_data):
        chatbot_id = self.create_chatbot(chatbot_data)
        chat_data = {
            "user_id": chatbot_data["userID"],
            "chatbot_id": chatbot_id
        }
        return self.chat_repository.create_chat(chat_data)

    def get_chat_participants(self, chat_id):
        return self.chat_repository.get_chat_participants(chat_id)

    def create_chatbot(self, chatbot_data):
        return self.chat_repository.create_chatbot(chatbot_data)