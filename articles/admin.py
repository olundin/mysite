from django.contrib import admin

from .models import Article, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Content", {"fields": ["title", "text"]}),
        ("Date information", {"fields": ["date_published", "date_modified"], "classes": ["collapse"]})
    ]
    readonly_fields = ("date_modified",)
    inlines = [CommentInline]
    list_display = ("title", "date_published", "date_modified")
    list_filter = ["date_published", "date_modified"]
    search_fields = ["title", "text"]

admin.site.register(Article, ArticleAdmin)
