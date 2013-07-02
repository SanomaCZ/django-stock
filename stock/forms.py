from django import forms
from django.utils.translation import ugettext_lazy as _

from stock.models import Operation


class OperationForm(forms.ModelForm):
    model = Operation

    def clean(self):
        data = self.cleaned_data

        if data.get('operation_type') == 'r':
            if data['item'].pieces - data['pieces'] < 0:
                raise forms.ValidationError(_("Given operation results in negative pieces on stock"))

        if self.instance:
            for forbidden_prop in ('pieces', 'operation_type'):
                if data[forbidden_prop] != self.instance.__dict__[forbidden_prop]:
                    raise forms.ValidationError(_("Cannot change existing operation"))
            if self.instance.__dict__.get('attachment'):
                raise forms.ValidationError(_("Cannot change existing operation"))

        return data
