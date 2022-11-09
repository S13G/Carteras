from django.contrib import admin

from users.models import Profile, Skill

# Register your models here.

admin.site.register([Profile, Skill])
