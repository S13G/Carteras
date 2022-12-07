import uuid

from django.db import models

from users.models import Profile


# Create your models here.

class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    demo_link = models.CharField(max_length=1000, null=True, blank=True)
    source_link = models.CharField(max_length=1000, null=True, blank=True)
    vote_total = models.IntegerField(default=0)
    vote_ratio = models.IntegerField(default=0)
    tags = models.ManyToManyField('Tag', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-vote_ratio", "-vote_total", "title"]

    @property
    def reviewers(self):
        queryset = self.reviews.all().values_list("owner__id", flat=True)
        return queryset

    @property
    def get_vote_count(self):
        reviews = self.reviews.all()
        up_votes = reviews.filter(value="up").count()
        total_votes = reviews.count()

        ratio = (up_votes / total_votes) * 100
        self.vote_total = total_votes
        self.vote_ratio = ratio
        self.save()


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote')
    )

    owner = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name="reviews")
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=50, choices=VOTE_TYPE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name
