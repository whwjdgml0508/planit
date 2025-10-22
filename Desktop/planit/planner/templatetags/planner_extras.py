from django import template
from datetime import datetime, timedelta

register = template.Library()

@register.filter
def add_days(value, days):
    """날짜에 일수를 더하는 필터"""
    if isinstance(value, str):
        try:
            date_obj = datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            return value
    else:
        date_obj = value
    
    return date_obj + timedelta(days=days)
