# Import necessary modules for handling class-based views and HTTP responses
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.utils.timezone import now
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Goal, Challenge, GoalCompletion, WhitelistedEmail
from .forms import WhitelistedEmailForm, CustomSignupForm
from datetime import timedelta, datetime
from django.db.models import Count, Q
from django.contrib.auth.models import User
import calendar

# Define a decorator to restrict access to admin users only
def admin_required(function=None):
    """Decorator that restricts view access to only superuser/admin users."""
    def _decorator(view_func):
        # Use `user_passes_test` to ensure that the user is a superuser
        decorated_view_func = user_passes_test(lambda u: u.is_superuser, login_url='/')(view_func)
        return decorated_view_func
    if function:
        return _decorator(function)
    return _decorator

@admin_required
def manage_whitelisted_emails(request):
    """
    View to manage whitelisted emails. Only accessible by admin users.
    Allows the admin to view and update the list of whitelisted emails.
    """
    emails = WhitelistedEmail.objects.all()

    if request.method == 'POST':
        email = request.POST.get('email')
        active = request.POST.get('active') == 'on'
        # Create or update the whitelisted email based on the form submission
        WhitelistedEmail.objects.update_or_create(email=email, defaults={'active': active})
        return redirect('manage-whitelisted-emails')

    context = {'emails': emails}
    return render(request, 'challenges/manage_whitelisted_emails.html', context)

def signup(request):
    """
    View to handle user signups.
    - Displays a form for new users to sign up.
    - On successful signup, logs the user in and redirects to the dashboard.
    """
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in automatically after signup
            return redirect('dashboard')
    else:
        form = CustomSignupForm()
    return render(request, 'challenges/signup.html', {'form': form})

