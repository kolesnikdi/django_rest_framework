"""
add blog.models(Post) to the admin site
"""
from django.contrib import admin

from blog.models import Post

admin.site.register(Post)
