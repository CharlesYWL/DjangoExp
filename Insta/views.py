from annoying.decorators import ajax_request
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from Insta.models import Post
from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import InstaUser, Post, Like, UserConnection, Comment

# Create your views here.


class HelloWorld(TemplateView):
    template_name = 'test.html'


class PostsView(ListView):
    model = Post
    template_name = 'index.html'

    def get_queryset(self):
        following = set()
        if self.request.user.is_anonymous:
            return following
        current_user = self.request.user
        following.add(current_user)
        for conn in UserConnection.objects.filter(creator=current_user).select_related('following'):
            following.add(conn.following)
        return Post.objects.filter(author__in=following)


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        liked = Like.objects.filter(post=self.kwargs.get(
            'pk'), user=self.request.user).first()
        if liked:
            data['liked'] = 1
        else:
            data['liked'] = 0
        return data


class UserDetailView(DetailView):
    model = InstaUser
    template_name = 'user_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_create.html'
    # fields = ['title', 'image']
    fields = '__all__'
    login_url = 'login'


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_edit.html'
    fields = '__all__'


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts')


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')


class ExploreView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'explore.html'
    login_url = 'login'

    def get_queryset(self):
        return Post.objects.all().order_by('-posted_on')[:20]


class EditProfile(LoginRequiredMixin, UpdateView):
    model = InstaUser
    template_name = 'user_edit.html'
    fields = ['profile_pic', 'username']
    login_url = 'login'


@ajax_request
def addLike(request):
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    try:
        like = Like(post=post, user=request.user)
        like.save()
        result = 1
    except Exception as e:
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        result = 0

    return {
        'result': result,
        'post_pk': post_pk
    }


@ajax_request
def toggleFollow(request):
    current_user = InstaUser.objects.get(pk=request.user.pk)
    follow_user_pk = request.POST.get('follow_user_pk')
    follow_user = InstaUser.objects.get(pk=follow_user_pk)

    try:
        if current_user != follow_user:
            if request.POST.get('type') == 'follow':
                connection = UserConnection(
                    creator=current_user, following=follow_user)
                connection.save()
            elif request.POST.get('type') == 'unfollow':
                UserConnection.objects.filter(
                    creator=current_user, following=follow_user).delete()
            result = 1
        else:
            result = 0
    except Exception as e:
        print(e)
        result = 0
    return {
        'result': result,
        'type': request.POST.get('type'),
        'follow_user_pk': follow_user_pk
    }


@ajax_request
def makeComment(request):
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    comment_text = request.POST.get('comment_text')
    user = InstaUser.objects.get(pk=request.user.pk)
    commenter_info = {}
    try:
        comment = Comment(post=post, user=user, comment=comment_text)
        comment.save()
        result = 1
        commenter_info = {
            'username': user.username,
            'comment_text': comment_text
        }
    except Exception as e:
        result = 0
    return{
        'result': result,
        'post_pk': post_pk,
        'commenter_info': commenter_info
    }
