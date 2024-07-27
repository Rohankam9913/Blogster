from .models import BlogModel
from django import forms

class CreateForm(forms.ModelForm):
    class Meta:
        model = BlogModel
        fields = ["title", "content", "topics"]
    