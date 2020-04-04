from django import forms

from .models import eventpost

class EventoModelForm(forms.ModelForm):
    class Meta:
        model = eventpost
        # Tengo que mapear los campos de mi modelo que quiera actualizar con el form
        fields = ['title', 'company', 'slug', 'desc', 'text' ]

    def clean_slug(self, *args, **kwargs):
        instance = self.instance
        slug = self.cleaned_data.get('slug')
        query = eventpost.objects.filter(slug__iexact=slug)
        if instance is not None:
            query = query.exclude(pk=instance.pk)
        if query.exists():
            raise forms.ValidationError("No admito slugs iguales")
        return slug
