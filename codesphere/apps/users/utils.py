from typing import NamedTuple, Union, Optional
from django.core.exceptions import ObjectDoesNotExist
from abc import ABC, abstractmethod
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Count, Q
from .models import Following, FollowingCategory, ContentType, User, UserProfile


class FollowingData(NamedTuple):
    instance: Union[FollowingCategory, ContentType.model_class] = None
    msg: Optional[str] = None


class FollowingMixin(ABC):

    @abstractmethod
    def get_request(self) -> WSGIRequest:
        raise NotImplementedError

    @classmethod
    def get_following_category(cls, category_id):
        try:
            following_category = FollowingCategory.objects.get(id=category_id)
        except FollowingCategory.DoesNotExist:
            return FollowingData(msg='Following category does not exist!')
        return FollowingData(instance=following_category)

    @classmethod
    def check_user(cls, following_model: ContentType.model_class,
                   user: User,
                   following_object) -> bool:
        if following_model is User and user.id == following_object.id:
            return False
        return True

    def get_following_object(self, category: FollowingCategory, following_id):
        following_category = category
        following_model = following_category.content_type.model_class()
        request = self.get_request()
        try:
            following_object = following_model.objects.get(id=following_id)
        except ObjectDoesNotExist:
            return FollowingData(msg='Following object does not exist!')
        if not self.check_user(following_model, following_object, request.user):
            return FollowingData(msg='You cannot subscribe to yourself')
        return FollowingData(instance=following_object)

    def follow(self, following_object) -> FollowingData:
        request = self.get_request()
        if Following.objects.filter(user=request.user, object_id=following_object.id):
            Following.objects.get(user=request.user, object_id=following_object.id).delete()
            return FollowingData(msg='You successfully unfollowed!')
        following = Following(content_object=following_object, user=request.user)
        following.save()
        return FollowingData(msg='Successfully followed!')


def count_followers(instance):
    followings_count = Following.objects.aggregate(count=Count('id', filter=Q(object_id=instance.id)))
    return followings_count['count']


def create_user_profile(user: User):
    if user.is_active and not UserProfile.objects.filter(user_id=user.id).exists():
        UserProfile.objects.create(user=user)
