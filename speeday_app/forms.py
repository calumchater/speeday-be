from django import forms

from .models import Product

class TaskForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'task_name',
            'start_time',
            'end_time',
        ]