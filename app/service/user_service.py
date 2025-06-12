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

    def hash_password(self, user_password):
        password = user_password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)
        return hashed_password.decode('utf-8')

