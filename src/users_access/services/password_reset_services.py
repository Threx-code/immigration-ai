from ..models import PasswordReset

class PasswordResetService:
    def __init__(self):
        self.manager = PasswordReset.objects

    def create(self, user):
        created = self.manager.create_password_reset(user=user)

