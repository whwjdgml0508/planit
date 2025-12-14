from django import template

register = template.Library()

@register.filter
def lookup(dictionary, key):
    """딕셔너리에서 키로 값을 조회하는 필터"""
    if dictionary is None:
        return None
    try:
        # 정수 키 처리
        if isinstance(key, str) and key.isdigit():
            key = int(key)
        return dictionary.get(key)
    except (AttributeError, TypeError, KeyError):
        return None

@register.filter
def get_item(dictionary, key):
    """딕셔너리에서 키로 값을 조회하는 필터 (lookup과 동일)"""
    if dictionary is None:
        return None
    try:
        # 정수 키 처리
        if isinstance(key, str) and key.isdigit():
            key = int(key)
        return dictionary.get(key)
    except (AttributeError, TypeError, KeyError):
        return None
