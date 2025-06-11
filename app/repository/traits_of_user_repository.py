from .connection_repository import create_connection

class TraitsOfUserRepository:
    @staticmethod
    def get_traits_of_user(user_id):
        query = (
            'SELECT t.trait_identifier '
            'FROM "Traits-of-user" tus '
            'JOIN Trait t ON t.trait_id = tus.trait_id '
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
    def insert_trait(generated_response):
        query = (
            'INSERT INTO "Traits-of-user" ("user_id", "trait_id") '
            'SELECT %s, t.trait_id '
            'FROM Trait t '
            'WHERE t.trait_identifier = %s;'
        )
        try:
            with create_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(query, (
                    generated_response["sender_id"],
                    generated_response["trait_identifier"]
                ))
                connection.commit()
        except Exception as e:
            print("Error inserting trait:", e)
