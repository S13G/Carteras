from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

from projects.forms import ProjectForm
from projects.models import Project, Tag


# Create your views here


def projects(request):
    search_query = ""
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query)

    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) | Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) | Q(tags__in=tags))
    context = {"projects": projects, "search_query": search_query}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    context = {"project": projectObj}
    return render(request, 'projects/single-project.html', context)


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
