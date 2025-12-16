from rest_framework import status
from finance.base.auth_api import AuthAPI
from password_reset.services.services import PasswordResetService
from ..serializers.create_user_success import UserSerializer
from ..services.user_service import UserService
from ..serializers.password_update import PasswordUpdateSerializer


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




