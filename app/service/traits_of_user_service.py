class TraitsOfUserService:
    def __init__(self, traits_of_user_repository):
        self.traits_of_user_repository = traits_of_user_repository

    def get_traits_of_user(self, user_id):
        return self.traits_of_user_repository.get_traits_of_user(user_id)