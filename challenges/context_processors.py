# challenges/context_processors.py

from django.utils.timezone import now

# Context processor to add the current date, year, and month to all templates
def current_date(request):
    """
    Adds today's date (`today`), current year (`year`), and current month (`month`) to the context.
    
    This function can be used in Django templates to dynamically display 
    the current date information without having to pass it manually through every view.
    
    Returns:
        A dictionary with the keys:
        - 'today': The current date.
        - 'year': The current year extracted from the date.
        - 'month': The current month extracted from the date.
    """
    today = now().date()  # Get today's date using Django's timezone-aware `now()` function
    return {
        'today': today,
        'year': today.year,  # Extract and include the current year
        'month': today.month,  # Extract and include the current month
    }
