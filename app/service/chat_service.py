import json


class ChatService:
    def __init__(self, chatbot, chat_repository):
        self.chatbot = chatbot
        self.chat_repository = chat_repository

    def create_chat(self, chat_data):
        chat_id = self.chat_repository.create_chat(chat_data)