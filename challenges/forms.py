from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import WhitelistedEmail

# Form for managing WhitelistedEmail entries in the database
class WhitelistedEmailForm(forms.ModelForm):
    class Meta:
        model = WhitelistedEmail  # Link the form to the WhitelistedEmail model
        fields = ['email', 'active']  # Specify which fields of the model to include in the form

# Custom signup form that extends the base ModelForm to include validation against whitelisted emails
class CustomSignupForm(forms.ModelForm):
    class Meta:
        model = User  # Link the form to the built-in User model
        fields = ['username', 'email', 'password']  # Specify which fields to include for the signup form

    # Define the password field explicitly to use a password input widget for proper hiding of input
    password = forms.CharField(widget=forms.PasswordInput)
    # Define the email field explicitly to use Django's built-in EmailField for validation
    email = forms.EmailField()

    def clean_email(self):
        """
        Custom validator for the email field.
        Check if the provided email is in the WhitelistedEmail model and is active.
        """
        email = self.cleaned_data.get('email')
        if not WhitelistedEmail.objects.filter(email=email, active=True).exists():
            # Raise an error if the email is not in the active whitelist
            raise ValidationError("This email address is not allowed to register. Please contact the admin.")
        return email

    def save(self, commit=True):
        """
        Override the default save method to handle password hashing correctly.
        This ensures that the password is stored in a hashed format in the database.
        """
        user = super().save(commit=False)  # Create a user object without saving it to the database yet
        user.set_password(self.cleaned_data['password'])  # Hash the password before saving
        if commit:  # Save the user object to the database if commit is True
            user.save()
        return user
