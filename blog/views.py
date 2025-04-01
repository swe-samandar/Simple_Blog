from django.shortcuts import render
from django.views import View
from .models import Category,Post, Comment
from datetime import datetime
from django.db.models import Q

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
        posts = Post.objects.all()
        context = {
            'latest_post': get_latest_post(),
            'today': get_today(),
            'posts': posts
        }
        return render(request, 'blog/index.html', context)

    def post(self, request):
        query = request.GET.get('query')
        posts = Post.objects.filter(title_icontains=query) if query else Post.objects.all()
        context = {
            'latest_post': get_latest_post(),
            'today': get_today(),
            'posts': posts
        }
        return render(request, 'blog/index.html', context)
    

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
        results = Post.objects.filter(
    Q(title__icontains=query) |  
    Q(content__icontains=query)  
)
        
        return render(request, 'search.html', {'query': query, 'results': results})
