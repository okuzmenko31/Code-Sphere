from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views import View

from .models import Tags, TagSubscribers


class AllTagsListView(ListView):
    """All tags view"""
    model = Tags
    template_name = 'tags/all-tags.html'
    context_object_name = 'tags'

    def get_queryset(self):
        return Tags.objects.all()


class SubscribeTag(View):
    """Subscribing tags view"""

    def get(self, *args, **kwargs):
        tag = get_object_or_404(Tags, id=self.kwargs['tag_id'])
        tag_subs = TagSubscribers.objects.filter(tag=tag)

        if self.request.user.is_authenticated:
            try:
                # if user is subscribed to tag, he will unsubscribe
                subscriber = tag_subs.get(user=self.request.user)
                if subscriber in tag_subs:
                    subscriber.delete()
            except (Exception,):
                # if user isn't subscribed, he will subscribe
                TagSubscribers.objects.create(user=self.request.user,
                                              tag=tag)
        return redirect('all-tags')
