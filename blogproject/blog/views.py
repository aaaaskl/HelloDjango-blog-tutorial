from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404,redirect
import markdown
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.contrib import messages
from django.db.models import Q

from pure_pagination.mixins import PaginationMixin
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

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

    m = re.search('<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''

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
class IndexView(PaginationMixin,ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    # 每页10条
    paginate_by = 10

    

    # def get_context_data(self, **kwargs):
    #     """
    #         {
    #             'paginator': <pure_pagination.paginator.Paginator object at 0x7fb0008b6160>, 
    #             'page_obj': <Page 1 of 21>, 
    #             'is_paginated': True, 
    #             'object_list': <QuerySet [<Post: Markdown 与代码高亮测试>, <Post: Sport majority modern specific four alone>, <Post: 由于一种出现谢谢信息学校>, <Post: 之间主题开发活动服务>, <Post: Program similar eight realize series opportunity name>, <Post: 用户无法那些项目国家>, <Post: 然后为了进入目前>, <Post: Coach plant figure responsibility finally particular>, <Post: Article science reduce heavy hard safe>, <Post: State line wife why wrong>]>, 
    #             'post_list': <QuerySet [<Post: Markdown 与代码高亮测试>, <Post: Sport majority modern specific four alone>, <Post: 由于一种出现谢谢信息学校>, <Post: 之间主题开发活动服务>, <Post: Program similar eight realize series opportunity name>, <Post: 用户无法那些项目国家>, <Post: 然后为了进入目前>, <Post: Coach plant figure responsibility finally particular>, <Post: Article science reduce heavy hard safe>, <Post: State line wife why wrong>]>, 
    #             'view': <blog.views.IndexView object at 0x7fb0008be610>
    #             }
    #     """
        
    #     context = super().get_context_data(**kwargs)
    #     return context

# 按年月归档
class ArchiveView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super().get_queryset().filter(created_time__year=year, created_time__month=month)

# 标签
class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(tags=tag)

# 分类
class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(category=cate)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):

        response = super().get(request, *args, **kwargs)

        self.object.increase_views()
        return response

    # def get_object(self, queryset=None):
    #     post = super().get_object(queryset=None)
    #     md = markdown.Markdown(extensions=[
    #         'markdown.extensions.extra',
    #         'markdown.extensions.codehilite',
    #         # 记得在顶部引入 TocExtension 和 slugify
    #         TocExtension(slugify=slugify),
    #     ])
    #     post.body = md.convert(post.body)

    #     m = re.search(
    #         r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    #     post.toc = m.group(1) if m is not None else ''

    #     return post


class SearchListView(PaginationMixin,ListView):
    paginate_by = 10
    template_name='blog/index.html'


    # ListView 如果要 定制查询结果重写get_queryset
    def get_queryset(self):
        q =self.request.GET.get('q')

        if not q:
            error_msg = "请输入搜索关键词"
            messages.add_message(self.request, messages.ERROR, error_msg, extra_tags='danger')
            return redirect('blog:index')
        post_list = Post.objects.filter( Q(title__icontains=q) | Q(body__icontains=q) )
        return post_list