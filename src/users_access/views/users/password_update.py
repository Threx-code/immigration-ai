from rest_framework import status
from main_system.base.auth_api import AuthAPI
from users_access.services.password_reset_services import PasswordResetService
from users_access.serializers.users.create_user_success import UserSerializer
from users_access.services.user_service import UserService
from users_access.serializers.users.password_update import PasswordUpdateSerializer


class UserPasswordUpdateAPI(AuthAPI):
    serializer_class = PasswordUpdateSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        service = UserService()
        user = service.update_password(request.user, serializer.validated_data.get('password'))

        PasswordResetService().create(user=user)

        return self.api_response(
            message="User password updated successfully.",
            data=UserSerializer(user).data,
            status_code=status.HTTP_200_OK
        )




