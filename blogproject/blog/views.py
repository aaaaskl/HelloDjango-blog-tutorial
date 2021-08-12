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
    print('hahaha category')
    cate = get_object_or_404(Category, pk=pk)
    print(cate)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    print(post_list)
    return render(request, 'blog/index.html', context={'post_list': post_list})


def tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=tag).order_by("-created_time")
    return render(request, 'blog/index.html', {'post_list': post_list})
