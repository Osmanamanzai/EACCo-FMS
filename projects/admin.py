from django.contrib import admin
from .models import Project, ProjectDocument

class ProjectDocumentInline(admin.TabularInline):
    model = ProjectDocument
    extra = 0

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'budget', 'status', 'created_by', 'created_at')
    list_filter = ('status',)
    search_fields = ('name', 'location')
    inlines = [ProjectDocumentInline]

admin.site.register(Project, ProjectAdmin)