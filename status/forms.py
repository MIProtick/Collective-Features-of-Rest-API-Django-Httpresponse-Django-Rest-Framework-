from django import forms
from .models import Status

class StatusForm(forms.ModelForm):
    
    class Meta:
        model = Status
        fields = ("id", "user", "content", "image",)

    def clean(self, *args, **kwargs):
        data = self.cleaned_data
        content = data.get('content', None)
        if content == '':
            content = None
        image = data.get('image', None)
        if content == None and image == None :
            raise(forms.ValidationError('Content or image is required.'))
            
        return super().clean(*args, **kwargs)
    
