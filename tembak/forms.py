from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class XlSigninForm(forms.Form):
    msisdn = forms.CharField()
    otp = forms.CharField()

    msisdn.widget.attrs.update({'placeholder': '628xx'})
    otp.widget.attrs.update({'placeholder': 'OTP'})

    def clean_msisdn(self):
        data = self.cleaned_data['msisdn']

        if not data.startswith('628'):
            raise ValidationError(_('Invalid MSISDN'))

        return data

    def clean_otp(self):
        data = self.cleaned_data['otp']

        if len(data) != 6:
            raise ValidationError(_('OTP length must be 6'))

        return data.upper()

class XlSendPackageForm(forms.Form):
    package_id = forms.IntegerField()

    package_id.widget.attrs.update({'placeholder': 'Package Id'})

    def clean_package_id(self):
        data = self.cleaned_data['package_id']

        return data
