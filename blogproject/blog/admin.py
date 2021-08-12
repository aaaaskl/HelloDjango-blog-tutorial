from django.contrib import admin
from django.db import models
from .models import Post,Category,Tag
from django.utils import timezone

class PostAdmin(admin.ModelAdmin):
    list_display=['title', 'created_time', 'modified_time', 'category', 'author'] #列表页显示
    fields = ['title', 'body','created_time', 'excerpt', 'category', 'tags'] # 表单 显示的字段(指定要用户填写的字段内容)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        return super().save_model(request, obj, form, change) 

admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)