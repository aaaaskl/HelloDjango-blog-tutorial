from django.db import models
from django.utils import timezone
from django.urls import reverse
import markdown
from django.utils.html import strip_tags

from django.contrib.auth.models import User
from markdown import extensions
# Register your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name    

class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField('标题',max_length=70)
    body = models.TextField('正文')
    created_time = models.DateTimeField('创建时间',default=timezone.now)
    modified_time = models.DateTimeField('修改时间')

    # PositiveIntegerField : 正整数或0
    # editable=False ： 不允许后台认为修改
    views = models.PositiveIntegerField(default=0,editable=False)
    excerpt = models.CharField('摘要',max_length=200, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE,verbose_name="分类")
    tags = models.ManyToManyField(Tag, blank=True,verbose_name="标签")
    author = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="作者")

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
    
    def save(self,*args,**kwargs):
        self.modified_time = timezone.now()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite'
        ])
        # 摘要 存入数据库的时候 将摘要 按正文截取54个字符保存
        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})

    def increase_views(self):
        self.views+=1
        # update_fields 参数来告诉 Django 只更新数据库中 views 字段的值
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title