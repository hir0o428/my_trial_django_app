from django import forms
from django.contrib.auth.forms import AuthenticationForm
from datetime import date

from .models import Demand


class LoginForm(AuthenticationForm):
    """Login Form"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class DemandCreateForm(forms.ModelForm):
    """Demand Create"""

    class Meta:
        model = Demand
        fields = (
            'product', 'technology',
            'content',
            'start_date', 'end_date',
            'frequency', 'comment'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'

    '''
    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        if start_date < date.today():
            raise forms.ValidationError("The date cannot be set in the past!")
        return start_date
    '''

    def clean(self):
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        today = date.today()
        if start_date < today:
            raise forms.ValidationError("The start date cannot be set in the past!({0} < Today: {1})"
                                        .format(start_date, today))
        elif start_date > end_date:
            raise forms.ValidationError("The end date is later than the start date(End: {0} < Start: {1})"
                                        .format(end_date, start_date))


class DemandUpdateForm(forms.ModelForm):
    """Demand Update"""

    class Meta:
        model = Demand
        fields = (
            'product', 'technology',
            'content',
            'start_date', 'end_date',
            'frequency', 'comment'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].widget.input_type = 'date'
        self.fields['end_date'].widget.input_type = 'date'

    def clean(self):
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        if start_date > end_date:
            raise forms.ValidationError("The end date is later than the start date")
