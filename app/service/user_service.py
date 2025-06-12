import bcrypt

class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def create_user(self, user_data):
        print(user_data)
        hashed_password = self.hash_password(user_data["password"])
        user = {
            "username": user_data["username"],
            "email": user_data["email"],
            "password": hashed_password
        }
        return self.user_repository.create_user(user)

    def login_user(self, user_data):
        user = self.user_repository.get_user(user_data["username"])
        submitted_password = user_data["password"].encode('utf-8')
        user_password = user[2]
        if isinstance(user_password, memoryview):
            user_password = user_password.tobytes()

        if bcrypt.checkpw(submitted_password, user_password):
            return user[0]

        else:
            return "Password is incorrect"

    @staticmethod
    def hash_password(user_password):
        password = user_password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)
        return hashed_password.decode('utf-8')

