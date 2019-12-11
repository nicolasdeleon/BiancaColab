from django.contrib import admin

# Register your models here.

from .models import BarPost, Fotos, PostRelations

admin.site.register(BarPost)
admin.site.register(Fotos)
admin.site.register(PostRelations)