
from django.core.exceptions import ValidationError
from django import forms


class UploadFileForm(forms.Form):
    select_file = forms.FileField()

    def clean_select_file(self):
        data = self.cleaned_data.get("select_file")
        if not data.name.endswith('.csv'):
            raise ValidationError("Error! Please select a csv file!")
        return data

        
CITY_CHOISES = [('LONDON', 'LONDON'),('PARIS', 'PARIS'),('PORTO', 'PORTO'),]

class ComPerCityForm(forms.Form):
    city= forms.CharField(label='Select city', widget=forms.Select(choices=CITY_CHOISES))
