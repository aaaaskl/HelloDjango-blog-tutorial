from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from django.views.decorators.http import require_POST
from django.contrib import messages

from .forms import CommentForm
from blog.models import Post

@require_POST
def comment(request,post_pk):
    # 先获取被评论的文章，方便之后将其和评论关联起来
    post = get_object_or_404(Post,pk=post_pk)

    print('^'*50)
    print(request.POST)
    form = CommentForm(request.POST)
    print(form)

    if form.is_valid():
        # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。？
        comment = form.save(commit=False)

        # 将评论和文章关联起来
        comment.post = post
        comment.save()

        messages.add_message(request,messages.SUCCESS,'评论发表成功',extra_tags='success')

        print('----post:',post)
        return redirect(post)
    context = {
        'post':post,
        'form':form,
    }
    messages.add_message(request,messages.ERROR,'评论发表失败',extra_tags='danger')
    return render(request, 'comments/preview.html', context=context)