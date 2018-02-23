"""Forms for the review app."""
from django import forms
from django.conf import settings
from django.utils.translation import get_language

from django_libs.loaders import load_member

from .models import Review, Rating, RatingCategory


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.bootstrap import (PrependedText, PrependedAppendedText, FormActions)


class ReviewForm(forms.ModelForm):


    def __init__(self, reviewed_item,  user=None, *args, **kwargs):
        self.user = user
        self.reviewed_item = reviewed_item
        self.widget = load_member(
            getattr(settings, 'REVIEW_FORM_CHOICE_WIDGET',
                    'django.forms.widgets.Select')
        )()

        super(ReviewForm, self).__init__(*args, **kwargs)

        if 'data' in kwargs and 'tags' in kwargs['data']:
            data= dict(kwargs['data'].iterlists())
            tags = data[u'tags'];
            self.fields['tags'] = forms.CharField(label=tags);
            # Dynamically add fields for each rating category
        for category in RatingCategory.objects.all():
            field_name = 'category_{0}'.format(category.pk)
            choices = category.get_choices()
            self.fields[field_name] = forms.ChoiceField(
                choices=choices, label=category.name,
                help_text=category.question,
                widget=self.widget,
            )
            self.fields[field_name].required = category.required
            if self.instance.pk:
                try:
                    self.initial.update({
                        'category_{0}'.format(category.pk): Rating.objects.get(
                            review=self.instance, category=category).value,
                    })
                except Rating.DoesNotExist:
                    pass

        self.helper = FormHelper(self)
        # You can dynamically adjust your layout
        self.helper.layout.append(Submit('save', 'save'))

    def save(self, *args, **kwargs):
        if not self.instance.pk:
            self.instance.user = self.user
            self.instance.reviewed_item = self.reviewed_item
            self.instance.language = get_language()
        self.instance = super(ReviewForm, self).save(*args, **kwargs)
        tags = self.cleaned_data['tags'].split(",") if 'tags' in self.cleaned_data else []
        # Update or create ratings
        #self.fields.pop('tags')
        for field in self.fields:
            if field.startswith('category_'):
                rating, created = Rating.objects.get_or_create(
                    review=self.instance,
                    category=RatingCategory.objects.get(
                        pk=field.replace('category_', '')),
                )
                rating.value = self.cleaned_data[field]
                rating.save()

        self.instance.average_rating = self.instance.get_average_rating()
        self.instance.save()
        for tag in tags:
            self.instance.tags.add(tag);
        return self.instance

    class Meta:
        model = Review
        fields = ('content','recommended','lived_from','lived_to','laundry_onsite','beds','baths','rent' )
