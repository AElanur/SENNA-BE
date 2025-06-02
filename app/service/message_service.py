class MessageService:
    def __init__(self, chatbot):
        self.chatbot = chatbot

    def get_messages(self, chat_id: int) -> list[dict]:
        messages = [
            {"sender": "Bot", "recipient": "Talon", "content": "Hallo, hoe gaat het?"},
            {"sender": "Talon", "recipient": "Bot", "content": "Goed, dank je! En met jou?"},
            {"sender": "Bot", "recipient": "Talon", "content": "Met mij gaat het ook goed, bedankt!"},
            {"sender": "Talon", "recipient": "Bot", "content": "Wat kan ik vandaag voor je doen?"},
            {"sender": "Bot", "recipient": "Talon", "content": "Kun je me helpen met mijn agenda?"},
            {"sender": "Talon", "recipient": "Bot", "content": "Natuurlijk! Wat wil je toevoegen?"},
            {"sender": "Bot", "recipient": "Talon", "content": "Een afspraak om 15:00 uur met Dr. Jansen."},
            {"sender": "Talon", "recipient": "Bot", "content": "Afspraak toegevoegd. Nog iets anders?"},
            {"sender": "Bot", "recipient": "Talon", "content": "Nee, dat was alles. Bedankt!"},
            {"sender": "Talon", "recipient": "Bot", "content": "Graag gedaan! Fijne dag verder."}
        ]
        return messages

    def send_message(self, user_message: str):
        print(user_message)
        response_message = self.chatbot.send_message(user_message)
        print("Bot response: " + response_message)
        return response_message

    def update_message(self):
        pass

    def delete_message(self):
        pass