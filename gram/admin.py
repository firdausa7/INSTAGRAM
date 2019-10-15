from django.contrib import admin
from .models import Comment,Post,Profile,Likes,Save,Follows
# Register your models here.
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Likes)
admin.site.register(Save)
admin.site.register(Follows)