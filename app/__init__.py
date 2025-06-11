from flask import Flask
from flask_cors import CORS
from sympy.printing.pytorch import torch

from app.chatbot.bot_service import BotService
from app.repository.chat_repository import ChatRepository
from app.repository.message_repository import MessageRepository
from app.repository.traits_of_user_repository import TraitsOfUserRepository
from app.routes import message_route
from app.routes import chat_route
from app.routes import traits_of_user_route
from app.service.chat_service import ChatService
from app.service.message_service import MessageService
from app.service.traits_of_user_service import TraitsOfUserService
from app.chatbot.chatbot_classifier import ChatbotClassifier
from app.chatbot.chatbot import Chatbot
from app.chatbot.training.big5.text_cnn import TextCNN
from app.chatbot.training.big5.tokenizer import vocab
from app.chatbot.training.big5.trait_info import trait_info

def create_app():
    app = Flask(__name__)
    CORS(app)
    model_path = "app/chatbot/training/communication/training_data/communication_data"
    personality_model_path = "app/chatbot/training/big5/data/big5_dataset.pt"
    max_length = 256

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    chatbot = Chatbot(model_path, max_length)

    embed_dim = 100
    num_classes = 5
    personality_model = TextCNN(vocab_size=len(vocab), embed_dim=embed_dim, num_classes=num_classes)
    state_dict = torch.load(personality_model_path, map_location=device, weights_only=False)
    personality_model.load_state_dict(state_dict)
    personality_model.to(device)
    personality_model.eval()

    message_repository = MessageRepository()
    chat_repository = ChatRepository()
    traits_of_user_repository = TraitsOfUserRepository()
    bot_service = BotService(chatbot, personality_model, message_repository, traits_of_user_repository, chat_repository, trait_info)

    message_service = MessageService(bot_service, message_repository)
    chat_service = ChatService(bot_service, chat_repository)
    traits_of_user_service = TraitsOfUserService(traits_of_user_repository)


    message_bp = message_route.create_message_blueprint(message_service)
    chat_bp = chat_route.create_chat_blueprint(chat_service)
    traits_of_user_bp = traits_of_user_route.create_traits_of_user_blueprint(traits_of_user_service)

    app.register_blueprint(message_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(traits_of_user_bp)

    return app

