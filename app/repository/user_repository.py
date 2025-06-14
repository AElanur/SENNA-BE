from .connection_repository import create_connection

class UserRepository:
    @staticmethod
    def create_user(user_data):
        query = (
            'INSERT INTO "User" (username, email, password) '
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
            'SELECT u.user_id, u.password, c.chat_id FROM "User" u '
            'JOIN "Chat" c ON c.user_id = u.user_id '
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