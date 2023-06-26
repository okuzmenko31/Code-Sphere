from rest_framework import serializers
from .models import Likes


class LikesSerializer(serializers.ModelSerializer):
    like_creator_username = serializers.SerializerMethodField(read_only=True,
                                                              required=False)
    like_instance_str = serializers.SerializerMethodField(read_only=True,
                                                          required=False)
    like_instance_id = serializers.SerializerMethodField(read_only=True,
                                                         required=False)

    class Meta:
        model = Likes
        fields = ('id', 'like_creator_username',
                  'instance_type', 'like_instance_str',
                  'like_instance_id')
        read_only_fields = ['instance_type']

    @classmethod
    def get_like_creator_username(cls, instance):
        return instance.creator.username

    @classmethod
    def get_like_instance_str(cls, instance):
        return instance.content_object.__str__()

    @classmethod
    def get_like_instance_id(cls, instance):
        return instance.content_object.id
