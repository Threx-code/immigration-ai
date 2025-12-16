from rest_framework import status
from main_system.base.auth_api import AuthAPI
from users_access.serializers.users.create_user_success import UserSerializer
from users_access.services.user_service import UserService
from users_access.serializers.users.add_avatar import UserAvatarSerializer


class UserAvatarAPI(AuthAPI):

    def patch(self, request):
        serializer = UserAvatarSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        service = UserService()
        user_avatar = service.update_avatar(request.user, serializer.validated_data.get('avatar'))

        return self.api_response(
            message="User avatar updated successfully.",
            data=UserSerializer(user_avatar).data,
            status_code=status.HTTP_200_OK
        )
