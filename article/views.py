from django.shortcuts import render, redirect, get_object_or_404
# 引入HttpResponse
from django.http import HttpResponse
# 引入刚才定义的ArticlePostForm表单类
from .forms import ArticlePostForm
# 引入User模型
from django.contrib.auth.models import User
# 导入数据模型ArticlePost
from .models import ArticlePost
from django.contrib.auth.decorators import login_required
# 引入分页模块
from django.core.paginator import Paginator
# 引入 Q 对象
from django.db.models import Q, Count
from comment.models import Comment
from .models import ArticleColumn
# 引入评论表单
from comment.forms import CommentForm


def article_list(request):
    article_list = ArticlePost.objects.all()
    article_column = ArticleColumn.objects.annotate(article_count=Count('article'))


    paginator = Paginator(article_list, 6)
    page_num = request.GET.get('page', 1)  # 获取url的页码参数（GET请求）
    articles = paginator.get_page(page_num)
    currentr_page_num = articles.number  # 获取当前页码
    # 获取当前页面前后各2页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)



    context = {}
    context['blogs'] = articles.object_list
    context['articles'] = articles
    context['page_range'] = page_range
    context['article_column'] = article_column

    return render(request, 'article/list.html', context)

# 文章详情
def article_detail(request, id):
    # 取出相应的文章
    article = get_object_or_404(ArticlePost,id=id)
    # 取出文章评论
    comments = Comment.objects.filter(article=id)


    # 需要传递给模板的对象
    if not request.COOKIES.get('blog_%s_readed' % id):
        article.total_views += 1
        article.save(update_fields=['total_views'])

    comment_form = CommentForm()
    context = { 'article': article ,'comments': comments ,'comment_form': comment_form,}
    # 载入模板，并返回context对象
    response =  render(request, 'article/detail.html', context)
    response.set_cookie('blog_%s_readed' % id, 'true')
    return response

# 写文章的视图
# 检查登录
@login_required(login_url='/userprofile/login/')
def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":

        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(request.POST, request.FILES)

        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            # 新增的代码
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            # 指定数据库中 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            new_article.author = User.objects.get(id=request.user.id)

            # 将新文章保存到数据库中
            new_article.save()
            article_post_form.save_m2m()
            # 完成后返回到文章列表
            return redirect("article:article_list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文
        # 新增及修改的代码
        columns = ArticleColumn.objects.all()
        context = {'article_post_form': article_post_form, 'columns': columns}
        # 返回模板
        return render(request, 'article/create.html', context)


# 安全删除文章
@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        if request.user != article.author:
            return HttpResponse("对不起，你无权修改这篇文章。")
        else:
            article.delete()
            return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")

# 更新文章
# 提醒用户登录
# 更新文章
@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新titile、body字段
    GET方法进入初始表单页面
    id： 文章的 id
    """

    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)

    # 过滤非作者的用户
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")

    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']

            if request.POST['column'] != 'none':
                # 保存文章栏目
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None

            if request.FILES.get('avatar'):
                article.avatar = request.FILES.get('avatar')

            article.tags.set(*request.POST.get('tags').split(','), clear=True)
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("article:article_detail", id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()

        # 文章栏目
        columns = ArticleColumn.objects.all()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = {
            'article': article,
            'article_post_form': article_post_form,
            'columns': columns,
            'tags': ','.join([x for x in article.tags.names()]),
        }

        # 将响应返回到模板中
        return render(request, 'article/update.html', context)

def blogs_with_type(request, id):
    blog_type = get_object_or_404(ArticleColumn, id=id)
    article_list= ArticlePost.objects.filter(column=blog_type)

    paginator = Paginator(article_list, 6)
    page_num = request.GET.get('page', 1)  # 获取url的页码参数（GET请求）
    articles = paginator.get_page(page_num)
    currentr_page_num = articles.number  # 获取当前页码
    # 获取当前页面前后各2页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    context = {}
    context['blogs'] = articles.object_list
    context['articles'] = articles
    context['page_range'] = page_range
    context['article_column'] = ArticleColumn.objects.annotate(article_count=Count('article'))
    context['blog_type'] = blog_type


    return render(request,'article/article_type.html', context)