from django.contrib import admin
from .models import Asset, Project

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'is_verified', 'created_at')
    list_filter = ('category', 'is_verified')
    search_fields = ('title', 'description')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'owner', 'amount_needed', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('project_name', 'description')

from .models import Question, QuizScore # Ajoute les imports

admin.site.register(Question)
admin.site.register(QuizScore)
