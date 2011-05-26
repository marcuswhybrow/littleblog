from django.contrib import admin
from littleblog.posts.models import Post, Tag

admin.site.register(Post)
admin.site.register(Tag)

