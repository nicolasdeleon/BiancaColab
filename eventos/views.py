from django.shortcuts import render, Http404, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import eventpost
from .models import postrelations
from .forms import EventoModelForm


#CRUD:CreateRetrieveUpdateDelete

#retrieve all
@staff_member_required 
def eventpost_alldetail_view(request):
    #lista de todos los eventos que tenemos:
    qs = eventpost.objects.all()#obtengo todos los post
    template_name = 'eventos/alldetail_view.html' #esto lo tengo que asociar a un html creo
    cant_de_posts = qs.count()
    if(cant_de_posts == 0):
        print("ERROR: No hay eventos!")
        raise Http404    
    context = {
        "title" : "Nuestros Eventos",
        "object_list" : qs,
        "cant_de_posts" : cant_de_posts
    } 
    return render(request, template_name,context)

#retrieve one
@staff_member_required 
def eventpost_event_view(request,slug):
    #lista de todos los eventos que tenemos:
    obj = get_object_or_404(BarPost,slug = slug) #obtengo el post del bar cuyo slug es unico
    template_name = 'eventos/event_view.html' #esto lo tengo que asociar a un html creo 
    users = obj.users.all()      
    context = {
        "title" : obj.title,
        "object" : obj,
        "cant_de_activos" : users,
    } 
    return render(request, template_name,context)

#create one
@staff_member_required
def blog_post_create_view(request):
    #use a form
    form = EventoModelForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = EventoModelForm()    
    template_name = "eventos/create_evento.html"
    context = {
        "title": "create event",
        'form' : form
    }

    return render(request, template_name,context)


#update one
@staff_member_required
def blog_post_update_view(request,slug):
    obj = BarPost.objects.get(slug = slug)
    if obj == None:
        raise Http404
    form = EventoModelForm(request.POST or None,instance=obj)
    if form.is_valid():
        form.save()
    template_name = "eventos/updateEvento.html"
    context = {
        'title' : "update event ",
        'object' : obj,
        'form' : form,
    }
    return render(request, template_name,context)

#delete one
@staff_member_required
def blog_post_delete_view(request,slug):
    obj = get_object_or_404(BarPost,slug = slug)
    if request.method == "POST":
        obj.delete()
        return redirect("/eventos/") 
    template_name = "eventos/deleteEvento.html"
    context = {
        'title' : "delete event ",
        'object' : obj,
    }
    return render(request, template_name,context)

