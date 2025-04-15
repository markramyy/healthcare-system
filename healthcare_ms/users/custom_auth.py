from rest_framework_simplejwt.exceptions import AuthenticationFailed
from healthcare_ms.users.models import User


def custom_user_authentication_rule(user: User):

    if not user.is_active:
        raise AuthenticationFailed('User account is not active')

    if user.user_type not in [type[0] for type in User.USER_TYPE_CHOICES]:
        raise AuthenticationFailed('User does not have the expected type')

    return True
