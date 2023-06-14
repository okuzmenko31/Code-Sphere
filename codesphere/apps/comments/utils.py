from enum import Enum
from django.core.exceptions import ObjectDoesNotExist
from typing import NamedTuple, Optional, Union
from apps.posts.models import Posts
from .models import Comments


class CommentsInstances(str, Enum):
    """
    All available instances for which user
    can add comment.
    """
    post = 'post'


class CommentData(NamedTuple):
    instance: Optional[Posts] = None
    error: Optional[str] = None


class CommentInstancesMixin:
    _instance = None

    @staticmethod
    def _get_instance_model(instance_type: CommentsInstances):
        if instance_type == CommentsInstances.post:
            return Posts

    def get_instance_by_id(self, instance_type: CommentsInstances,
                           instance_id) -> CommentData:
        instance_model = self._get_instance_model(instance_type)
        try:
            self._instance = instance_model.objects.get(id=instance_id)
        except ObjectDoesNotExist:
            return CommentData(error='Instance doest not exist!')
        return CommentData(instance=self._instance)

    @property
    def allowed_instances_types(self) -> list:
        instances_lst = []
        for instance in CommentsInstances:
            instances_lst.append(instance.value)
        return instances_lst

    def check_kwargs(self, **kwargs) -> Union[str, None]:
        if kwargs['instance_value'] not in self.allowed_instances_types:
            return CommentData(error='Instance value does not exist!').error
        _, error = self.get_instance_by_id(instance_type=kwargs['instance_value'],
                                           instance_id=kwargs['instance_id'])
        if error is not None:
            return error
        return None


class CommentsMixin(CommentInstancesMixin):

    @staticmethod
    def get_comments(instance_id: int) -> Comments:
        return Comments.objects.filter(object_id=instance_id)

    def add_comment(self, instance_type: CommentsInstances, instance_id, data):
        instance = self.get_instance_by_id(instance_type=instance_type,
                                           instance_id=instance_id)
        if instance is not None:
            comment = Comments(content_object=instance, **data)
            comment.save()
