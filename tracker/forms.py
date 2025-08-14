from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import (
    UserProfile, WeightEntry, Exercise, Nutrition, Sleep, 
    WaterIntake, HealthGoal, Mood, Medication, HealthMetric
)


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['date_of_birth', 'gender', 'height', 'activity_level']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '100', 'max': '250'}),
            'activity_level': forms.Select(attrs={'class': 'form-control'}),
        }


class WeightEntryForm(forms.ModelForm):
    class Meta:
        model = WeightEntry
        fields = ['weight', 'date', 'notes']
        widgets = {
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '20', 'max': '500'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['exercise_type', 'name', 'duration', 'calories_burned', 'date', 'notes']
        widgets = {
            'exercise_type': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '1440'}),
            'calories_burned': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '2000'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class NutritionForm(forms.ModelForm):
    class Meta:
        model = Nutrition
        fields = ['meal_type', 'food_name', 'calories', 'protein', 'carbs', 'fat', 'fiber', 'date', 'notes']
        widgets = {
            'meal_type': forms.Select(attrs={'class': 'form-control'}),
            'food_name': forms.TextInput(attrs={'class': 'form-control'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '5000'}),
            'protein': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '500'}),
            'carbs': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '1000'}),
            'fat': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '200'}),
            'fiber': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '100'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class SleepForm(forms.ModelForm):
    class Meta:
        model = Sleep
        fields = ['sleep_time', 'wake_time', 'quality', 'notes']
        widgets = {
            'sleep_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'wake_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'quality': forms.Select(choices=[(i, f"{i}/10") for i in range(1, 11)], attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        sleep_time = cleaned_data.get('sleep_time')
        wake_time = cleaned_data.get('wake_time')
        
        if sleep_time and wake_time and sleep_time >= wake_time:
            raise forms.ValidationError("Wake time must be after sleep time.")
        
        return cleaned_data


class WaterIntakeForm(forms.ModelForm):
    class Meta:
        model = WaterIntake
        fields = ['amount', 'date', 'time', 'notes']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'min': '50', 'max': '5000', 'step': '50'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class HealthGoalForm(forms.ModelForm):
    class Meta:
        model = HealthGoal
        fields = ['goal_type', 'title', 'description', 'target_value', 'target_unit', 'start_date', 'target_date']
        widgets = {
            'goal_type': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'target_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'target_unit': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'target_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        target_date = cleaned_data.get('target_date')
        
        if start_date and target_date and start_date >= target_date:
            raise forms.ValidationError("Target date must be after start date.")
        
        return cleaned_data


class MoodForm(forms.ModelForm):
    class Meta:
        model = Mood
        fields = ['mood', 'date', 'notes']
        widgets = {
            'mood': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['name', 'dosage', 'frequency', 'start_date', 'end_date', 'notes', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control'}),
            'frequency': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError("End date must be after start date.")
        
        return cleaned_data


class HealthMetricForm(forms.ModelForm):
    class Meta:
        model = HealthMetric
        fields = ['metric_type', 'value', 'unit', 'date', 'notes']
        widgets = {
            'metric_type': forms.Select(attrs={'class': 'form-control'}),
            'value': forms.TextInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class QuickAddForm(forms.Form):
    QUICK_ADD_CHOICES = [
        ('weight', 'Weight Entry'),
        ('exercise', 'Exercise'),
        ('nutrition', 'Food/Drink'),
        ('water', 'Water Intake'),
        ('mood', 'Mood Check'),
    ]
    
    action_type = forms.ChoiceField(
        choices=QUICK_ADD_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    value = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter value...'})
    )
    notes = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional notes...'})
    )
