from rest_framework import serializers
from .models import Tags
from apps.followings.utils import count_followers


class TagsSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Tags
        fields = ['id', 'name', 'image', 'followers_count', 'slug']

    def get_followers_count(self, instance):
        return count_followers(instance)
