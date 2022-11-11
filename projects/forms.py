from django import forms
from django.forms import ModelForm

from projects.models import Project


# Create your forms below


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = "__all__"
        exclude = ["vote_ratio", "vote_total", "owner"]
        widgets = {
            'tags': forms.CheckboxSelectMultiple(), # making the checkboxes better
        }

    # adding styles to the form by adding the css class to be modified
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})