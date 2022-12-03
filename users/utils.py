from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from users.models import Profile, Skill


# paginating profiles
def paginateProfiles(request, profiles, results):
    page = request.GET.get("page")
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    # indicating how many pagination buttons will show
    left_index = (int(page) - 4)
    right_index = (int(page) + 5)

    if left_index < 1:
        left_index = 1

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)
    return custom_range, profiles


# function for passing profiles and filtering by search query
def searchProfiles(request):
    search_query = ""
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__icontains=search_query)
    # used distinct() to make sure the profiles were not being duplicated because of the skills search
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) | Q(short_intro__icontains=search_query) | Q(skill__in=skills))
    return profiles, search_query
