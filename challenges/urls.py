# Import necessary modules and views
from django.urls import path
from .views import GoalListView, GoalCreateView, GoalUpdateView, GoalDeleteView, ChallengeListView, DailyGoalTrackerView, CalendarView
from . import views  # Import additional views from the current directory

# Define the URL patterns for the application
urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Home view for the app, associated with the dashboard view
    path('signup/', views.signup, name='signup'),  # URL for user signup page
    path('login/', views.login_view, name='login'),  # URL for user login page
    path('logout/', views.logout_view, name='logout'),  # URL for user logout, triggers logout action and redirects to login page
    path('manage-whitelisted-emails/', views.manage_whitelisted_emails, name='manage-whitelisted-emails'),  # Admin-only view for managing whitelisted emails
    path('goals/', GoalListView.as_view(), name='goal-list'),  # URL for listing user goals using GoalListView class-based view
    path('goals/new/', GoalCreateView.as_view(), name='goal-create'),  # URL for creating new goals using GoalCreateView class-based view
    path('goals/<int:pk>/edit/', GoalUpdateView.as_view(), name='goal-edit'),  # URL for editing existing goals based on primary key (pk) using GoalUpdateView class-based view
    path('goals/<int:pk>/delete/', GoalDeleteView.as_view(), name='goal-delete'),  # URL for deleting goals based on primary key (pk) using GoalDeleteView class-based view
    path('challenges/', ChallengeListView.as_view(), name='challenge-list'),  # URL for listing user challenges using ChallengeListView class-based view
    path('daily-tracker/', DailyGoalTrackerView.as_view(), name='daily-goal-tracker'),  # URL for tracking daily goals using DailyGoalTrackerView class-based view
    path('calendar/', CalendarView.as_view(), name='calendar-view-default'),  # URL for viewing goals in a calendar format without specific year/month parameters
    path('calendar/<int:year>/<int:month>/', CalendarView.as_view(), name='calendar-view'),  # URL for viewing goals in a calendar format for a specific year and month
]
