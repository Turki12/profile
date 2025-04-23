from django.contrib import admin
from .models import Project,Certificate,ContactMessage
# Register your models here.
admin.site.register(Project)
admin.site.register(Certificate)
admin.site.register(ContactMessage)