from app.providers.user_provider import UserProvider

class AuthService:
    @staticmethod
    def login(data):
        return UserProvider.authenticate_user(data)
    @staticmethod
    def register(username, password):
        return UserProvider.create_user(username, password)
    def register_service(data):
        return UserProvider.create_user(data)
        
