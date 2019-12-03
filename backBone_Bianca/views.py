from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import get_user_model
from BarEvento.models import BarPost
User = get_user_model()

def home_view(request):
    title = ""
    context = {"title":title}
    return render(request, "home.html",context)

def contacto_view(request):
    title = "contacto"
    context = {"title":title}
    return render(request, "contacto.html",context)

def quienes_somos_view(request):
    title = "nosotros"
    context = {"title":title}
    return render(request, "quienes_somos.html",context)

@staff_member_required
def user_list_view(request):
    qs = User.objects.all()
    title = "users"
    context = {
        "title": title,
        "user_list" : qs 
        }
    return render(request, "userlist.html",context)

@staff_member_required
def usersToBeAccepted_view(request):
 

    qs = BarPost.objects.all()

#    for x in qs:
#        variable = x.users.exclude(x.users_winners)
#       x.users_tobeaccepted = x.users.exclude(x.users_winners)
#    variable = BarPost.objects.filter()

    title = "users to be accepted"
    context = {
        "title": title,
        "BarEvento_list" : qs
        }
    return render(request, "users-to-be-accepted.html",context)