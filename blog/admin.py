from django.contrib import admin
from .models import Category, Tag, Post, Comment

# Admin for Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

# Admin for Tag
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Admin for Post
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'views', 'like_count', 'dislike_count', 'author', 'status', 'featured', 'publish_date', 'created_at', 'updated_at')
    list_filter = ('views', 'status', 'featured', 'categories', 'tags', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ('categories', 'tags',)
    filter_horizontal = ('categories', 'tags', 'likes', 'dislikes')
    raw_id_fields = ('author',)
    date_hierarchy = 'publish_date'
    actions = ['make_published']

    def make_published(self, request, queryset):
        queryset.update(status=Post.PUBLISHED)
    make_published.short_description = "Mark selected posts as published"

    # Custom method to display like count in the admin panel
    def like_count(self, obj):
        return obj.likes.count()
    like_count.short_description = 'Likes Count'
    
    # Custom method to display dislike count in the admin panel
    def dislike_count(self, obj):
        return obj.dislikes.count()
    dislike_count.short_description = 'Dislikes Count'

# Admin for Comment
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'content', 'created_at', 'approved')
    list_filter = ('approved', 'created_at')
    search_fields = ('author__username', 'content')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
    approve_comments.short_description = "Approve selected comments"