def login_view(request):
    """
    View to handle user logins.
    - Displays a form for existing users to log in.
    - On successful login, redirects to the dashboard.
    - Shows an error message if the login credentials are invalid.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'challenges/login.html', {'error': 'Invalid username or password.'})
    return render(request, 'challenges/login.html')

def logout_view(request):
    """
    View to handle user logouts.
    - Logs the user out and redirects to the login page.
    """
    logout(request)
    return redirect('login')

def dashboard(request):
    """
    Dashboard view displaying the user's monthly and weekly goal completion percentages.
    - Calculates the percentage of completed goals for the current week and month.
    - Displays individual goal statistics for the current month and week.
    """
    today = now().date()

    # Calculate start and end of the current week (Monday to Sunday)
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    # Calculate start and end of the current month
    start_of_month = today.replace(day=1)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    # Fetch all goals for the current user
    goals = Goal.objects.filter(user=request.user)

    # Calculate monthly completion percentage
    monthly_completions = GoalCompletion.objects.filter(goal__in=goals, date__gte=start_of_month, date__lte=today, completed=True).count()
    total_monthly_goals = GoalCompletion.objects.filter(goal__in=goals, date__gte=start_of_month, date__lte=today).count()
    monthly_completion_percentage = (monthly_completions / total_monthly_goals) * 100 if total_monthly_goals else 0

    # Calculate weekly completion percentage
    weekly_completions = GoalCompletion.objects.filter(goal__in=goals, date__gte=start_of_week, date__lte=today, completed=True).count()
    total_weekly_goals = GoalCompletion.objects.filter(goal__in=goals, date__gte=start_of_week, date__lte=today).count()
    weekly_completion_percentage = (weekly_completions / total_weekly_goals) * 100 if total_weekly_goals else 0

    # Calculate individual goal statistics for display in the dashboard table
    goal_stats = []
    for goal in goals:
        # Calculate month-to-date stats for each goal
        month_to_date_goal_completions = GoalCompletion.objects.filter(goal=goal, date__gte=start_of_month, date__lte=today, completed=True).count()
        month_to_date_total_goal_days = GoalCompletion.objects.filter(goal=goal, date__gte=start_of_month, date__lte=today).count()
        month_to_date_completion_percentage = (month_to_date_goal_completions / month_to_date_total_goal_days) * 100 if month_to_date_total_goal_days else 0

        # Calculate week-to-date stats for each goal
        week_to_date_goal_completions = GoalCompletion.objects.filter(goal=goal, date__gte=start_of_week, date__lte=today, completed=True).count()
        week_to_date_total_goal_days = GoalCompletion.objects.filter(goal=goal, date__gte=start_of_week, date__lte=today).count()
        week_to_date_completion_percentage = (week_to_date_goal_completions / week_to_date_total_goal_days) * 100 if week_to_date_total_goal_days else 0

        # Append goal stats to the list
        goal_stats.append({
            'goal_name': goal.name,
            'month_to_date_days_set': month_to_date_total_goal_days,
            'month_to_date_days_completed': month_to_date_goal_completions,
            'month_to_date_percentage': round(month_to_date_completion_percentage, 1),
            'week_to_date_days_set': week_to_date_total_goal_days,
            'week_to_date_days_completed': week_to_date_goal_completions,
            'week_to_date_percentage': round(week_to_date_completion_percentage, 1),
        })

    # Pass the calculated stats to the template
    context = {
        'today': today,
        'monthly_completion_percentage': round(monthly_completion_percentage, 1),
        'weekly_completion_percentage': round(weekly_completion_percentage, 1),
        'goal_stats': goal_stats,
    }

    return render(request, 'challenges/dashboard.html', context)

@login_required(login_url='login')
def LeaderboardView(request):
    """
    View to display the leaderboard for the current month-to-date.
    Users are ranked by the percentage of their set goals completed,
    with a secondary sort by the total number of goals completed.
    """
    
    # Get the current date
    today = now().date()

    # Get the start of the current month by setting the day to 1
    start_of_month = today.replace(day=1)

    # Annotate users with counts for set goals and completed goals for the current month
    users = User.objects.annotate(
        total_goals_set=Count(
            'goal__goalcompletion',  # Count the number of goal completions related to each user's goals
            filter=Q(goal__goalcompletion__date__gte=start_of_month)  # Filter goal completions for the current month
        ),
        total_goals_completed=Count(
            'goal__goalcompletion',  # Count the number of completed goals
            filter=Q(goal__goalcompletion__date__gte=start_of_month, goal__goalcompletion__completed=True)  # Filter completed goals for the current month
        )
    ).filter(total_goals_set__gt=0)  # Filter out users with no goals set

    # Prepare the leaderboard data by calculating the completion percentage for each user
    leaderboard_data = []
    for user in users:
        if user.total_goals_set > 0:
            # Calculate the completion percentage
            completion_percentage = (user.total_goals_completed / user.total_goals_set) * 100
        else:
            completion_percentage = 0  # If no goals are set, the percentage is 0
        # Append each user's data to the leaderboard
        leaderboard_data.append({
            'user': user,
            'completion_percentage': round(completion_percentage, 1),  # Round the percentage to one decimal place
            'total_goals_set': user.total_goals_set,  # Total goals set for the month
            'total_goals_completed': user.total_goals_completed  # Total goals completed for the month
        })

    # Sort the leaderboard primarily by completion percentage (descending), and secondarily by total goals completed (descending)
    leaderboard_data.sort(key=lambda x: (-x['completion_percentage'], -x['total_goals_completed']))

    # Assign ranking numbers to each user in the sorted leaderboard
    for index, user_data in enumerate(leaderboard_data, start=1):
        user_data['rank'] = index

    # Create the context with leaderboard data
    context = {
        'leaderboard_data': leaderboard_data,
    }

    # Render the leaderboard template and pass the context
    return render(request, 'challenges/leaderboard.html', context)

# List view of all user goals, using a class-based view pattern
@method_decorator(login_required(login_url='login'), name='dispatch')
class GoalListView(ListView):
    """Displays a list of goals for the logged-in user."""
    model = Goal
    template_name = 'challenges/goal_list.html'
    context_object_name = 'goals'

    def get_queryset(self):
        """Fetches the goals associated with the current logged-in user."""
        return Goal.objects.filter(user=self.request.user)

# View for creating a new goal
@method_decorator(login_required(login_url='login'), name='dispatch')
class GoalCreateView(CreateView):
    """Allows the user to create a new goal."""
    model = Goal
    template_name = 'challenges/goal_form.html'
    fields = ['name', 'description', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    success_url = '/goals/'

    def form_valid(self, form):
        """Automatically associates the new goal with the logged-in user."""
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Adds a custom title to the goal creation form."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Goal'
        return context

# Update existing goal view
@method_decorator(login_required(login_url='login'), name='dispatch')
class GoalUpdateView(UpdateView):
    """Allows the user to update an existing goal."""
    model = Goal
    template_name = 'challenges/goal_form.html'
    fields = ['name', 'description', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    success_url = '/goals/'

    def get_context_data(self, **kwargs):
        """Adds a custom title to the goal update form."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Goal'
        return context

# View for deleting a goal
@method_decorator(login_required(login_url='login'), name='dispatch')
class GoalDeleteView(DeleteView):
    """Allows the user to delete an existing goal."""
    model = Goal
    template_name = 'challenges/goal_confirm_delete.html'  # Optional: Confirmation page template
    success_url = reverse_lazy('goal-list')  # Redirect to the goal list after deletion

    def get_queryset(self):
        """Ensure that only the owner of the goal can delete it."""
        return super().get_queryset().filter(user=self.request.user)

# List view of user challenges
@method_decorator(login_required(login_url='login'), name='dispatch')
class ChallengeListView(ListView):
    """Displays a list of challenges for the logged-in user."""
    model = Challenge
    template_name = 'challenges/challenge_list.html'
    context_object_name = 'challenges'

    def get_queryset(self):
        """Fetches the challenges associated with the current logged-in user."""
        return Challenge.objects.filter(user=self.request.user)

