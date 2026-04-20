from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from .models import User
from apps.library.models import Library

@receiver(user_logged_in)
def handle_user_logged_in(request, user, **kwargs):
    print("User logged in: ", user.email, "(id: ", user.id, ")")
    try:
        library = Library.objects.filter(user=user.id)
        if len(library) == 0:
            library = Library.objects.create(user=user)
            library.save()
        else:
            print("Library Exist")
    except Library.DoesNotExist:
        print("Signal create library Error")
        
