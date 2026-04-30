from django import forms
from .models import Task


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            css_class = 'form-select' if isinstance(field.widget, forms.Select) else 'form-control'
            field.widget.attrs['class'] = css_class


class TaskForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class TaskFilterForm(BootstrapFormMixin, forms.Form):
    status = forms.ChoiceField(
        choices=[('', 'All statuses')] + list(Task.Status.choices),
        required=False
    )
    priority = forms.ChoiceField(
        choices=[('', 'All priorities')] + list(Task.Priority.choices),
        required=False
    )
