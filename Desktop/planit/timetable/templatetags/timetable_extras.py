from django import template

register = template.Library()

@register.filter
def lookup(dictionary, key):
    """딕셔너리에서 키로 값을 조회하는 필터"""
    if dictionary and key in dictionary:
        return dictionary[key]
    return None

@register.filter
def get_item(dictionary, key):
    """딕셔너리에서 키로 값을 조회하는 필터 (lookup과 동일)"""
    return dictionary.get(key) if dictionary else None
