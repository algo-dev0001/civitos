from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post', 'created_at', 'flagged')
    list_filter = ('flagged', 'created_at')
    search_fields = ('author', 'text')
    readonly_fields = ('created_at',)
