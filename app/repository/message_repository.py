from datetime import datetime
from .connection_repository import create_connection

class MessageRepository:
    @staticmethod
    def get_messages_from_chat(chat_id):
        query = 'SELECT * FROM "Message" WHERE "chat_id" = %s ORDER BY "message_id" ASC'
        try:
            with create_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(query, (chat_id,))
                rows = cursor.fetchall()
                messages = [
                    dict(zip([column[0] for column in cursor.description], row))
                    for row in rows
                ]
            return messages
        except Exception as e:
            print("Error retrieving messages: ", e)
            return []

    @staticmethod
    def delete_message(message_id):
        query = 'DELETE FROM "Message" WHERE "message_id" = %s'
        try:
            with create_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(query, (message_id,))
        except Exception as e:
            print("Error deleting message: ", e)
            return []

    @staticmethod
    def insert_message(user_message):
        query = (
            'INSERT INTO "Message" ("sender_id", "chat_id", "content", "timestamp", "sender_type") '
            'VALUES (%s, %s, %s, %s, %s)'
        )
        try:
            with create_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(query, (
                    user_message["sender_id"],
                    user_message["chat_id"],
                    user_message["content"],
                    datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
                    user_message["sender_type"]
                ))
                connection.commit()
        except Exception as e:
            print("Error inserting message:", e)