from rest_framework import serializers
from .models import Comments
from django.utils.timesince import timesince


class CommentsSerializer(serializers.ModelSerializer):
    user_username = serializers.SerializerMethodField(read_only=True, required=False)
    created_timesince = serializers.SerializerMethodField(read_only=True, required=False)
    comment_instance_str = serializers.SerializerMethodField(read_only=True, required=False)
    comment_instance_id = serializers.SerializerMethodField(read_only=True, required=False)

    class Meta:
        model = Comments
        fields = ['id',
                  'user_username',
                  'created_timesince',
                  'text',
                  'comment_instance_str',
                  'comment_instance_id']

    @classmethod
    def get_user_username(cls, instance):
        return instance.user.username

    @classmethod
    def get_created_timesince(cls, instance):
        return timesince(instance.created) + ' ago'

    @classmethod
    def get_comment_instance_str(cls, instance):
        return instance.content_object.__str__()

    @classmethod
    def get_comment_instance_id(cls, instance):
        return instance.content_object.id
