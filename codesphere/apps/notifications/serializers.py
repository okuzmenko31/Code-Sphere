from django.utils.timesince import timesince
from rest_framework import serializers


class NotificationSerializer(serializers.Serializer):
    sender_username = serializers.SerializerMethodField(read_only=True)
    unread = serializers.BooleanField(read_only=True, required=False)
    message = serializers.SerializerMethodField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    date = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_sender_username(instance):
        return instance.actor.username

    @staticmethod
    def get_message(instance):
        return instance.verb

    @staticmethod
    def get_description(instance):
        return instance.description

    @staticmethod
    def get_date(instance):
        return timesince(instance.timestamp) + ' ago'
