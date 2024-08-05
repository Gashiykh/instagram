from django.urls import reverse
from django.views import generic

from webapp.models import Post, Image
from webapp.forms import PostForm, ImageForm


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
        return reverse('home')