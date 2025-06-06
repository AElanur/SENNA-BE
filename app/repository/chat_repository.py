from .connection_repository import create_connection

class ChatRepository:
    @staticmethod
    def create_chat(chat_data):
        query = (
            'INSERT INTO "Chat" (user_id, bot_id) '
            'VALUES (%s, %s) '
            'RETURNING chat_id'
        )
        try:
            with create_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(query, (
                    chat_data['user_id'],
                    chat_data['bot_id']
                ))
                result = cursor.fetchone()
                if result:
                    chat_id = result[0]
                    connection.commit()
                    return chat_id
                else:
                    return None
        except Exception as e:
            print("Error creating chat:", e)

    @staticmethod
    def get_bot_id(bot_id):
        try:
            with create_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(
                    'SELECT "bot_id" FROM "Chat" WHERE "bot_id" = %s', (bot_id,)
                )
                result = cursor.fetchone()
                if result:
                    return result[0]
                return None
        except Exception as e:
            print("Error getting bot id:", e)
            return None
