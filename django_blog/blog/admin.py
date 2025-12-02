"""
from django.contrib import admin
from .models import Post, UserProfile

# Register the Post model
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_date")
    search_fields = ("title", "content", "author__username")
    list_filter = ("published_date", "author")

# Register the UserProfile model
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "bio", "profile_pic")
    search_fields = ("user__username", "bio")
"""
