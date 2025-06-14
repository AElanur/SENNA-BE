class ChatbotClassifier:
    def __init__(self, traits_of_user_repo):
        self.traits_of_user_repo = traits_of_user_repo
        self.trait_possession_grade = 0.5

    def classify_trait(self, data):
        user_id = data["receiver_id"]
        self.insert_trait_to_user(data)
        self.calculate_presence_of_trait(user_id)

    def calculate_presence_of_trait(self, user_id):
        result = self.get_messaging_trait_count(user_id)
        print(user_id)
        if result == None:
            print("No messages present")
        elif result[0] / result[1] > self.trait_possession_grade:
            print("percentage is above 50%")

    def get_messaging_trait_count(self, user_id):
        result = self.traits_of_user_repo.get_count_trait_in_messages(user_id)
        return result

    def insert_trait_to_user(self, data):
        self.traits_of_user_repo.insert_trait(data)