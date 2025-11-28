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
        value_float = float(str(value)) if value is not None else 0
        arg_float = float(str(arg)) if arg is not None else 0
        return value_float * arg_float
    except (ValueError, TypeError, AttributeError):
        return 0

@register.filter
def div(value, arg):
    """나눗셈 필터"""
    try:
        value_float = float(str(value)) if value is not None else 0
        arg_float = float(str(arg)) if arg is not None else 0
        
        if arg_float == 0:
            return 0
        return value_float / arg_float
    except (ValueError, TypeError, AttributeError):
        return 0

@register.filter
def percentage(value, total):
    """퍼센트 계산 필터"""
    try:
        # Decimal이나 다른 타입을 float로 변환
        value_float = float(str(value)) if value is not None else 0
        total_float = float(str(total)) if total is not None else 0
        
        if total_float == 0:
            return 0
        return round((value_float / total_float) * 100, 1)
    except (ValueError, TypeError, AttributeError):
        return 0
