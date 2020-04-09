from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.contrib.auth import get_user_model
from eventos.models import Event
User = get_user_model()

def home_view(request):
    title = ""
    context = {"title":title}
    return render(request, "home.html", context)

def contacto_view(request):
    title = "contacto"
    context = {"title":title}
    return render(request, "contacto.html", context)

def quienes_somos_view(request):
    title = "nosotros"
    context = {"title":title}
    return render(request, "quienes_somos.html", context)

@staff_member_required
def user_list_view(request):
    query = User.objects.all()
    title = "users"
    context = {
        "title": title,
        "user_list" : query
        }
    return render(request, "userlist.html", context)

@staff_member_required
def usersToBeAccepted_view(request):
    query = eventpost.objects.all()
    title = "users to be accepted"
    context = {
        "title": title,
        "postevents_list" : query
        }
    return render(request, "users-to-be-accepted.html", context)
