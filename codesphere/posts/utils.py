from .models import ViewersIPs


class AddViewByIP:

    @staticmethod
    def get_client_ip(request):
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

