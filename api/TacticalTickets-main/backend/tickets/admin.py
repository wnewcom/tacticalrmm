from django.contrib import admin
from .models import Category, Ticket, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'color', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ['created_at']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'priority', 'status', 'category', 'created_by', 'assigned_to', 'created_at']
    list_filter = ['status', 'priority', 'category', 'created_at']
    search_fields = ['title', 'description']
    raw_id_fields = ['created_by', 'assigned_to']
    inlines = [CommentInline]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority', 'due_date')
        }),
        ('Assignment', {
            'fields': ('created_by', 'assigned_to')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'author', 'created_at', 'is_internal']
    list_filter = ['is_internal', 'created_at']
    search_fields = ['content', 'ticket__title']
    raw_id_fields = ['ticket', 'author']