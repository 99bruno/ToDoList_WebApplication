from django.contrib import admin
from .models import Task, TagTask

admin.site.register(Task)

admin.site.register(TagTask)
