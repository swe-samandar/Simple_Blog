from django.shortcuts import render,  redirect, get_object_or_404
from django.views import View
from .models import Category, Post, Comment
from datetime import datetime
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import PostCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def get_today():
    return datetime.date(datetime.today())

def get_categories():
    return Category.objects.all()

def get_related_post():
    posts = Post.objects.all()
    return posts

def get_latest_post():
    return Post.objects.all().first()


# Create your views here.

class PostsListView(View):
    def get(self, request):
        posts_list = Post.objects.all()
        paginator = Paginator(posts_list, 4)
        page_number = request.GET.get('page', 1)  
        posts = paginator.get_page(page_number)

        context = {
            'categories': get_categories(),
            'today': get_today(),
            'posts': posts
        }
        return render(request, 'blog/index.html', context)
    

class CreatePostView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'blog:post_create'

    def get(self, request):
        return self.render_form(PostCreateForm())

    def post(self, request):
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:index')
        return self.render_form(form)

    def render_form(self, form):
        return render(self.request, 'blog/post_create.html', {'form': form})


class UpdatePostView(UserPassesTestMixin, LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'blog:post_update'

    def get_object(self, pk):
        return get_object_or_404(Post, id=pk)

    def get(self, request, pk):
        post = self.get_object(pk)
        form = PostCreateForm(instance=post)
        return render(request, 'blog/post_update.html', {'form': form})

    def post(self, request, pk):
        post = self.get_object(pk)
        form = PostCreateForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()
            return redirect('blog:detail', pk=pk)

        return render(request, 'blog/post_update.html', {'form': form})

    def test_func(self):
        post = self.get_object(self.kwargs['pk'])
        return post.author == self.request.user


class DeletePostView(UserPassesTestMixin, LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'blog:post_delete'

    def get_object(self, pk):
        return get_object_or_404(Post, id=pk)

    def test_func(self):
        post = self.get_object(self.kwargs['pk'])
        return post.author == self.request.user

    def get(self, request, pk):
        post = self.get_object(pk)
        return render(request, 'blog/post_delete.html', {'post': post})

    def post(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return redirect('blog:index')
    

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        message = request.POST.get('message', '').strip()
        post_id = request.POST.get('post_id')

        if not message:
            return JsonResponse({'error': "Izoh bo'sh bo'lmasligi kerak!"}, status=400)

        post = get_object_or_404(Post, id=post_id)

        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=message
        )

        return JsonResponse({
            'message': 'Comment added successfully!',
            'comment': {
                'author': f'{comment.author.first_name} {comment.author.last_name}',
                'content': comment.content,
                'created_at': comment.created_at.strftime('%Y-%m-%d')
            }
        })


class CategoryPostView(View):
    def get(self, request, pk):
        ctg = get_object_or_404(Category, id=pk)
        posts = Post.objects.filter(categories=ctg)
        return render(request, 'blog/category_post.html', {'posts': posts})


class LikePostView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)

        if request.user in post.likes.all():
            post.likes.remove(request.user) 
            liked = False
        else:
            post.likes.add(request.user)
            liked = True

        return JsonResponse({
            "status": "liked" if liked else "unliked",
            "like_count": post.likes.count()
        })

class AboutView(View):
    def get(self, request):
        return render(request, 'blog/about.html')


class ContactViev(View):
    def get(self, request):
        return render(request, 'blog/contact.html')
    

class DetailView(View):
    def get(self, request, pk):
        print(get_latest_post())
        post_ = Post.objects.get(pk=pk)
        context = {
            'post_': post_,
            'latest_post': get_latest_post(),
            'related_posts': get_related_post(),
            'categories': get_categories(),
            'today': get_today()
        }
        return render(request, 'blog/detail.html', context)
    
    def post(self, request, pk):
        query = request.GET.get('query')
        posts = Post.objects.filter(title_icontains=query) if query else Post.objects.all()
        post_ = Post.objects.get(pk=pk)
        context = {
            'post_': post_,
            'posts': posts,
            'latest_post': get_latest_post(),
            'today': get_today(),
            'related_posts': get_related_post(),
            'categories': get_categories(),
        }

        content = request.GET.get('message')
        if content:
            comment = Comment.objects.create(content=content)
            comment.save()
            

        return render(request, 'blog/detail.html', context)


class SearchView(View):
    def get(self, request):
        query = request.GET.get('query', '')
        results = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        return render(request, 'search.html', {'query': query, 'results': results})
