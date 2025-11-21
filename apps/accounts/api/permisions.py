from rest_framework.permissions import BasePermission


class IsVerified(BasePermission):
    """
    Allows access only to verified customers (customer.is_verified == True).
    """

    message = "Your email has not been confirmed. Please check your email and verify it."

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return getattr(request.user, "is_verified", False)