# Daily goal tracker view to track goals by date
@method_decorator(login_required(login_url='login'), name='dispatch')
class DailyGoalTrackerView(View):
    """Displays and handles updates to the daily goals for the selected date."""

    def get(self, request):
        """Displays the daily tracker for the selected date."""
        # Get the date parameter from the query string or use today's date by default
        date_str = request.GET.get('date', None)
        if date_str:
            try:
                selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                selected_date = timezone.localtime().date()  # Use local date if there's a parsing error
        else:
            selected_date = timezone.localtime().date()

        # Determine the day of the week (0 = Monday, 6 = Sunday) and fetch goals for that day
        day_of_week = selected_date.weekday()
        goals = Goal.objects.filter(user=request.user)

        # Filter goals based on the selected day of the week
        day_of_week_map = {0: 'monday', 1: 'tuesday', 2: 'wednesday', 3: 'thursday', 4: 'friday', 5: 'saturday', 6: 'sunday'}
        goals = goals.filter(**{day_of_week_map[day_of_week]: True})

        # Get the goal completions for the selected day and map them to their status
        goal_completions = GoalCompletion.objects.filter(goal__in=goals, date=selected_date)
        goal_status_map = {goal.id: False for goal in goals}
        for completion in goal_completions:
            goal_status_map[completion.goal.id] = completion.completed

        context = {
            'today': timezone.localtime().date(),  # Use local date for 'today'
            'selected_date': selected_date,
            'goals': goals,
            'goal_status_map': goal_status_map,
        }

        return render(request, 'challenges/daily_goal_tracker.html', context)

    def post(self, request):
        """Handles updating the goal completion status for the selected date."""
        # Get the selected date from the form submission or use today's date
        selected_date_str = request.POST.get('selected_date')
        if selected_date_str:
            try:
                selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
            except ValueError:
                selected_date = timezone.localtime().date()
        else:
            selected_date = timezone.localtime().date()

        # Iterate over all goals and update their completion status based on form inputs
        goals = Goal.objects.filter(user=request.user)
        for goal in goals:
            goal_completed = request.POST.get(f'goal_{goal.id}', 'off') == 'on'  # Checkbox is 'on' if checked
            GoalCompletion.objects.update_or_create(goal=goal, date=selected_date, defaults={'completed': goal_completed})

        # Redirect back to the daily tracker with the selected date
        return redirect(f'{reverse_lazy("daily-goal-tracker")}?date={selected_date}')

# Calendar view for viewing goals in a monthly calendar format
@method_decorator(login_required(login_url='login'), name='dispatch')
class CalendarView(View):
    """Displays the user's goals in a monthly calendar format."""

    def get(self, request, year=None, month=None):
        """Handles GET requests to display the calendar for the specified or current month."""
        # Use the current month and year if not provided
        if not year or not month:
            today = now().date()
            year = today.year
            month = today.month

        # Generate the calendar for the specified month and year, starting with Sunday
        cal = calendar.Calendar(firstweekday=6)
        month_days = list(cal.itermonthdays4(year, month))  # Generate (year, month, day, weekday) tuples

        # Fetch all goals for the current user
        goals = Goal.objects.filter(user=request.user)

        # Map each day of the month to the goals scheduled for that day
        day_goal_map = {day: [] for day in range(1, 32)}
        for goal in goals:
            days_of_week = {0: goal.monday, 1: goal.tuesday, 2: goal.wednesday, 3: goal.thursday, 4: goal.friday, 5: goal.saturday, 6: goal.sunday}
            for (y, m, d, wd) in month_days:
                if d != 0 and m == month and days_of_week.get(wd, False):
                    day_goal_map[d].append(goal)

        # Get all goal completions for the current user in the specified month
        goal_completions = GoalCompletion.objects.filter(goal__user=request.user, date__year=year, date__month=month)

        # Create a map of (goal, day) -> completion status for the month
        completion_map = {(completion.goal.id, completion.date.day): completion.completed for completion in goal_completions}

        # Build the structured list for template rendering
        month_data = []
        for (y, m, d, wd) in month_days:
            if d == 0 or m != month:
                # Padding day or day from a different month
                month_data.append({'day': None, 'goals': None})
            else:
                goals_for_day = [{'goal': goal, 'completed': completion_map.get((goal.id, d), False)} for goal in day_goal_map[d]]
                month_data.append({'day': d, 'goals': goals_for_day})

        # Calculate previous and next months for calendar navigation
        prev_month, next_month = month - 1, month + 1
        prev_year, next_year = year, year

        if prev_month == 0:  # If previous month is December of the previous year
            prev_month, prev_year = 12, year - 1

        if next_month == 13:  # If next month is January of the next year
            next_month, next_year = 1, year + 1

        # Pass all context variables to the template
        return render(request, 'challenges/calendar_view.html', {
            'year': year,
            'month': month,
            'month_data': month_data,
            'month_name': calendar.month_name[month],
            'prev_year': prev_year,
            'prev_month': prev_month,
            'next_year': next_year,
            'next_month': next_month,
            'today': now().date(),  # Add the current date for highlighting
        })
