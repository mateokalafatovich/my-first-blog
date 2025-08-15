from django.contrib import admin
from .models import Post, Comment, Like

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_date', 'published_date']
    list_filter = ['created_date', 'published_date', 'author']
    search_fields = ['title', 'text']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_date', 'approved']
    list_filter = ['approved', 'created_date']
    search_fields = ['author__username', 'post__title', 'content']
    actions = ['approve_comments', 'disapprove_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
    
    def disapprove_comments(self, request, queryset):
        queryset.update(approved=False)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_date']
    list_filter = ['created_date']