from .models import Comments
from apps.content_type_instances.utils import count_content_type_instance_quantity


def count_comments(instance_type,
                   instance_id):
    return count_content_type_instance_quantity(model=Comments,
                                                instance_type=instance_type,
                                                instance_id=instance_id)
