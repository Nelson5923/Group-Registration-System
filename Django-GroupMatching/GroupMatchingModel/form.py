from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from GroupMatchingModel.models import Project
from GroupMatchingModel.models import Group
from django.forms import ModelChoiceField

# Modify Select Form Value

class ProjectModelChoiceField(ModelChoiceField):

    def label_from_instance(self, obj):
        return obj.project_name

class GroupModelChoiceField(ModelChoiceField):

    def label_from_instance(self, obj):
        return obj.group_name

# User Creation

class ProfileForm(UserCreationForm):

    # sid = forms.CharField(max_length=10)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email',)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already in use.")
        else:
            return username

class LoginForm(forms.Form):
    username = forms.CharField(label="Username",max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class CreateProjectForm(forms.Form):
    project_name = forms.CharField(label="Project Name: ", max_length=200, required=True)
    min_member = forms.CharField(label="Minimum Number of Member: ", max_length=2, required=True)
    max_member = forms.CharField(label="Maximum Number of Member: ", max_length=2, required=True)
    deadline = forms.DateField(label="Deadline: ", widget=forms.DateTimeInput(attrs={'type': 'date'}), required=True)
    description = forms.CharField(label="Project Description: ", widget=forms.Textarea(attrs={'rows':4,
                                            'cols':90,
                                            'style':'resize:none;'}))

    def clean_project_name(self):
        project_name = self.cleaned_data.get('project_name')
        if Project.objects.filter(project_name=project_name).exists():
            raise forms.ValidationError("This project name is already in use.")
        else:
            return project_name

class CreateGroupForm(forms.Form):

    # CustomizedModel return a Object & Create a Select Form

    project = ProjectModelChoiceField(label="Project Name: ",widget=forms.Select, queryset=Project.objects.all())
    group_name = forms.CharField(label="Group Name: ", max_length=40)
    description = forms.CharField(label="Group Description: ", widget=forms.Textarea(attrs={'rows':4,
                                            'cols':90,
                                            'style':'resize:none;'}))

    def clean_group_name(self):
        group_name = self.cleaned_data.get('group_name')
        project = self.cleaned_data.get('project')
        if Group.objects.filter(group_name=group_name,project=project).exists():
            raise forms.ValidationError("This group name is already in use.")
        else:
            return group_name

class JoinGroupForm(forms.Form):

    project = ProjectModelChoiceField(label="Choose your project: ", widget=forms.Select, queryset=Project.objects.all())
    group = GroupModelChoiceField(label="Choose your group to join: ", widget=forms.Select, queryset=Group.objects.none())

    def __init__(self, *args, **kwargs):
        selected = kwargs.pop('selected', None)
        super(JoinGroupForm, self).__init__(*args, **kwargs)
        if selected is not None:
            self.fields['project'] = ProjectModelChoiceField(label="Choose your project: ", widget=forms.Select, queryset=Project.objects.all())
            self.fields['group'] = GroupModelChoiceField(label="Choose your group to join: ", widget=forms.Select,
                queryset=Group.objects.filter(project=selected))

class SelectGroupForm(forms.Form):

    group = GroupModelChoiceField(label="Select your group: ", widget=forms.Select,
                                  queryset=Group.objects.none())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SelectGroupForm, self).__init__(*args, **kwargs)

        if user is not None:
            self.fields['group'] = GroupModelChoiceField(label="Select your group: ", widget=forms.Select,
                queryset=user.group_set.all())