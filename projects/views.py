from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from projects.forms import ProjectForm
from projects.models import Project
from projects.utils import searchProjects, paginateProjects


# Create your views here


# passing all projects
def projects(request):
    projects, search_query = searchProjects(request)

    # pagination
    custom_range, projects = paginateProjects(request, projects, 6)

    context = {"projects": projects, "search_query": search_query, "custom_range": custom_range}
    return render(request, 'projects/projects.html', context)


# single project details
def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    context = {"project": projectObj}
    return render(request, 'projects/single-project.html', context)


# create projects
@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')
    context = {"form": form}
    return render(request, 'projects/project-form.html', context)


# update project
@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    try:
        project = profile.project_set.get(id=pk)
    except Project.DoesNotExist:
        messages.error(request, "This project doesn't belong to you")
        return redirect('account')
    form = ProjectForm(instance=project)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        form.save()
        return redirect('projects')
    context = {"form": form}
    return render(request, 'projects/project-form.html', context)


# delete project
@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    try:
        project = profile.project_set.get(id=pk)
    except Project.DoesNotExist:
        messages.error(request, "This project doesn't belong to you")
        return redirect('account')

    if request.method == "POST":
        project.delete()
        return redirect('account')
    return render(request, 'delete-template.html', {"object": project})
