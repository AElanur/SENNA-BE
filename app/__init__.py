from flask import Flask
from flask_cors import CORS

from app.chatbot.bot_service import BotService
from app.repository.chat_repository import ChatRepository
from app.repository.message_repository import MessageRepository
from app.routes import message_route
from app.routes import chat_route
from app.service.chat_service import ChatService
from app.service.message_service import MessageService
from app.chatbot.chatbot_classifier import ChatbotClassifier
from app.chatbot.chatbot import Chatbot


def create_app():
    app = Flask(__name__)
    CORS(app)
    model_path = "app/chatbot/training/communication/training_data/communication_data"
    classifier_path = "app/chatbot/training/classifier/training_data/classification_data"
    max_length = 256

    classifier = ChatbotClassifier(classifier_path, max_length)
    chatbot = Chatbot(model_path, max_length)

    message_repository = MessageRepository()
    chat_repository = ChatRepository()
    bot_service = BotService(classifier, chatbot, message_repository, chat_repository)

    message_service = MessageService(bot_service, message_repository)
    chat_service = ChatService(bot_service, chat_repository)


    message_bp = message_route.create_message_blueprint(message_service)
    chat_bp = chat_route.create_chat_blueprint(chat_service)

    app.register_blueprint(message_bp)
    app.register_blueprint(chat_bp)

    return app

