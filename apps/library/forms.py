from django.forms import ModelForm
from .models import Library

class LibraryForm(ModelForm):
    class Meta:
        model = Library
        fields = ["user"]