from django.template import Library

register = Library()

@register.inclusion_tag('home/result.html')
def show_result(queryset):
    return {'objects': queryset}