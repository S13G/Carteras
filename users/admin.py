from django.contrib import admin

from users.models import Profile, Skill, Message

# Register your models here.

admin.site.register([Profile, Skill, Message])
