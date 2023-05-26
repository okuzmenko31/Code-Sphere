from typing import NamedTuple, Union, Optional
from django.core.exceptions import ObjectDoesNotExist
from abc import ABC, abstractmethod
from django.core.handlers.wsgi import WSGIRequest
from .models import Following, FollowingCategory, ContentType, User


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

    def follow(self, following_category, following_object):
        request = self.get_request()
        following, created = Following.objects.get_or_create(user=request.user,
                                                             content_type=following_category.content_type,
                                                             object_id=following_object.id)
        if not created:
            following.delete()
            return FollowingData(msg='You successfully unfollowed!')
        return FollowingData(msg='Successfully followed!')
