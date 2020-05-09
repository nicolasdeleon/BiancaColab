from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import Http404, get_object_or_404, redirect, render

from .forms import EventoModelForm
from .models import Event


@staff_member_required
def eventpost_alldetail_view(request):
    """ List ALL existing events """
    query = Event.objects.all()
    template_name = 'eventos/alldetail_view.html'
    cant_de_posts = query.count()
    if cant_de_posts == 0:
        print("ERROR: No hay eventos!")
        raise Http404
    context = {
        "title": "Nuestros Eventos",
        "object_list": query,
        "cant_de_posts": cant_de_posts
    }
    return render(request, template_name, context)


@staff_member_required
def eventpost_event_view(request, slug):
    """ Gets a single event denoted by its slug """
    event = get_object_or_404(Event, slug=slug)
    template_name = 'eventos/event_view.html'
    users = event.users.all()
    post_relations = event.postelations_set.all()
    story_list = []
    for post_relation in post_relations:
        story_list.append(post_relation.story.image)
    context = {
        "title": event.title,
        "object": event,
        "cant_de_activos": users,
        "images": story_list
    }
    return render(request, template_name, context)


@staff_member_required
def blog_post_create_view(request):
    """ Creates a new event """
    form = EventoModelForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = EventoModelForm()
    template_name = "eventos/create_evento.html"
    context = {
        "title": "create event",
        'form': form
    }
    return render(request, template_name, context)


@staff_member_required
def blog_post_update_view(request, slug):
    """ Updates an event denoted by its slug """
    event = Event.objects.get(slug=slug)
    if event is None:
        raise Http404
    form = EventoModelForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
    template_name = "eventos/updateEvento.html"
    context = {
        'title': "update event ",
        'object': event,
        'form': form,
    }
    return render(request, template_name, context)


@staff_member_required
def blog_post_delete_view(request, slug):
    """ Deletes an event denoted by its slug """
    event = get_object_or_404(Event, slug=slug)
    if request.method == "POST":
        event.delete()
        return redirect("/eventos/")
    template_name = "eventos/deleteEvento.html"
    context = {
        'title': "delete event",
        'object': event,
    }
    return render(request, template_name, context)
