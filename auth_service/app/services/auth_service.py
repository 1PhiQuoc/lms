from app.providers.user_provider import UserProvider

class AuthService:
    @staticmethod
    def login(data):
        return UserProvider.authenticate_user(data)
    @staticmethod
    def register(data):
        return UserProvider.create_user(data)
        
