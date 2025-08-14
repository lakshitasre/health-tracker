from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ], null=True, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Height in cm")
    activity_level = models.CharField(max_length=20, choices=[
        ('sedentary', 'Sedentary (little or no exercise)'),
        ('lightly_active', 'Lightly active (light exercise 1-3 days/week)'),
        ('moderately_active', 'Moderately active (moderate exercise 3-5 days/week)'),
        ('very_active', 'Very active (hard exercise 6-7 days/week)'),
        ('extremely_active', 'Extremely active (very hard exercise, physical job)')
    ], default='sedentary')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_bmi(self, weight):
        if self.height and weight:
            height_m = float(self.height) / 100
            weight_float = float(weight)
            return round(weight_float / (height_m ** 2), 2)
        return None

    def get_bmr(self, weight):
        """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
        if self.height and weight:
            weight_float = float(weight)
            height_float = float(self.height)
            age = self.get_age()
            if age:
                if self.gender == 'M':
                    return round(10 * weight_float + 6.25 * height_float - 5 * age + 5)
                elif self.gender == 'F':
                    return round(10 * weight_float + 6.25 * height_float - 5 * age - 161)
        return None

    def get_age(self):
        if self.date_of_birth:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None


class WeightEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(20), MaxValueValidator(500)])
    date = models.DateField(default=timezone.now)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        unique_together = ['user', 'date']

    def __str__(self):
        return f"{self.user.username} - {self.weight}kg on {self.date}"


class Exercise(models.Model):
    EXERCISE_TYPES = [
        ('cardio', 'Cardio'),
        ('strength', 'Strength Training'),
        ('flexibility', 'Flexibility'),
        ('sports', 'Sports'),
        ('other', 'Other')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_type = models.CharField(max_length=20, choices=EXERCISE_TYPES)
    name = models.CharField(max_length=100)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    calories_burned = models.PositiveIntegerField(help_text="Calories burned")
    date = models.DateField(default=timezone.now)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.name} on {self.date}"


class Nutrition(models.Model):
    MEAL_TYPES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    food_name = models.CharField(max_length=100)
    calories = models.PositiveIntegerField()
    protein = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, help_text="Protein in grams")
    carbs = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, help_text="Carbohydrates in grams")
    fat = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, help_text="Fat in grams")
    fiber = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, help_text="Fiber in grams")
    date = models.DateField(default=timezone.now)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.food_name} ({self.meal_type}) on {self.date}"


class Sleep(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sleep_time = models.DateTimeField(help_text="When you went to sleep")
    wake_time = models.DateTimeField(help_text="When you woke up")
    quality = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 11)], help_text="Sleep quality 1-10")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sleep_time']

    def __str__(self):
        return f"{self.user.username} - {self.sleep_time.date()} to {self.wake_time.date()}"

    @property
    def duration_hours(self):
        if self.sleep_time and self.wake_time:
            duration = self.wake_time - self.sleep_time
            return round(duration.total_seconds() / 3600, 1)
        return 0


class WaterIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(help_text="Amount in ml")
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.user.username} - {self.amount}ml on {self.date}"


class HealthGoal(models.Model):
    GOAL_TYPES = [
        ('weight', 'Weight Goal'),
        ('exercise', 'Exercise Goal'),
        ('nutrition', 'Nutrition Goal'),
        ('sleep', 'Sleep Goal'),
        ('water', 'Water Intake Goal'),
        ('general', 'General Health Goal')
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('paused', 'Paused')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    target_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    target_unit = models.CharField(max_length=20, blank=True)
    start_date = models.DateField(default=timezone.now)
    target_date = models.DateField()
    current_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    @property
    def progress_percentage(self):
        if self.target_value and self.current_value:
            return min(100, round((self.current_value / self.target_value) * 100, 1))
        return 0

    @property
    def is_overdue(self):
        return timezone.now().date() > self.target_date and self.status == 'active'


class Mood(models.Model):
    MOOD_CHOICES = [
        (1, '😢 Very Sad'),
        (2, '😞 Sad'),
        (3, '😐 Neutral'),
        (4, '🙂 Happy'),
        (5, '😄 Very Happy')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood = models.PositiveIntegerField(choices=MOOD_CHOICES)
    date = models.DateField(default=timezone.now)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        unique_together = ['user', 'date']

    def __str__(self):
        return f"{self.user.username} - Mood {self.mood} on {self.date}"


class Medication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=100)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.name}"


class HealthMetric(models.Model):
    METRIC_TYPES = [
        ('blood_pressure', 'Blood Pressure'),
        ('heart_rate', 'Heart Rate'),
        ('blood_sugar', 'Blood Sugar'),
        ('temperature', 'Body Temperature'),
        ('cholesterol', 'Cholesterol'),
        ('other', 'Other')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    metric_type = models.CharField(max_length=20, choices=METRIC_TYPES)
    value = models.CharField(max_length=100)
    unit = models.CharField(max_length=20, blank=True)
    date = models.DateField(default=timezone.now)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.metric_type}: {self.value} on {self.date}"
