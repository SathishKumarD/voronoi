from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.bootstrap import (PrependedText, PrependedAppendedText, FormActions)
from crispy_forms.layout import Submit, HTML
from crispy_forms.bootstrap import FormActions

from .models import House

class HouseForm(forms.ModelForm):
	class Meta:
		model = House
		fields = ('house_number','street','city','zipcode','state')

	def __init__(self, *args, **kwargs):
		super(HouseForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.layout.append(
		FormActions(HTML("""<a role="button" class="btn btn-default" 
			href="/">Cancel</a>"""),
		Submit('save', 'Submit'),))
    
