from datetime import datetime
from .connection_repository import create_connection

class MessageRepository:
    @staticmethod
    def get_messages_from_chat(chat_id):
        query = 'SELECT * FROM message WHERE "chat_id" = %s ORDER BY message_id ASC'
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
        query = 'DELETE FROM message WHERE message_id = %s'
        try:
            with create_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(query, (message_id,))
        except Exception as e:
            print("Error deleting message: ", e)
            return []

    @staticmethod
    def insert_message(chat_id, user_id, content, sender_type):
        query = (
            'INSERT INTO message (chat_id, user_id, content, "timestamp", sender_type) '
            'VALUES (%s, %s, %s, %s, %s)'
        )
        try:
            with create_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(query, (
                    chat_id,
                    user_id,
                    content,
                    datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
                    sender_type
                ))
                connection.commit()
        except Exception as e:
            print("Error inserting message:", e)
