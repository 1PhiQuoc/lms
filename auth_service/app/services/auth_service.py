from app.providers.user_provider import UserProvider

class AuthService:
    @staticmethod
    def login(data):
        username = data.get("username")
        password = data.get("password")
        return UserProvider.authenticate_user(username, password)
    @staticmethod
    def register(username, password):
        return UserProvider.create_user(username, password)
    def register_service(data):
        username = data.get("username")
        password = data.get("password")
        return UserProvider.create_user(username, password)
    def get_profile():
        return UserProvider.get_user_profile()
