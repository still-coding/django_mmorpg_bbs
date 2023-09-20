from django import forms
from django.forms import ModelForm, ClearableFileInput
from .models import Ad, Response

class ResponseForm(ModelForm):
    class Meta:
        model = Response
        fields = ('text', 'ad', 'user')
        labels = {
            'text': 'Response Text',
        }
        widgets = {
            'text': forms.TextInput(),
            'ad': forms.HiddenInput(),
            'user': forms.HiddenInput(),
        }



class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class AdForm(ModelForm):
    class Meta:
        model = Ad
        fields = ('category', 'title', 'text', 'price', 'user')
        widgets = {
            'user': forms.HiddenInput(),
        }



class AdImageForm(forms.Form):
    image = MultipleFileField(required=False)
