from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from .models import Posts
from .forms import CreatePostForm
from tags.models import Tags


class AllPostsListView(ListView):
    model = Posts
    template_name = 'posts/all-posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Posts.objects.filter(is_confirmed=True)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class CreatePostView(View):

    def get(self, *args, **kwargs):
        form = CreatePostForm()
        if is_ajax(self.request):
            try:
                term = self.request.GET.get('term')
                tags = Tags.objects.all().filter(name__icontains=term)
                response_content = list(tags.values())
                return JsonResponse(response_content, safe=False)
            except (Exception,):
                return render(self.request, 'posts/create-post.html', {'form': form})
        return render(self.request, 'posts/create-post.html', {'form': form})

    def post(self, *args, **kwargs):
        form = CreatePostForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.creator = self.request.user.profile
            post.save()
            post.tags.set(form.cleaned_data['tags'])
        return self.get(*args, **kwargs)


class PostDetail(View):

    def get(self, *args, **kwargs):
        post = Posts.objects.get(id=kwargs['post_id'])
        return render(self.request, 'posts/post-detail.html', {'post': post})
