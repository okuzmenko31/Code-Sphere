from notifications.signals import notify
from .models import Posts
from django.urls import reverse
from apps.followings.models import Following
from apps.notifications.utils import NotificationsMixin


class UnconfirmedPostsSerializerMixin:
    """
    Mixin which allows staff users to edit
    some fields of unconfirmed posts.
    """
    staff_edit = False
    staff_fields = []  # fields which staff can edit

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.staff_edit is True:
            read_only_fields = []
            for field in self.Meta.fields:
                if field not in self.staff_fields:
                    read_only_fields.append(field)
            self.Meta.read_only_fields = read_only_fields

            self.Meta.fields.extend(self.staff_fields)


class PostMixin:

    @staticmethod
    def get_post_notification_message(post: Posts):
        post_url = reverse('post_detail', kwargs={'post_id': post.id})
        message = f'{post.creator.username} made a new post , check it by this link: \n{post_url}'
        return message

    @staticmethod
    def get_post_creator_followers(post: Posts) -> list[Following]:
        followers_list = []
        post_creator_followers = Following.objects.filter(object_id=post.creator.id)
        for follower in post_creator_followers:
            followers_list.append(follower.user)
        return followers_list
