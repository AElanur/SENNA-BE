from .connection_repository import create_connection

class TraitsOfUserRepository:
    @staticmethod
    def get_traits_of_user(user_id):
        query = (
            'SELECT t.trait_identifier '
            'FROM traits_of_user tus '
            'JOIN trait t ON t.trait_id = tus.trait_id '
            'WHERE tus.user_id = %s'
        )
        try:
            with create_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(query, (user_id,))
                rows = cursor.fetchall()
                traits = [
                    dict(zip([column[0] for column in cursor.description], row))
                    for row in rows
                ]
            return traits
        except Exception as e:
            print("Error retrieving traits: ", e)
            return []

    @staticmethod
    def get_count_trait_in_messages(user_id):
        try:
            with create_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(
                    'SELECT tus.trait_count, mou.messaging_count '
                    'FROM traits_of_user tus '
                    'JOIN messages_of_user mou ON mou.user_id = tus.user_id '
                    'WHERE mou.user_id = %s',
                    (user_id,)
                )
                result = cursor.fetchone()
                if result:
                    return result
                return None
        except Exception as e:
            print("Error getting bot id:", e)
            return None

    @staticmethod
    def insert_trait(generated_response):
        query = (
            'INSERT INTO traits_of_user (user_id, trait_id, trait_count, trait_possession) '
            'SELECT %s, t.trait_id, 1, %s '
            'FROM trait t '
            'WHERE t.trait_identifier = %s '
            'ON CONFLICT (user_id, trait_id) '
            'DO UPDATE SET trait_count = traits_of_user.trait_count + 1, '
            'trait_possession = EXCLUDED.trait_possession;'
        )
        try:
            with create_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(query, (
                    generated_response["receiver_id"],
                    False,
                    generated_response["trait_identifier"],
                ))
                connection.commit()
        except Exception as e:
            print("Error inserting trait:", e)
