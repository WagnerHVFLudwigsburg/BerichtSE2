from django.contrib import admin
from .models import Post, Comment, Events, CommentEvents

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Events)
admin.site.register(CommentEvents)

# Register your models here.
