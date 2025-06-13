from .connection_repository import create_connection

class ChatRepository:
    @staticmethod
    def create_chatbot(chatbot_data):
        query = (
            'INSERT INTO "Chatbot" (chatbot_name, created_by_user_id) '
            'VALUES (%s, %s) '
            'RETURNING chatbot_id'
        )
        try:
            with create_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(query, (
                    chatbot_data['botName'],
                    chatbot_data['userID']
                ))
                chatbot_id = cursor.fetchone()[0]
                connection.commit()
                return chatbot_id
        except Exception as e:
            print("Error creating chatbot:", e)

    @staticmethod
    def create_chat(chat_data):
        query = (
            'INSERT INTO "Chat" (user_id, chatbot_id) '
            'VALUES (%s, %s) '
            'RETURNING chat_id'
        )
        try:
            with create_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(query, (
                    chat_data['user_id'],
                    chat_data['chatbot_id']
                ))
                chat_id = cursor.fetchone()[0]
                connection.commit()
                return chat_id
        except Exception as e:
            print("Error creating chat:", e)

    @staticmethod
    def get_bot_id(bot_id):
        try:
            with create_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(
                    'SELECT "chatbot_id" FROM "Chat" WHERE "chatbot_id" = %s', (bot_id,)
                )
                result = cursor.fetchone()
                if result:
                    return result[0]
                return None
        except Exception as e:
            print("Error getting bot id:", e)
            return None

    @staticmethod
    def get_chat_participants(chat_id):
        try:
            with create_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(
                    'SELECT "chatbot_name", "username" FROM "Chat" c '
                    'JOIN "User" u ON u.user_id = c.user_id '
                    'JOIN "Chatbot" cb ON cb.chatbot_id = c.chatbot_id '
                    'WHERE "chat_id" = %s', (chat_id,)
                )
                row = cursor.fetchone()
                connection.commit()
                if row:
                    return {
                        "chatbot_name": row[0],
                        "username": row[1]
                    }
                else:
                    return {}
        except Exception as e:
            print("Error getting bot id:", e)
            return None


