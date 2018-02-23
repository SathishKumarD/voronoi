from django.views.generic.edit import CreateView

from .models import House
from .forms import HouseForm


class CreateHouseView(CreateView):
	"""A create view for Foo model"""
	template_name = "house_form.html"
	model = House
	form_class = HouseForm
