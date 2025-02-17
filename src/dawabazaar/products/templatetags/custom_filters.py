from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    """Subtracts arg from value."""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return 0  # Handle errors gracefully

@register.filter
def percentage(value, total):
    """Calculates the percentage: (value / total) * 100"""
    try:
        return round((int(value) / int(total)) * 100, 2)  # Rounded to 2 decimal places
    except (ZeroDivisionError, ValueError, TypeError):
        return 0  # Handle division by zero or invalid input
