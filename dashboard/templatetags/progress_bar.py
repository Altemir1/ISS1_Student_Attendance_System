from django import template


register = template.Library()

@register.filter
def calculate_progress(value):
    absent_hours = value['absent_hours']
    total_hours = value['total_hours']
    return int(round((absent_hours / total_hours) * 100))