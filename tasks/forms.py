from django import forms
from .models import Task


class TaskFilterForm(forms.Form):
    status = forms.ChoiceField(
        choices=[('', 'All')] + list(Task.Status.choices),
        required=False
    )
    priority = forms.ChoiceField(
        choices=[('', 'All')] + list(Task.Priority.choices),
        required=False
    )