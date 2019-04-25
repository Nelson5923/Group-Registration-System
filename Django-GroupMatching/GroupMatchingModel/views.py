import json
import os
import datetime
import random

from django.shortcuts import render
from django.shortcuts import redirect
from GroupMatchingModel.form import ProfileForm
from GroupMatchingModel.form import LoginForm
from GroupMatchingModel.form import CreateProjectForm
from GroupMatchingModel.form import CreateGroupForm
from GroupMatchingModel.form import JoinGroupForm
from GroupMatchingModel.form import SelectGroupForm
from GroupMatchingModel.models import Profile
from GroupMatchingModel.models import Group
from GroupMatchingModel.models import Project
from GroupMatchingModel.models import Membership
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.mail import EmailMessage


# Create your views here.

def ShowMessage(request):

    return render(request, 'home.html', {'user': request.user})

@login_required(login_url='/login/')
def createProject(request):

    if request.method == 'POST':

        form = CreateProjectForm(request.POST)

        if form.is_valid():

            project_name = form.cleaned_data.get('project_name')
            min_member = form.cleaned_data.get('min_member')
            max_member = form.cleaned_data.get('max_member')
            deadline = form.cleaned_data.get('deadline')
            description = form.cleaned_data.get('description')

            model = Project.objects.create(project_name=project_name,
                                           min_member=min_member,
                                           max_member = max_member,
                                           deadline=deadline,
                                           description=description)
            model.save()
            messages.success(request, 'Your project has submitted.')

    else:

        form = CreateProjectForm()

    return render(request, 'form.html', {'form': form})

@login_required(login_url='/login/')
def createGroup(request):

    if request.method == 'POST':

        form = CreateGroupForm(request.POST)

        if form.is_valid():

            project = form.cleaned_data.get('project')
            group_name = form.cleaned_data.get('group_name')
            description = form.cleaned_data.get('description')
            model = Group.objects.create(project=project,
                                         group_name=group_name,
                                         description=description)
            model.save()

            messages.success(request, 'Your group application has submitted.')

    else:

        form = CreateGroupForm()

    return render(request, 'form.html', {'form': form})

@login_required(login_url='/login/')
def loadGroup(request):

    project_name = request.GET.get('project_name')
    project = Project.objects.get(project_name=project_name)
    form = JoinGroupForm(selected=project)

    return render(request, 'load_gp.html', {'form': form})

@login_required(login_url='/login/')
def joinGroup(request):

    if request.method == 'POST':

        form = JoinGroupForm(request.POST, selected=request.POST['project'])

        if form.is_valid():

            project = form.cleaned_data.get('project')
            group = form.cleaned_data.get('group')
            error_flag = 0

            if Membership.objects.filter(user=request.user, group=group).exists():

                messages.error(request, 'You have already joined the group.')
                error_flag = 1

            if Membership.objects.filter(group=group).count() >= int(group.project.max_member):

                messages.error(request, 'The group is already full.')
                error_flag = 1

            if error_flag is not 1:

                Membership.objects.create(user=request.user, group=group)
                messages.success(request, 'Your application has submitted.')

        else:

            messages.error(request, 'Fail.')

    else:

        form = JoinGroupForm(selected=None)

    return render(request, 'form.html', {'form': form})

@login_required(login_url='/login/')
def quitGroup(request):

    if request.method == 'POST':

        form = SelectGroupForm(request.POST, user=request.user)
        form.fields['group'].label = "Choose your group to quit: "

        if form.is_valid():

            group = form.cleaned_data.get('group')
            Membership.objects.filter(user=request.user, group=group).delete()
            messages.success(request, 'Success to quit a group')

        else:

            messages.error(request, 'Fail.')

    else:

        form = SelectGroupForm(user=request.user)
        form.fields['group'].label = "Choose your group to quit: "

    return render(request, 'form.html', {'form': form})

@login_required(login_url='/login/')
def ShowGroup(request):

    if request.method == 'POST':

        form = SelectGroupForm(request.POST, user=request.user)
        form.fields['group'].label = "Choose your group to show: "

        if form.is_valid():

            group = form.cleaned_data.get('group')
            members = Membership.objects.filter(group=group)

            return render(request, 'status.html', {'form': form, 'group': group, 'members': members})

        else:

            messages.error(request, 'Fail.')

    else:

        form = SelectGroupForm(user=request.user)
        form.fields['group'].label = "Choose your group to show: "

    return render(request, 'status.html', {'form': form})

def SignUp(request):

    if request.method == 'POST':

        form = ProfileForm(request.POST)

        if form.is_valid():

                user = form.save()
                user.refresh_from_db()  # load the profile instance created by the signal
                user.save()

                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = auth.authenticate(username=username, password=password)
                auth.login(request, user)
                messages.success(request, 'SignUp Success.')
                return render(request, 'home.html', {'user': user})

        else:

            messages.error(request, 'SignUp Fail.')

    else:

        form = ProfileForm()

    return render(request, 'signup.html', {'form': form})

def Login(request):

    if request.method == 'POST':

        form = LoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(username=username, password=password)

            if not user:

                messages.error(request, 'Username or Password not Correct')

            else:

                auth.login(request, user)
                messages.success(request, 'Success to Login !')
                return render(request, 'home.html', {'user': user})

        else:

            messages.error(request, 'Unknown Error')

    else:

        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def Logout(request):

    if request.user.is_authenticated:

        auth.logout(request)
        messages.success(request, 'You are Logging out !')
        return render(request, 'home.html')

    return redirect('/home/')

@login_required(login_url='/login/')
def DeliverEmail(request):

    due_project = Project.objects.filter(deadline=datetime.date.today())

    for p in due_project:

        groups = Group.objects.filter(project=p)

        for g in groups:

            m = Membership.objects.filter(group=g)

            if m.count() >= int(p.min_member):

                member_string = '\n'.join([u.user.username + ': ' + u.user.email for u in m])
                message_body = 'Your Group Member is:' + '\n' + member_string
                email = EmailMessage('Your Group ' + g.group_name +
                                    ' in ' + p.project_name + ' is formed!',  message_body, to=[u.user.email for u in m])
                email.send()

    messages.success(request, 'You deliver the email!')
    return render(request, 'home.html')

@login_required(login_url='/login/')
def ClearProject(request):

    due_project = Project.objects.filter(deadline=datetime.date.today())

    for p in due_project:

        groups = Group.objects.filter(project=p)
        random_user = []

        for g in groups:

            users = Membership.objects.filter(group=g)

            if users.count() < int(p.min_member):

                for u in users:

                    random_user.append(u.user)

                g.delete()

        i = 0

        while random_user:

            if i % int(p.max_member) is 0:

                new_group = Group.objects.create(project=p,
                                             group_name=str(random.getrandbits(30)),
                                             description='Random Group')
                new_group.save()

            new_member = Membership.objects.create(user=random_user[0], group=new_group)

            new_member.save()

            del random_user[0]

            i = i + 1

    messages.success(request, 'You clean the project!')
    return render(request, 'home.html')








