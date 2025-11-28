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

@register.filter
def mul(value, arg):
    """곱셈 필터"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def div(value, arg):
    """나눗셈 필터"""
    try:
        if float(arg) == 0:
            return 0
        return float(value) / float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def percentage(value, total):
    """퍼센트 계산 필터"""
    try:
        if float(total) == 0:
            return 0
        return round((float(value) / float(total)) * 100, 1)
    except (ValueError, TypeError):
        return 0
