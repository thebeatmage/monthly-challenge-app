from django.contrib.auth.models import User
from django.db import models

# Represents a user's goal with a name, description, and schedule for the days of the week
class Goal(models.Model):
    name = models.CharField(max_length=100)  # The name of the goal, with a maximum length of 100 characters
    description = models.TextField(blank=True)  # An optional description field for additional goal details
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link each goal to a user; delete the goal if the user is deleted
    monday = models.BooleanField(default=False)  # Flag to indicate if the goal is set for Monday
    tuesday = models.BooleanField(default=False)  # Flag to indicate if the goal is set for Tuesday
    wednesday = models.BooleanField(default=False)  # Flag to indicate if the goal is set for Wednesday
    thursday = models.BooleanField(default=False)  # Flag to indicate if the goal is set for Thursday
    friday = models.BooleanField(default=False)  # Flag to indicate if the goal is set for Friday
    saturday = models.BooleanField(default=False)  # Flag to indicate if the goal is set for Saturday
    sunday = models.BooleanField(default=False)  # Flag to indicate if the goal is set for Sunday

    def __str__(self):
        # Return the name of the goal when the object is printed
        return self.name

# Represents a record of a goal's completion status for a specific date
class GoalCompletion(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)  # Link each completion record to a goal; delete the record if the goal is deleted
    date = models.DateField()  # The date when the goal was completed or not
    completed = models.BooleanField(default=False)  # Status of whether the goal was completed or not for the given date

    class Meta:
        unique_together = ('goal', 'date')  # Ensure that a goal can only have one completion status per date

    def __str__(self):
        # Return a descriptive string for the completion record
        return f"{self.goal.name} on {self.date} - {'Completed' if self.completed else 'Not Completed'}"

# Represents a challenge for a user, which can include multiple goals and span a date range
class Challenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link each challenge to a user; delete the challenge if the user is deleted
    start_date = models.DateField()  # The starting date of the challenge
    end_date = models.DateField()  # The ending date of the challenge
    goals = models.ManyToManyField(Goal)  # A many-to-many relationship to associate multiple goals with a challenge

    def __str__(self):
        # Return a descriptive string for the challenge
        return f"Challenge for {self.user.username} ({self.start_date} to {self.end_date})"

# Represents a whitelisted email address for restricting signups
class WhitelistedEmail(models.Model):
    email = models.EmailField(unique=True)  # Store the whitelisted email address, ensuring it is unique in the database
    active = models.BooleanField(default=True)  # Toggle to indicate if the email is currently active for use

    def __str__(self):
        # Return the email address when the object is printed
        return self.email
