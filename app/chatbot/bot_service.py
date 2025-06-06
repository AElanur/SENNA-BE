class BotService:
    def __init__(self, classifier, bot_model, message_repository, chat_repository):
        self.classifier = classifier
        self.bot_model = bot_model
        self.message_repository = message_repository
        self.chat_repository = chat_repository

    def handle_message(self, data):
        bot_response = self.generate_response(data['content'])
        bot_message = {
            "chat_id": data['chat_id'],
            "sender_id": self.get_bot_id(data['chat_id']),
            "content": bot_response,
            "sender_type": "bot"
        }
        self.insert_message(bot_message)
        return {"status": "success", "message": "Bot response inserted."}

    def generate_response(self, user_message):
        predicted_class, probs = self.classifier.classify_message(user_message)
        response = self.bot_model.generate_message(user_message, predicted_class)
        return response

    def get_bot_id(self, chat_id):
        bot_id = self.chat_repository.get_bot_id(chat_id)
        return bot_id

    def insert_message(self, data):
        self.message_repository.insert_message(data)