from .models import Updates as UpdateModel

from django import forms

class UpdateModelForm(forms.ModelForm):
    
    class Meta:
        model = UpdateModel
        fields = ("user", "content", "image");
