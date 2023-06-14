from rest_framework import serializers
from .models import Posts
from .utils import UnconfirmedPostsSerializerMixin
from django.urls import reverse
from apps.comments.utils import CommentsInstancesTypes


class PostsSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField(read_only=True)
    post_comment_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Posts
        fields = ['id', 'creator', 'title', 'short_description',
                  'cover_photo', 'tags', 'post_views', 'text', 'post_comment_url']
        read_only_fields = ['creator']

    def get_creator(self, instance):
        return instance.creator.username

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        tags_list = []
        for tag in instance.tags.all():
            tags_list.append(tag.name)
        ret['tags'] = tags_list
        return ret

    def get_post_comment_url(self, instance):
        return reverse('add_comment', kwargs={'instance_value': CommentsInstancesTypes.post.value,
                                              'instance_id': instance.id})


class UnconfirmedPostsSerializer(UnconfirmedPostsSerializerMixin, PostsSerializer):
    staff_edit = True
    staff_fields = ['is_confirmed']
