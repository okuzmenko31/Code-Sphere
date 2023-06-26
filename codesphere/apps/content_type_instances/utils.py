from enum import Enum
from typing import NamedTuple, Optional, Union

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q

from apps.posts.models import Posts

MODEL_INSTANCES_TYPES = (
    ('post', 'post'),
)


class InstancesTypes(str, Enum):
    """
    All available instances for which user
    can add comment.
    """
    post = 'post'


class ContentTypeData(NamedTuple):
    instance: Optional[Posts] = None
    error: Optional[str] = None


class ContentTypeInstancesMixin:
    _instance = None

    @staticmethod
    def _get_instance_model(instance_type: InstancesTypes):
        if instance_type == InstancesTypes.post:
            return Posts

    def get_instance_by_id(self, instance_type: InstancesTypes,
                           instance_id) -> ContentTypeData:
        instance_model = self._get_instance_model(instance_type)
        try:
            self._instance = instance_model.objects.get(id=instance_id)
        except ObjectDoesNotExist:
            return ContentTypeData(error='Instance doest not exist!')
        return ContentTypeData(instance=self._instance)

    @staticmethod
    def get_instance_by_model_and_type(model,
                                       instance_type: InstancesTypes,
                                       instance_id: int):
        return model.objects.filter(instance_type=instance_type,
                                    object_id=instance_id)

    @property
    def allowed_instances_types(self) -> list:
        instances_lst = []
        for instance in InstancesTypes:
            instances_lst.append(instance.value)
        return instances_lst

    def check_kwargs(self, **kwargs) -> Union[str, None]:
        if kwargs['instance_value'] not in self.allowed_instances_types:
            return ContentTypeData(error='Instance value does not exist!').error
        _, error = self.get_instance_by_id(instance_type=kwargs['instance_value'],
                                           instance_id=kwargs['instance_id'])
        if error is not None:
            return error
        return None


def count_content_type_instance_quantity(model,
                                         instance_type,
                                         instance_id):
    quantity = model.objects.aggregate(count=Count('id', filter=Q(instance_type=instance_type,
                                                                  object_id=instance_id)))
    return quantity['count']
