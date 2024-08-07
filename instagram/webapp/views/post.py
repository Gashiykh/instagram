from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import CreateView

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
            ).exists()
        context['post'] = post
        return context


class PostCreateView(generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_form'] = ImageForm(self.request.POST, self.request.FILES)
        else:
            context['image_form'] = ImageForm()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()

        context = self.get_context_data()
        image_form = context['image_form']
        if image_form.is_valid():
            images = self.request.FILES.getlist('images')
            for image in images:
                Image.objects.create(post=self.object, image=image)

        user = self.request.user
        user.post_count = user.posts.count()
        user.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('posts')


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['post_id']
        form.save()
        post_id = self.kwargs['post_id']
        comment_text = form.cleaned_data['text']
        if 'from_home' in self.request.GET:
            return redirect(f'/?user_comment_post={post_id}&comment_text={comment_text}')
        return redirect(reverse_lazy('post', kwargs={
            'post_id': post_id}) + f'?user_comment_post={post_id}&comment_text={comment_text}')

    def get_success_url(self):
        if self.request.GET.get('from_home'):
            return reverse_lazy('home')
        return reverse_lazy('post', kwargs={'pk': self.object.post.id})
