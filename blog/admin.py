from django.contrib import admin
from .models import Category, Post, Comment, Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message_preview', 'is_read', 'sended_at')
    list_filter = ('is_read',)
    search_fields = ('name', 'email', 'message')

    def message_preview(self, obj):
        return obj.message[:50]
    message_preview.short_description = "Message Preview"

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Message, MessageAdmin)