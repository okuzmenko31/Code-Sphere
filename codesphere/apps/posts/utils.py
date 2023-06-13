from apps.followings.models import Following
from .models import ViewersIPs


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


class ViewsMixin:
    """
    Mixin for views logic of posts.
    Creates or gets view by user's ip address.
    Expected that this mixin will be used only
    with classes which are inherited from RetrieveModelMixin.
    """

    @staticmethod
    def get_client_ip(request) -> str:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')  # В REMOTE_ADDR user's IP
        return ip

    def check_or_add_ip(self, request, post):
        ip = self.get_client_ip(request)
        if ViewersIPs.objects.filter(ip=ip).exists():
            post.views.add(ViewersIPs.objects.get(ip=ip))
        else:
            new_ip = ViewersIPs.objects.create(ip=ip)
            post.views.add(new_ip)

    def retrieve(self, request, *args, **kwargs):
        self.check_or_add_ip(request=request, post=self.get_object())
        return super().retrieve(request, *args, **kwargs)
