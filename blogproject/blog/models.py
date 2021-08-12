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
    # 文章标题
    title = models.CharField('标题',max_length=70)

    # 文章正文，我们使用了 TextField
    body = models.TextField('正文')

    # 这两个列分别表示文章的创建时间和最后一次修改时间，存储时间的字段用 DateTimeField 类型。
    created_time = models.DateTimeField('创建时间',default=timezone.now)
    modified_time = models.DateTimeField('修改时间')

    # PositiveIntegerField : 正整数或0
    # editable=False ： 不允许后台认为修改
    viwes = models.PositiveIntegerField(default=0,editable=False)

    # 指定 CharField 的 blank=True 参数值后就可以允许空值了。
    excerpt = models.CharField('摘要',max_length=200, blank=True)

    # 这是分类与标签，分类与标签的模型我们已经定义在上面。
    # 我们在这里把文章对应的数据库表和分类、标签对应的数据库表关联了起来，但是关联形式稍微有点不同。
    # 我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以我们使用的是 ForeignKey，即一
    # 对多的关联关系。且自 django 2.0 以后，ForeignKey 必须传入一个 on_delete 参数用来指定当关联的
    # 数据被删除时，被关联的数据的行为，我们这里假定当某个分类被删除时，该分类下全部文章也同时被删除，因此     # 使用 models.CASCADE 参数，意为级联删除。
    # 而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用 
    # ManyToManyField，表明这是多对多的关联关系。
    # 同时我们规定文章可以没有标签，因此为标签 tags 指定了 blank=True。
    # https://docs.djangoproject.com/en/2.2/topics/db/models/#relationships
    category = models.ForeignKey(Category, on_delete=models.CASCADE,verbose_name="分类")
    tags = models.ManyToManyField(Tag, blank=True,verbose_name="标签")

    # django.contrib.auth 是 django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 
    # Category 类似。
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

        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})


    def increase_views(self):
        self.views+=1
        # update_fields 参数来告诉 Django 只更新数据库中 views 字段的值，以提高效率
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title