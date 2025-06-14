from .connection_repository import create_connection

class UserRepository:
    @staticmethod
    def create_user(user_data):
        query = (
            'INSERT INTO senna_user (username, email, password) '
            'VALUES (%s, %s, %s) '
            'RETURNING user_id;'
        )
        try:
            with create_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(query, (
                    user_data['username'],
                    user_data['email'],
                    user_data['password'],
                ))
                user_id = cursor.fetchone()[0]
                connection.commit()
                return user_id
        except Exception as e:
            print("Error inserting trait:", e)

    @staticmethod
    def login_user(user_data):
        query = (
            'SELECT u.user_id, u.password, c.chat_id FROM senna_user u '
            'JOIN chat c ON c.user_id = u.user_id '
            'WHERE username = %s;'
        )
        try:
            with create_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(query, (user_data,))
                data_user = cursor.fetchone()
                connection.commit()
                return data_user
        except Exception as e:
            print("Error inserting trait:", e)

    @staticmethod
    def create_session(user_id, session_key, expires_at):
        query = (
            'INSERT INTO user_session (user_id, user_session_id, expires_at) '
            'VALUES (%s, %s, %s);'
        )
        try:
            with create_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(query, (user_id, session_key, expires_at))
                connection.commit()
        except Exception as e:
            print("Error creating session:", e)

    @staticmethod
    def get_session(session_key):
        query = (
            'SELECT user_id, expires_at FROM user_session '
            'WHERE user_session_id = %s;'
        )
        try:
            with create_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(query, (session_key,))
                result = cursor.fetchone()
                if result:
                    return {'user_id': result[0], 'expires_at': result[1]}
                return None
        except Exception as e:
            print("Error fetching session:", e)
            return None

    @staticmethod
    def validate_session(session_key):
        query = (
            'SELECT user_id FROM user_session '
            'WHERE user_session_id = %s AND expires_at > NOW();'
        )
        try:
            with create_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(query, (session_key,))
                result = cursor.fetchone()
                return result[0] if result else None
        except Exception as e:
            print("Error validating session:", e)
            return None

