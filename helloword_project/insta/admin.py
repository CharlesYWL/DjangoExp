from django.contrib import admin

from Insta.models import InstaUser, Post
# Register your models here.
admin.site.register(Post)
admin.site.register(InstaUser)
