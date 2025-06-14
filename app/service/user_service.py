import bcrypt

class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def create_user(self, user_data):
        hashed_password = self.hash_password(user_data["password"])
        user = {
            "username": user_data["username"],
            "email": user_data["email"],
            "password": hashed_password
        }
        return self.user_repository.create_user(user)

    def login_user(self, user_data):
        user_info = self.user_repository.login_user(user_data["username"])
        submitted_password = user_data["password"].encode('utf-8')
        user_password = user_info[1]
        if isinstance(user_password, memoryview):
            user_password = user_password.tobytes()

        if bcrypt.checkpw(submitted_password, user_password):
            return {
                "user_id": user_info[0],
                "chat_id": user_info[2]
            }
        else:
            return { "ERROR_MESSAGE": "Password is incorrect" }

    @staticmethod
    def hash_password(user_password):
        password = user_password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)
        return hashed_password.decode('utf-8')

