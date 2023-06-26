from rest_framework import serializers
from .models import Posts
from .utils import UnconfirmedPostsSerializerMixin
from django.urls import reverse
from apps.content_type_instances.utils import InstancesTypes
from apps.comments.utils import count_comments
from apps.likes.utils import count_likes
from apps.tags.serializers import TagsSerializer


class PostsSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField(read_only=True)
    post_comment_url = serializers.SerializerMethodField(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True,
                                                       required=False)
    likes_count = serializers.SerializerMethodField(read_only=True,
                                                    required=False)
    tags = TagsSerializer(many=True, read_only=True)

    class Meta:
        model = Posts
        fields = ['id', 'creator', 'title', 'short_description',
                  'cover_photo', 'tags', 'post_views', 'text',
                  'post_comment_url', 'comments_count', 'likes_count']
        read_only_fields = ['creator']

    def get_creator(self, instance):
        return instance.creator.username

    @classmethod
    def get_post_comment_url(cls, instance):
        return reverse('comments_list_create', kwargs={'instance_value': InstancesTypes.post.value,
                                                       'instance_id': instance.id})

    @classmethod
    def get_comments_count(cls, instance):
        return count_comments(instance_type='post', instance_id=instance.id)

    @classmethod
    def get_likes_count(cls, instance):
        return count_likes(instance_type='post', instance_id=instance.id)


class UnconfirmedPostsSerializer(UnconfirmedPostsSerializerMixin, PostsSerializer):
    staff_edit = True
    staff_fields = ['is_confirmed']
