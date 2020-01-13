from django import forms
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage

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

    def send_email(self):
        product = self.cleaned_data['product']
        product_id = self.cleaned_data['product_id']
        tech_node = self.cleaned_data['tech_node']
        content = self.cleaned_data['content']
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        frequency = self.cleaned_data['frequency']
        comment = self.cleaned_data['comment']

        subject = 'Demand Creation {0} for {1}'.format(content, product)
        message = 'From: Administrator of Demand Manager\n' + \
                  '<Registered Items>\n' + \
                  ' ' * 2 + 'Product: {}\n'.format(product) + \
                  ' ' * 2 + 'Product ID: {}\n'.format(product_id) + \
                  ' ' * 2 + 'Technology Node: {}\n'.format(tech_node) + \
                  ' ' * 2 + 'Verification Content: {}\n'.format(content) + \
                  ' ' * 2 + 'Date of Start: {}\n'.format(start_date) + \
                  ' ' * 2 + 'Date of End: {}\n'.format(end_date) + \
                  ' ' * 2 + 'Frequency[%]: {}\n'.format(frequency) + \
                  ' ' * 2 + 'Comment: {}\n'.format(comment)
        from_email = 'admin@example.com'
        to_list = ['test@example.com']
        bcc_list = ['admin@example.com']

        email = EmailMessage(subject=subject, body=message, from_email=from_email, to=to_list, bcc=bcc_list)
        email.send()


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
        help_text="Set License File.",
    )

    def upload(self):
        upload_file = self.cleaned_data['license_file']
        license_type = self.cleaned_data['license_type']
        file_name = default_storage.save("demand_manager/license/" + upload_file.name, upload_file)
        return license_type, default_storage.url(file_name)

