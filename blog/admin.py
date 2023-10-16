from django.contrib import admin
from .models import Post, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    fields = ('name', 'slug', 'created', 'updated')
    readonly_fields = ('created', 'updated')
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'published')
    fields = ('title', 'slug', 'description', 'category', 'author', 'published', 'image', 'publish_date', "tag")
    readonly_fields = ('created', 'updated')
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("category", "author", "published")

admin.site.register(Tag)