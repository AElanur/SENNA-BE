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