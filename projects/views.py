from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from projects.forms import ProjectForm, ReviewForm
from projects.models import Project, Tag
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
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        projectObj.get_vote_count

        messages.success(request, "Your review was successfully submitted")
        return redirect('project', pk=projectObj.id)

        # update project vote count
    context = {"project": projectObj, "form": form}
    return render(request, 'projects/single-project.html', context)


# create projects
@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == "POST":
        new_tags = request.POST.get("newtags").replace(",", " ").split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in new_tags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
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
        # adding new tags to the project form using a textarea
        new_tags = request.POST.get("newtags").replace(",", " ").split()
        form = ProjectForm(request.POST, request.FILES, instance=project)
        project = form.save()
        for tag in new_tags:
            tag, created = Tag.objects.get_or_create(name=tag)
            project.tags.add(tag)
        return redirect('projects')
    context = {"form": form, "project": project}
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
