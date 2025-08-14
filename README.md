# 🏥 Health Tracker

A comprehensive Django-based health and wellness tracking application that helps users monitor their health metrics, set goals, and track progress over time.

## ✨ Features

### 🎯 Core Functionality
- **Weight Tracking**: Monitor weight changes with BMI calculations and trend analysis
- **Exercise Logging**: Track workouts, duration, and calories burned
- **Nutrition Monitoring**: Log meals and track macronutrients (protein, carbs, fat, fiber)
- **Sleep Analysis**: Monitor sleep patterns, quality, and duration
- **Hydration Tracking**: Track daily water intake
- **Mood Monitoring**: Daily mood check-ins with notes
- **Goal Setting**: Set and track health goals with progress visualization
- **Health Metrics**: Track blood pressure, heart rate, blood sugar, and more

### 🎨 User Experience
- **Beautiful Dashboard**: Modern, responsive design with Bootstrap 5
- **Real-time Analytics**: Charts and progress tracking
- **Quick Actions**: Fast entry forms for common activities
- **Mobile Responsive**: Works perfectly on all devices
- **User Profiles**: Personalized health profiles with activity levels

### 🔒 Security & Privacy
- **User Authentication**: Secure login and registration system
- **Data Privacy**: Individual user data isolation
- **Admin Panel**: Comprehensive admin interface for data management

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/lakshitasre/health_tracker.git
   cd health_tracker
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Open your browser**
   Navigate to `http://127.0.0.1:8000/`

## 📱 Usage

### Getting Started
1. **Register** for a new account or **login** if you already have one
2. **Complete your profile** with basic health information
3. **Start tracking** your health metrics using the dashboard
4. **Set goals** and monitor your progress
5. **Use quick actions** for fast data entry

### Key Features
- **Dashboard**: Overview of today's health status
- **Weight Tracker**: Log weight entries and view trends
- **Exercise Logger**: Record workouts and track calories
- **Nutrition Tracker**: Monitor food intake and macronutrients
- **Sleep Monitor**: Track sleep quality and duration
- **Water Intake**: Stay hydrated with daily tracking
- **Mood Check-ins**: Monitor emotional well-being
- **Goal Management**: Set and achieve health objectives

## 🛠️ Technology Stack

- **Backend**: Django 5.0.3
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Database**: SQLite (development), PostgreSQL (production)
- **Charts**: Chart.js
- **Icons**: Bootstrap Icons
- **Deployment**: Render, Heroku ready

## 📊 Database Models

The application includes comprehensive models for:
- User profiles and authentication
- Weight entries and BMI calculations
- Exercise logging and calorie tracking
- Nutrition and meal planning
- Sleep patterns and quality
- Water intake monitoring
- Health goals and progress
- Mood tracking
- Health metrics (blood pressure, heart rate, etc.)

## 🚀 Deployment

### Render Deployment

1. **Fork/Clone** this repository to your GitHub account
2. **Connect** your repository to Render
3. **Create a new Web Service**
4. **Configure** the following:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn health_tracker.wsgi:application`
   - **Environment Variables**: Set `DEBUG=False` and `SECRET_KEY`

### Environment Variables
```bash
DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=your-database-url
ALLOWED_HOSTS=your-domain.com
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django community for the excellent framework
- Bootstrap team for the beautiful UI components
- Chart.js for the interactive charts
- All contributors who help improve this project

## 📞 Support

If you have any questions or need help:
- Create an issue on GitHub
- Contact: [Your Contact Information]

## 🔮 Future Enhancements

- [ ] Mobile app (React Native/Flutter)
- [ ] Social features and challenges
- [ ] Integration with fitness devices
- [ ] Advanced analytics and AI insights
- [ ] Meal planning and recipes
- [ ] Workout plans and routines
- [ ] Health reminders and notifications

---

**Made with ❤️ for better health tracking**
