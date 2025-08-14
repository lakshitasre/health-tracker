from django.contrib import admin
from django.utils.html import format_html
from .models import (
    UserProfile, WeightEntry, Exercise, Nutrition, Sleep, 
    WaterIntake, HealthGoal, Mood, Medication, HealthMetric
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'height', 'activity_level', 'get_age', 'created_at']
    list_filter = ['gender', 'activity_level', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(WeightEntry)
class WeightEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'weight', 'date', 'get_bmi', 'created_at']
    list_filter = ['date', 'created_at']
    search_fields = ['user__username', 'notes']
    readonly_fields = ['created_at']
    date_hierarchy = 'date'

    def get_bmi(self, obj):
        if obj.user.profile.height:
            bmi = obj.user.profile.get_bmi(obj.weight)
            if bmi:
                if bmi < 18.5:
                    color = 'red'
                elif bmi < 25:
                    color = 'green'
                elif bmi < 30:
                    color = 'orange'
                else:
                    color = 'red'
                return format_html('<span style="color: {};">{}</span>', color, bmi)
        return '-'
    get_bmi.short_description = 'BMI'


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['user', 'exercise_type', 'name', 'duration', 'calories_burned', 'date']
    list_filter = ['exercise_type', 'date', 'created_at']
    search_fields = ['user__username', 'name', 'notes']
    readonly_fields = ['created_at']
    date_hierarchy = 'date'


@admin.register(Nutrition)
class NutritionAdmin(admin.ModelAdmin):
    list_display = ['user', 'meal_type', 'food_name', 'calories', 'protein', 'carbs', 'fat', 'date']
    list_filter = ['meal_type', 'date', 'created_at']
    search_fields = ['user__username', 'food_name', 'notes']
    readonly_fields = ['created_at']
    date_hierarchy = 'date'


@admin.register(Sleep)
class SleepAdmin(admin.ModelAdmin):
    list_display = ['user', 'sleep_time', 'wake_time', 'duration_hours', 'quality']
    list_filter = ['quality', 'sleep_time', 'created_at']
    search_fields = ['user__username', 'notes']
    readonly_fields = ['created_at', 'duration_hours']
    date_hierarchy = 'sleep_time'


@admin.register(WaterIntake)
class WaterIntakeAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'date', 'time', 'get_liters']
    list_filter = ['date', 'created_at']
    search_fields = ['user__username', 'notes']
    readonly_fields = ['created_at']
    date_hierarchy = 'date'

    def get_liters(self, obj):
        return f"{obj.amount / 1000:.1f}L"
    get_liters.short_description = 'Amount (L)'


@admin.register(HealthGoal)
class HealthGoalAdmin(admin.ModelAdmin):
    list_display = ['user', 'goal_type', 'title', 'target_value', 'current_value', 'progress_percentage', 'status', 'target_date']
    list_filter = ['goal_type', 'status', 'target_date', 'created_at']
    search_fields = ['user__username', 'title', 'description']
    readonly_fields = ['created_at', 'updated_at', 'progress_percentage']
    date_hierarchy = 'target_date'

    def progress_percentage(self, obj):
        percentage = obj.progress_percentage
        if percentage >= 80:
            color = 'green'
        elif percentage >= 50:
            color = 'orange'
        else:
            color = 'red'
        return format_html('<span style="color: {};">{}%</span>', color, percentage)
    progress_percentage.short_description = 'Progress'


@admin.register(Mood)
class MoodAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_mood_emoji', 'date', 'created_at']
    list_filter = ['mood', 'date', 'created_at']
    search_fields = ['user__username', 'notes']
    readonly_fields = ['created_at']
    date_hierarchy = 'date'

    def get_mood_emoji(self, obj):
        emoji_map = {1: '😢', 2: '😞', 3: '😐', 4: '🙂', 5: '😄'}
        return emoji_map.get(obj.mood, '')
    get_mood_emoji.short_description = 'Mood'


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'dosage', 'frequency', 'start_date', 'end_date', 'is_active']
    list_filter = ['is_active', 'start_date', 'created_at']
    search_fields = ['user__username', 'name', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'start_date'


@admin.register(HealthMetric)
class HealthMetricAdmin(admin.ModelAdmin):
    list_display = ['user', 'metric_type', 'value', 'unit', 'date', 'created_at']
    list_filter = ['metric_type', 'date', 'created_at']
    search_fields = ['user__username', 'value', 'notes']
    readonly_fields = ['created_at']
    date_hierarchy = 'date'
