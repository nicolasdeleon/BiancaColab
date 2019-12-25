from django import forms

from .models import eventpost

class EventoModelForm(forms.ModelForm):
	class Meta:
		model = eventpost
		fields = ['title','company','slug','desc','code'] #tengo que mapear los campos de mi modelo que quiera actualizar con el form
	
	def clean_slug(self, *args, **kwargs):
		instance = self.instance
		slug = self.cleaned_data.get('slug')
		qs = eventpost.objects.filter(slug__iexact= slug)
		if instance is not None:
			qs = qs.exclude(pk=instance.pk)
		if qs.exists():
			raise forms.ValidationError("No admito slugs iguales") 
		return slug