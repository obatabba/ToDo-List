from django import forms
from .models import Task


class TaskAddFrom(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'due_date']

    title = forms.CharField(
        max_length=80,
        required=True,
        label='',
        widget=forms.widgets.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'What you want to do...'
            }
        )
    )

    description = forms.CharField(
        max_length=80,
        required=False,
        label='',
        widget=forms.widgets.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Explain some details...'
            }
        )
    )

    priority = forms.ChoiceField(
        choices=Task.PRIORITY_CHOICES.items(),  # Use the choices defined in the model
        widget=forms.Select(
            attrs={'class': 'form-select'}
        )
    )

    due_date = forms.DateTimeField(
        required=False,
        widget=forms.widgets.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }
        )
    )
