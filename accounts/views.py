from django.shortcuts import render
from .models import user, EmailConfirmed

# Create your views here.
def email_test_view(request):
    template_name = 'email_confirmation.html'
    userario = user.objects.get(email="nicolas@hotmail.com")
    userario.emailconfirmed.activate_user_email()
    return render(request, template_name)