from django import template
from django.contrib.contenttypes.models import ContentType
from .. import models
import urllib

register = template.Library()


@register.filter
def remove_spaces(value):
    return value.replace(' ', '+')


@register.simple_tag(takes_context = True)
def url_replace(context, field, value):
	dict_ = context['context']['request'].GET.copy()
	dict_[field] = value
	return dict_.urlencode()

@register.assignment_tag
def get_rent_options():
	default = [{'text':'Anything','value':''}]
	options = [{'text':'< '+str(x),'value':x} for x in [300,400,500,600,700,800,1000,1200,1500]]
	return default + options


@register.filter
def divide(value, arg):
	if not value:
		return None
	try:
		return  round(1.0*value /arg,1) 
	except (ValueError, ZeroDivisionError):
		return None

