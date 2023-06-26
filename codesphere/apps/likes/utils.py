from .models import Likes
from ..content_type_instances.utils import count_content_type_instance_quantity


def check_exist_like(instance_type,
                     user,
                     instance_id) -> bool:
    exist = Likes.objects.filter(instance_type=instance_type,
                                 creator=user,
                                 object_id=instance_id).exists()
    if exist:
        Likes.objects.get(instance_type=instance_type,
                          creator=user,
                          object_id=instance_id).delete()
        return True
    return False


def count_likes(instance_type,
                instance_id):
    return count_content_type_instance_quantity(model=Likes,
                                                instance_type=instance_type,
                                                instance_id=instance_id)
