from django.contrib import admin
from .models import Asset, Project, Question, QuizScore, Payment


# ===============================
# 💰 ASSET
# ===============================
@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'is_verified', 'created_at', 'status')
    list_filter = ('category', 'is_verified', 'status')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)


# ===============================
# 🚀 PROJECT
# ===============================
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'owner', 'amount_needed', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('project_name', 'description')
    ordering = ('-created_at',)


# ===============================
# 🧠 QUIZ
# ===============================
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'correct_answer', 'points')


@admin.register(QuizScore)
class QuizScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'weekly_score', 'total_games', 'last_played')
    ordering = ('-score',)


# ===============================
# 💳 PAYMENT (IMPORTANT 🔥)
# ===============================
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'method', 'status', 'created_at')
    list_filter = ('status', 'method')
    search_fields = ('user__username', 'reference')
    ordering = ('-created_at',)
