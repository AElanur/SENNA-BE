class BotService:
    def __init__(self, classifier, bot_model, message_repository, chat_repository):
        self.classifier = classifier
        self.bot_model = bot_model
        self.message_repository = message_repository
        self.chat_repository = chat_repository

    def handle_message(self, data):
        conversation_history = self.get_conversation_history(data['chat_id'])
        bot_response = self.generate_response(conversation_history)
        bot_message = {
            "chat_id": data['chat_id'],
            "sender_id": self.get_bot_id(data['chat_id']),
            "content": bot_response,
            "sender_type": "bot"
        }
        self.insert_message(bot_message)
        return {"status": "success", "message": "Bot response inserted."}

    def generate_response(self, conversation_history):
        user_message = conversation_history[-1]["input"]
        predicted_class, probs = self.classifier.classify_message(user_message)
        response = self.bot_model.generate_message(conversation_history, predicted_class)
        return response

    def get_conversation_history(self, chat_id):
        messages = self.message_repository.get_messages_from_chat(chat_id)
        history = []
        for msg in messages:
            if msg["sender_type"] == "user":
                history.append({"input": msg["content"]})
            else:
                history.append({"target": msg["content"]})
        return history

    def get_bot_id(self, chat_id):
        bot_id = self.chat_repository.get_bot_id(chat_id)
        return bot_id

    def insert_message(self, data):
        self.message_repository.insert_message(data)
