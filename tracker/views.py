from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.db.models import Sum, Avg, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import *
from .forms import *
import json


def home(request):
    if request.user.is_authenticated:
        return redirect('tracker:dashboard')
    return render(request, 'tracker/home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'tracker/register.html', {'form': form})


@login_required
def dashboard(request):
    today = timezone.now().date()
    user = request.user
    
    # Get today's data
    try:
        today_weight = WeightEntry.objects.filter(user=user, date=today).latest('created_at')
    except WeightEntry.DoesNotExist:
        today_weight = None
    
    try:
        today_mood = Mood.objects.get(user=user, date=today)
    except Mood.DoesNotExist:
        today_mood = None
    
    # Get recent data
    recent_weight = WeightEntry.objects.filter(user=user).order_by('-date')[:7]
    recent_exercise = Exercise.objects.filter(user=user).order_by('-date')[:5]
    recent_nutrition = Nutrition.objects.filter(user=user).order_by('-date')[:5]
    
    # Calculate today's totals
    today_exercise_calories = Exercise.objects.filter(user=user, date=today).aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0
    today_nutrition_calories = Nutrition.objects.filter(user=user, date=today).aggregate(Sum('calories'))['calories__sum'] or 0
    today_water = WaterIntake.objects.filter(user=user, date=today).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Get active goals
    active_goals = HealthGoal.objects.filter(user=user, status='active').order_by('target_date')[:5]
    
    context = {
        'today_weight': today_weight,
        'today_mood': today_mood,
        'recent_weight': recent_weight,
        'recent_exercise': recent_exercise,
        'recent_nutrition': recent_nutrition,
        'today_exercise_calories': today_exercise_calories,
        'today_nutrition_calories': today_nutrition_calories,
        'today_water': today_water,
        'active_goals': active_goals,
    }
    
    return render(request, 'tracker/dashboard.html', context)


@login_required
def weight_tracker(request):
    if request.method == 'POST':
        form = WeightEntryForm(request.POST)
        if form.is_valid():
            weight_entry = form.save(commit=False)
            weight_entry.user = request.user
            weight_entry.save()
            messages.success(request, 'Weight entry added successfully!')
            return redirect('tracker:weight_tracker')
    else:
        form = WeightEntryForm()
    
    weight_entries = WeightEntry.objects.filter(user=request.user).order_by('-date')
    paginator = Paginator(weight_entries, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculate statistics
    if weight_entries.exists():
        latest_weight = weight_entries.first().weight
        first_weight = weight_entries.last().weight
        weight_change = latest_weight - first_weight
        avg_weight = weight_entries.aggregate(Avg('weight'))['weight__avg']
    else:
        latest_weight = first_weight = weight_change = avg_weight = None
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'latest_weight': latest_weight,
        'first_weight': first_weight,
        'weight_change': weight_change,
        'avg_weight': avg_weight,
    }
    
    return render(request, 'tracker/weight_tracker.html', context)


@login_required
def exercise_tracker(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.user = request.user
            exercise.save()
            messages.success(request, 'Exercise logged successfully!')
            return redirect('tracker:exercise_tracker')
    else:
        form = ExerciseForm()
    
    exercises = Exercise.objects.filter(user=request.user).order_by('-date')
    paginator = Paginator(exercises, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculate statistics
    total_exercises = exercises.count()
    total_calories = exercises.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0
    total_duration = exercises.aggregate(Sum('duration'))['duration__sum'] or 0
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'total_exercises': total_exercises,
        'total_calories': total_calories,
        'total_duration': total_duration,
    }
    
    return render(request, 'tracker/exercise_tracker.html', context)


@login_required
def nutrition_tracker(request):
    if request.method == 'POST':
        form = NutritionForm(request.POST)
        if form.is_valid():
            nutrition = form.save(commit=False)
            nutrition.user = request.user
            nutrition.save()
            messages.success(request, 'Food logged successfully!')
            return redirect('tracker:nutrition_tracker')
    else:
        form = NutritionForm()
    
    nutrition_entries = Nutrition.objects.filter(user=request.user).order_by('-date')
    paginator = Paginator(nutrition_entries, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculate today's totals
    today = timezone.now().date()
    today_nutrition = nutrition_entries.filter(date=today)
    today_calories = today_nutrition.aggregate(Sum('calories'))['calories__sum'] or 0
    today_protein = today_nutrition.aggregate(Sum('protein'))['protein__sum'] or 0
    today_carbs = today_nutrition.aggregate(Sum('carbs'))['carbs__sum'] or 0
    today_fat = today_nutrition.aggregate(Sum('fat'))['fat__sum'] or 0
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'today_calories': today_calories,
        'today_protein': today_protein,
        'today_carbs': today_carbs,
        'today_fat': today_fat,
    }
    
    return render(request, 'tracker/nutrition_tracker.html', context)


@login_required
def sleep_tracker(request):
    if request.method == 'POST':
        form = SleepForm(request.POST)
        if form.is_valid():
            sleep = form.save(commit=False)
            sleep.user = request.user
            sleep.save()
            messages.success(request, 'Sleep logged successfully!')
            return redirect('tracker:sleep_tracker')
    else:
        form = SleepForm()
    
    sleep_entries = Sleep.objects.filter(user=request.user).order_by('-sleep_time')
    paginator = Paginator(sleep_entries, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculate statistics
    total_sleep_entries = sleep_entries.count()
    avg_sleep_quality = sleep_entries.aggregate(Avg('quality'))['quality__avg'] or 0
    
    # Calculate average sleep duration manually since it's a property
    total_duration = 0
    valid_entries = 0
    for entry in sleep_entries:
        if entry.sleep_time and entry.wake_time:
            total_duration += entry.duration_hours
            valid_entries += 1
    
    avg_sleep_duration = round(total_duration / valid_entries, 1) if valid_entries > 0 else 0
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'total_sleep_entries': total_sleep_entries,
        'avg_sleep_quality': avg_sleep_quality,
        'avg_sleep_duration': avg_sleep_duration,
    }
    
    return render(request, 'tracker/sleep_tracker.html', context)


@login_required
def water_tracker(request):
    if request.method == 'POST':
        form = WaterIntakeForm(request.POST)
        if form.is_valid():
            water = form.save(commit=False)
            water.user = request.user
            water.save()
            messages.success(request, 'Water intake logged successfully!')
            return redirect('tracker:water_tracker')
    else:
        form = WaterIntakeForm()
    
    water_entries = WaterIntake.objects.filter(user=request.user).order_by('-date', '-time')
    paginator = Paginator(water_entries, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculate today's total
    today = timezone.now().date()
    today_water = water_entries.filter(date=today).aggregate(Sum('amount'))['amount__sum'] or 0
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'today_water': today_water,
        'today': today,
        'now': timezone.now(),
    }
    
    return render(request, 'tracker/water_tracker.html', context)


@login_required
def goals(request):
    if request.method == 'POST':
        form = HealthGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, 'Goal created successfully!')
            return redirect('tracker:goals')
    else:
        form = HealthGoalForm()
    
    active_goals = HealthGoal.objects.filter(user=request.user, status='active').order_by('target_date')
    completed_goals = HealthGoal.objects.filter(user=request.user, status='completed').order_by('-updated_at')
    paused_goals = HealthGoal.objects.filter(user=request.user, status='paused').order_by('-updated_at')
    
    context = {
        'form': form,
        'active_goals': active_goals,
        'completed_goals': completed_goals,
        'paused_goals': paused_goals,
    }
    
    return render(request, 'tracker/goals.html', context)


@login_required
def mood_tracker(request):
    if request.method == 'POST':
        form = MoodForm(request.POST)
        if form.is_valid():
            mood = form.save(commit=False)
            mood.user = request.user
            mood.save()
            messages.success(request, 'Mood logged successfully!')
            return redirect('tracker:mood_tracker')
    else:
        form = MoodForm()
    
    mood_entries = Mood.objects.filter(user=request.user).order_by('-date')
    paginator = Paginator(mood_entries, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculate statistics
    total_mood_entries = mood_entries.count()
    avg_mood = mood_entries.aggregate(Avg('mood'))['mood__avg'] or 0
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'total_mood_entries': total_mood_entries,
        'avg_mood': avg_mood,
        'today': timezone.now().date(),
    }
    
    return render(request, 'tracker/mood_tracker.html', context)


@login_required
def profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('tracker:profile')
    else:
        form = UserProfileForm(instance=profile)
    
    # Get user statistics
    user = request.user
    total_weight_entries = WeightEntry.objects.filter(user=user).count()
    total_exercises = Exercise.objects.filter(user=user).count()
    total_nutrition_entries = Nutrition.objects.filter(user=user).count()
    total_sleep_entries = Sleep.objects.filter(user=user).count()
    total_goals = HealthGoal.objects.filter(user=user).count()
    
    # Get latest weight for BMI calculation
    try:
        latest_weight = WeightEntry.objects.filter(user=user).latest('date').weight
        bmi = profile.get_bmi(latest_weight)
        bmr = profile.get_bmr(latest_weight)
    except WeightEntry.DoesNotExist:
        bmi = bmr = None
    
    context = {
        'form': form,
        'profile': profile,
        'total_weight_entries': total_weight_entries,
        'total_exercises': total_exercises,
        'total_nutrition_entries': total_nutrition_entries,
        'total_sleep_entries': total_sleep_entries,
        'total_goals': total_goals,
        'bmi': bmi,
        'bmr': bmr,
    }
    
    return render(request, 'tracker/profile.html', context)


@login_required
def analytics(request):
    user = request.user
    today = timezone.now().date()
    
    # Date range for analytics
    days = request.GET.get('days', 30)
    try:
        days = int(days)
    except ValueError:
        days = 30
    
    start_date = today - timedelta(days=days)
    
    # Weight analytics
    weight_data = WeightEntry.objects.filter(
        user=user, 
        date__range=[start_date, today]
    ).order_by('date')
    
    # Exercise analytics
    exercise_data = Exercise.objects.filter(
        user=user, 
        date__range=[start_date, today]
    ).order_by('date')
    
    # Nutrition analytics
    nutrition_data = Nutrition.objects.filter(
        user=user, 
        date__range=[start_date, today]
    ).order_by('date')
    
    # Calculate weight change
    weight_change = None
    if weight_data.exists():
        first_weight = weight_data.first().weight
        last_weight = weight_data.last().weight
        weight_change = last_weight - first_weight
    
    context = {
        'days': days,
        'weight_data': weight_data,
        'exercise_data': exercise_data,
        'nutrition_data': nutrition_data,
        'start_date': start_date,
        'today': today,
        'weight_change': weight_change,
    }
    
    return render(request, 'tracker/analytics.html', context)


@login_required
def quick_add(request):
    if request.method == 'POST':
        form = QuickAddForm(request.POST)
        if form.is_valid():
            action_type = form.cleaned_data['action_type']
            value = form.cleaned_data['value']
            notes = form.cleaned_data['notes']
            
            try:
                if action_type == 'weight':
                    weight = float(value)
                    WeightEntry.objects.create(
                        user=request.user,
                        weight=weight,
                        notes=notes
                    )
                    messages.success(request, f'Weight {weight}kg logged successfully!')
                
                elif action_type == 'exercise':
                    Exercise.objects.create(
                        user=request.user,
                        exercise_type='other',
                        name=value,
                        duration=30,
                        calories_burned=150,
                        notes=notes
                    )
                    messages.success(request, f'Exercise "{value}" logged successfully!')
                
                elif action_type == 'nutrition':
                    Nutrition.objects.create(
                        user=request.user,
                        meal_type='snack',
                        food_name=value,
                        calories=100,
                        notes=notes
                    )
                    messages.success(request, f'Food "{value}" logged successfully!')
                
                elif action_type == 'water':
                    amount = int(value)
                    WaterIntake.objects.create(
                        user=request.user,
                        amount=amount,
                        notes=notes
                    )
                    messages.success(request, f'{amount}ml water logged successfully!')
                
                elif action_type == 'mood':
                    mood_value = int(value)
                    if 1 <= mood_value <= 5:
                        Mood.objects.create(
                            user=request.user,
                            mood=mood_value,
                            notes=notes
                        )
                        messages.success(request, 'Mood logged successfully!')
                    else:
                        messages.error(request, 'Mood must be between 1 and 5')
                
            except (ValueError, TypeError):
                messages.error(request, 'Invalid value format')
            
            return redirect('tracker:dashboard')
    
    # If it's a GET request or form is invalid
    form = QuickAddForm()
    context = {'form': form}
    return render(request, 'tracker/quick_add.html', context)


@login_required
def edit_entry(request, model_name, entry_id):
    model_map = {
        'weight': WeightEntry,
        'exercise': Exercise,
        'nutrition': Nutrition,
        'sleep': Sleep,
        'water': WaterIntake,
        'mood': Mood,
        'goal': HealthGoal,
    }
    
    form_map = {
        'weight': WeightEntryForm,
        'exercise': ExerciseForm,
        'nutrition': NutritionForm,
        'sleep': SleepForm,
        'water': WaterIntakeForm,
        'mood': MoodForm,
        'goal': HealthGoalForm,
    }
    
    if model_name not in model_map:
        messages.error(request, 'Invalid model type')
        return redirect('tracker:dashboard')
    
    Model = model_map[model_name]
    FormClass = form_map[model_name]
    
    entry = get_object_or_404(Model, id=entry_id, user=request.user)
    
    if request.method == 'POST':
        form = FormClass(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, f'{model_name.title()} updated successfully!')
            return redirect(f'tracker:{model_name}_tracker')
    else:
        form = FormClass(instance=entry)
    
    context = {
        'form': form,
        'entry': entry,
        'model_name': model_name,
    }
    
    return render(request, 'tracker/edit_entry.html', context)


@login_required
def delete_entry(request, model_name, entry_id):
    model_map = {
        'weight': WeightEntry,
        'exercise': Exercise,
        'nutrition': Nutrition,
        'sleep': Sleep,
        'water': WaterIntake,
        'mood': Mood,
        'goal': HealthGoal,
    }
    
    if model_name not in model_map:
        messages.error(request, 'Invalid model type')
        return redirect('tracker:dashboard')
    
    Model = model_map[model_name]
    entry = get_object_or_404(Model, id=entry_id, user=request.user)
    
    if request.method == 'POST':
        entry.delete()
        messages.success(request, f'{model_name.title()} deleted successfully!')
        return redirect(f'tracker:{model_name}_tracker')
    
    context = {
        'entry': entry,
        'model_name': model_name,
    }
    
    return render(request, 'tracker/delete_entry.html', context)


@login_required
def get_chart_data(request):
    days = int(request.GET.get('days', 30))
    today = timezone.now().date()
    start_date = today - timedelta(days=days)
    
    # Weight data
    weight_data = WeightEntry.objects.filter(
        user=request.user,
        date__range=[start_date, today]
    ).order_by('date').values('date', 'weight')
    
    # Exercise data
    exercise_data = Exercise.objects.filter(
        user=request.user,
        date__range=[start_date, today]
    ).order_by('date').values('date').annotate(
        total_duration=Sum('duration'),
        total_calories=Sum('calories_burned')
    )
    
    # Water data
    water_data = WaterIntake.objects.filter(
        user=request.user,
        date__range=[start_date, today]
    ).order_by('date').values('date').annotate(total_amount=Sum('amount'))
    
    return JsonResponse({
        'weight_data': list(weight_data),
        'exercise_data': list(exercise_data),
        'water_data': list(water_data),
    })
