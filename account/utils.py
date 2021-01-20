from django.core.mail import send_mail
from rest_framework import permissions

def send_activation_email(user):
    subject    = "Thanks for registrations to our website!"
    body       = "Thanks for registrations to our website!\n"\
        "For activation your account, follow the link below:\n"\
        f'http://127.0.0.1:8000/v1/account/activate/{user.activation_code}/'
    from_email = 'e-shop@django.kg'
    recipients = [user.email]
    send_mail(subject=subject, message=body,
              from_email=from_email, recipient_list=recipients,
              fail_silently=False)


class IsOwnerAccount(permissions.BasePermission):
    """Permission for checking user is owner of the account or superuser"""
    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username or bool(request.user and request.user.is_superuser)



