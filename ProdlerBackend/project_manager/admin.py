from django.contrib import admin
from .models import Project, Issues, Milestones, Comments
# Register your models here.
admin.site.register(Project)
admin.site.register(Issues)
admin.site.register(Milestones)
admin.site.register(Comments)
