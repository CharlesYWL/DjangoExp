from django.contrib import admin

from Insta.models import InstaUser, Post, Like, UserConnection, Comment
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'image', 'posted_on']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        obj.save()


admin.site.register(Post, PostAdmin)
admin.site.register(InstaUser)
admin.site.register(Like)
admin.site.register(UserConnection)
admin.site.register(Comment)
