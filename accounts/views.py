import re
from django.shortcuts import render, Http404
from .models import user, EmailConfirmed


SHA1_RE = re.compile('^[a-f0-9]{40}$')

# Create your views here.
def activation_view(request, activation_key):
    if SHA1_RE.search(activation_key):
        template_name = 'activation_complete.html'
        try:
            instance = EmailConfirmed.objects.get(activation_key=activation_key)
        except EmailConfirmed.DoesNotExist:
            instance = None
            raise Http404
        if instance is not None and not instance.confirmed:
            status = "Activation Complete!"
            instance.confirmed = True
            instance.save()
        elif instance is not None and instance.confirmed:
            status = "Account is Already Active"
        context = {
            'status': status
        }
        return render(request, template_name,context)
    else:
        raise Http404