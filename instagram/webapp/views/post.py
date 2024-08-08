from django.db.models import F
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from webapp.models import Comment, Image, Like, Post
from webapp.forms import CommentForm, ImageForm, PostForm


class PostView(generic.DetailView):
    model = Post
    template_name = 'posts/post.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = post.comments.all().order_by('created_at')
        context['comments'] = comments

        post.liked = Like.objects.filter(
                post=post.id,
                author=self.request.user
            ).exists() if self.request.user.is_authenticated else False
        context['post'] = post
        return context


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/create.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['image_form'] = ImageForm(self.request.POST, self.request.FILES)
        else:
            data['image_form'] = ImageForm()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        image_form = context['image_form']
        if image_form.is_valid():
            self.object = form.save(commit=False)
            self.object.author = self.request.user
            self.object.save()
            for image in self.request.FILES.getlist('image'):
                Image.objects.create(post=self.object, image=image)
            user = self.request.user
            user.post_count = F('post_count') + 1
            user.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, image_form=image_form))
        
    def get_success_url(self):
        return reverse('profile', kwargs={'user_id': self.request.user.id})


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])

        form.instance.author = self.request.user
        form.instance.post_id = post.id
        form.save()

        post.comment_count = F('comment_count') + 1
        post.save()

        comment_text = form.cleaned_data['text']
        if 'from_home' in self.request.GET:
            return redirect(f'/?user_comment_post={post.id}&comment_text={comment_text}')

        return redirect(reverse_lazy('post', kwargs={
            'post_id': post.id}) + f'?user_comment_post={post.id}&comment_text={comment_text}')

    def get_success_url(self):
        if self.request.GET.get('from_home'):
            return reverse_lazy('home')
        return reverse_lazy('post', kwargs={'pk': self.object.post.id})


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    # ToDo: реализовать проверку на существование поста
    model = Post
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        author = post.author

        response = super().delete(request, *args, **kwargs)

        author.post_count = F('post_count') - 1
        author.save()

        return response

    def get_success_url(self):
        return reverse('home')