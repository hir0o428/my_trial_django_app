from django import forms
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

from .models import Demand, Release


class DemandCreateForm(forms.ModelForm):
    """Demand Create"""

    class Meta:
        model = Demand
        fields = (
            'product', 'product_id',
            'tech_node',
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
            'product', 'product_id',
            'tech_node',
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


class DemandAnalysisForm(forms.Form):
    period_start = forms.DateField(
        label="Date of Start",
        initial=date.today(),
        widget=forms.DateInput(attrs={"type":"date"}),
    )
    period_end = forms.DateField(
        label="Date of End",
        initial=date.today() + relativedelta(months=1) - timedelta(days=1),
        widget=forms.DateInput(attrs={"type":"date"}),
    )
    reference_hours = forms.IntegerField(
        label = "Reference hours per day",
        initial = 8,
    )


class ImportReleasedLicenseForm(forms.Form):
    license_type = forms.ChoiceField(
        label="License Type",
        choices=Release.lic_type_choice,
    )
    license_file = forms.FileField(
        label="License File",
        help_text="Set License File."
    )
