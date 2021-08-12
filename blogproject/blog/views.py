from django.views.generic import ListView,DetailView
from django.shortcuts import render, get_object_or_404
import markdown
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

# Create your views here.
from django.http import HttpResponse
from .models import Category, Post, Tag
import re


def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html', context={
        'post_list': post_list
    })


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 阅读量 +1
    post.increase_views()

    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 'markdown.extensions.toc',
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)
    post.toc = md.toc
    print(post.toc)
    # <div class="toc">
    # <ul></ul>
    # </div>

    m = re.search('<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    print('m is', m)
    post.toc = m.group(1) if m is not None else ''

    print(post.toc)
    print(post.created_time)
    return render(request, 'blog/detail.html', context={'post': post})

def archive(request, year, month):
    post_list = Post.objects.filter(
        created_time__year=year, created_time__month=month).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=tag).order_by("-created_time")
    return render(request, 'blog/index.html', {'post_list': post_list})





# 获取文章列表 ， ListView 就是从数据库中获取某个模型列表数据的
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

# 按年月归档
class ArchiveView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super().get_queryset().filter(created_time__year=year,created_time__month=month)

# 标签
class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag,pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(tags=tag)

# 分类
class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(category=cate)

class PostDetailView(DetailView):
    model=Post
    template_name='blog/detail.html'
    context_object_name='post'

    def get(self,request,*args,**kwargs):

        response = super().get(request,*args,**kwargs)

        self.object.increase_views()
        return response

    def get_object(self,queryset=None):
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 记得在顶部引入 TocExtension 和 slugify
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)

        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''

        return post