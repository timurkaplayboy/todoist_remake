from django import forms

from .models import Task, TaskComment


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                css_class = 'form-check-input'
            elif isinstance(field.widget, forms.Select):
                css_class = 'form-select'
            else:
                css_class = 'form-control'
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
    only_mine = forms.BooleanField(
        label='Only my tasks',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


class CommentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ['text', 'media']
        labels = {
            'text': 'Comment',
            'media': 'Media or file',
        }
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write an update, question, or decision...'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        media = cleaned_data.get('media')

        if not text and not media:
            raise forms.ValidationError('Add a comment text or attach a file.')

        return cleaned_data
