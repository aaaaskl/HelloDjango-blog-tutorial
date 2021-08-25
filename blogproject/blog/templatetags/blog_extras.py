from django import template
from ..models import Post,Category,Tag
from django.db.models.aggregates import Count
from django.db.models.functions import ExtractYear,ExtractMonth

register = template.Library()


"""
inclusion_tag 装饰器的参数 takes_context 设置为 True 时将告诉 django，
在渲染 _recent_posts.html 模板时，不仅传入show_recent_posts 返回的模板变量，
同时会传入父模板（即使用 {% show_recent_posts %} 模板标签的模板）上下文
（可以简单理解为渲染父模板的视图函数传入父模板的模板变量以及 django 自己传入的模板变量）
"""
@register.inclusion_tag('blog/inclusions/_recent_posts.html',takes_context=True)
def show_recent_posts(context,num=5):
    return {
        'recent_post_list':Post.objects.all().order_by('-created_time')[:num]
    }

@register.inclusion_tag('blog/inclusions/_archives.html',takes_context=True)
def show_archives(context):
    date_list = Post.objects.annotate(year=ExtractYear('created_time'), month=ExtractMonth('created_time')).values('year','month').order_by('-year','-month').annotate(num_posts=Count('id'))
    return {
        # 'date_list':Post.objects.dates('created_time','month',order='DESC')
        'date_list':date_list
    }


@register.inclusion_tag('blog/inclusions/_categories.html',takes_context=True)
def show_categories(context):
    category_list = Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'category_list':category_list
    }


"""
{% load blog_extras %} {% show_categories %}{% show_tags %}
1.  base.html 先 load templatestags下的py文件{% load blog_extras %}，并调用其中的{% func %}
2. inclusion_tag 返回 待渲染的变量和一小段html代码 插入到之前load的html文件中 
"""

@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    tag_list = Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'tag_list': tag_list,
    }    