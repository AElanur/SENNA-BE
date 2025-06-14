import bcrypt
import secrets
from datetime import datetime, timezone, timedelta

class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def validate_session(self, session_key):
        session = self.user_repository.get_session(session_key)
        if session and session['expires_at'] > datetime.now(timezone.utc):
            return session['user_id']
        return None

    def logout_user(self, user_id):
        self.user_repository.delete_sessions_by_user(user_id)
        return {"status": "success", "message": "User logged out."}

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
        user_id = user_info[0]
        submitted_password = user_data["password"].encode('utf-8')
        user_password = user_info[1]
        if isinstance(user_password, memoryview):
            user_password = user_password.tobytes()

        if bcrypt.checkpw(submitted_password, user_password):
            session_key = self.create_user_session(user_id)
            return {
                "session_key": session_key,
                "user_id": user_info[0],
                "chat_id": user_info[2]
            }
        else:
            return {"ERROR_MESSAGE": "Password is incorrect"}

    def create_user_session(self, user_id):
        session_key = secrets.token_urlsafe(32)
        expires_at = datetime.now(UTC) + timedelta(hours=1)
        self.user_repository.create_session(user_id, session_key, expires_at)
        return session_key

    @staticmethod
    def hash_password(user_password):
        password = user_password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)
        return hashed_password.decode('utf-8')

