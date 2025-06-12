from .training.big5.tokenizer import vocab, text_to_indices
import torch


class BotService:
    def __init__(self, bot_model, chatbot_classifier, personality_model, message_repository, traits_of_user_repository, chat_repository, trait_info):
        self.bot_model = bot_model
        self.chatbot_classifier = chatbot_classifier
        self.personality_model = personality_model
        self.message_repository = message_repository
        self.traits_of_user_repository = traits_of_user_repository
        self.chat_repository = chat_repository
        self.trait_info = trait_info

    def analyze_personality_trait(self, user_message):
        text = user_message.lower()

        indices = text_to_indices(user_message, vocab)
        input_tensor = torch.tensor([indices], dtype=torch.long).to(self.personality_model.embedding.weight.device)
        with torch.no_grad():
            logits = self.personality_model(input_tensor)
            predicted_class = logits.argmax(dim=1).item()

        personality_info = self.trait_info[predicted_class]
        trait_keywords = personality_info["trait_keywords"]

        matched_identifier = None
        # Check all trait keywords for matches in the text
        for trait, kw_list in trait_keywords.items():
            if any(kw in text for kw in kw_list):
                matched_identifier = trait
                break

        # Optional: fallback to most likely trait if none matched
        if not matched_identifier:
            matched_identifier = list(trait_keywords.keys())[0]

        return matched_identifier

    def handle_message(self, data):
        conversation_history = self.get_conversation_history(data['chat_id'])
        bot_response = self.generate_response(conversation_history)
        user_message = conversation_history[-1]["input"]

        detected_trait = self.analyze_personality_trait(user_message)
        print(f'Trait detected: {detected_trait}')

        bot_message = {
            "chat_id": data['chat_id'],
            "user_id": self.get_bot_id(data['chat_id']),
            "content": bot_response,
            "sender_type": "bot",
            "trait_identifier": detected_trait
        }
        self.insert_message(bot_message)
        self.insert_trait_to_user(bot_message)
        return {"status": "success", "message": "Bot response inserted.", "identified_trait": detected_trait}

    def generate_response(self, conversation_history):
        user_message = conversation_history[-1]["input"]

        response = self.bot_model.generate_message(conversation_history, user_message)
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

    def insert_trait_to_user(self, data):
        self.chatbot_classifier.classify_trait(data)
