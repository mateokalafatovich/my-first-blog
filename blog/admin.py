from django.contrib import admin
from django.utils.text import slugify
from .models import Post, Comment, Like, Tag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_date', 'published_date', 'get_tags']
    list_filter = ['created_date', 'published_date', 'author', 'tags']
    search_fields = ['title', 'text']
    filter_horizontal = ['tags']  # Makes tag selection easier
    
    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    get_tags.short_description = 'Tags'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'get_post_count', 'created_date']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    
    def get_post_count(self, obj):
        return obj.get_post_count()
    get_post_count.short_description = 'Post Count'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_date', 'approved']
    list_filter = ['approved', 'created_date']
    search_fields = ['author__username', 'post__title', 'content']
    actions = ['approve_comments', 'disapprove_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
    approve_comments.short_description = "Mark selected comments as approved"
    
    def disapprove_comments(self, request, queryset):
        queryset.update(approved=False)
    disapprove_comments.short_description = "Mark selected comments as not approved"

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_date']
    list_filter = ['created_date']
    search_fields = ['user__username', 'post__title']