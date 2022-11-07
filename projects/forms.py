from django.forms import ModelForm

from projects.models import Project


# Create your forms below


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = "__all__"
        exclude = ["vote_ratio", "vote_total"]
