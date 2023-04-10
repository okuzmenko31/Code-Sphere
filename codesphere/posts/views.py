from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView
from django.views import View
from .models import Posts, PostLikes
from .forms import CreatePostForm
from tags.models import Tags
from .utils import AddViewByIP
from comments.forms import PostComment


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


class PostDetail(AddViewByIP, View):

    def get(self, *args, **kwargs):
        comment_form = PostComment()
        post = Posts.objects.get(id=kwargs['post_id'])
        context = {
            'post': post,
            'comment_form': comment_form
        }
        if PostLikes.objects.filter(user=self.request.user.profile, post=post).exists():
            user_like = PostLikes.objects.get(post=post, user=self.request.user.profile)
            context['user_like'] = user_like
        self.check_or_add_ip(self.request, post)
        return render(self.request, template_name='posts/post-detail.html', context=context)


class LikePost(View):

    def get(self, *args, **kwargs):
        post = get_object_or_404(Posts, id=kwargs['post_id'])

        if PostLikes.objects.filter(post=post,
                                    user=self.request.user.profile).exists():
            like = PostLikes.objects.get(post=post, user=self.request.user.profile)
            like.delete()
        else:
            PostLikes.objects.create(post=post, user=self.request.user.profile)
        return redirect(post.get_absolute_url())


class AddPostComment(CreateView):
    form_class = PostComment
    template_name = 'posts/post-detail.html'
    context_object_name = 'form'

    def form_valid(self, form):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Posts, id=post_id)

        # saving comment
        comment = form.save(commit=False)
        comment.user = self.request.user.profile
        comment.content_type = ContentType.objects.get_for_model(post)
        comment.object_id = post_id
        comment.save()
        return redirect(post.get_absolute_url())
