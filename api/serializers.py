from rest_framework import serializers

from projects.models import Project, Tag, Review
from users.models import Profile


# Create serializers


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    reviews = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)

    class Meta:
        model = Project
        fields = "__all__"

    def get_reviews(self, obj):
        reviews = obj.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data
