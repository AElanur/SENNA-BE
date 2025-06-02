from flask import Flask
from flask_cors import CORS
from app.routes import message_route
from app.service.message_service import MessageService
from app.chatbot.chatbot import Chatbot


def create_app():
    app = Flask(__name__)
    CORS(app)
    chatbot = Chatbot()
    message_service = MessageService(chatbot)
    message_bp = message_route.create_message_blueprint(message_service)

    app.register_blueprint(message_bp)


    return app

