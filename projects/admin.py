from django.contrib import admin

from projects.models import Project, Review, Tag

# Register your models here.

admin.site.register([Project, Review, Tag])
