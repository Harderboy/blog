from django.shortcuts import render, reverse, redirect
from django.views import View
from home.models import ArticleCategory, Article, Comment
from django.http import HttpResponseNotFound
from django.core.paginator import Paginator, EmptyPage


# Create your views here.


class IndexView(View):
    """首页展示"""

    def get(self, request):
        """
        1、获取分类信息
        2、获取用户点击的分类id
        3、根据分类id进行分类的查询
        4、获取分页参数
        5、根据分类信息查询文章数据
        6、创建分页器
        7、进行分页处理
        8、组织数据传递给模版
        :param request:
        :return:
        """
        # 获取博客分类信息
        categories = ArticleCategory.objects.all()

        # ?cat_id=xxx&page_num=xxx&page_size=xxx
        # 获取用户点击的分类id
        cat_id = request.GET.get('cat_id', 1)
        page_num = request.GET.get('page_num', 1)
        page_size = request.GET.get('page_size', 10)
        # 判断分类id
        try:
            category = ArticleCategory.objects.get(id=cat_id)
        except ArticleCategory.DoesNotExist:
            return HttpResponseNotFound('没有此分类')

        # 分页数据
        articles = Article.objects.filter(
            category=category
        )
        #
        # 创建分页器：每页N条记录
        paginator = Paginator(articles, page_size)
        # 获取每页文章数据
        try:
            page_articles = paginator.page(page_num)
        except EmptyPage:
            # 如果没有分页数据，默认给用户404
            return HttpResponseNotFound('empty page')
        # 获取列表页总页数
        total_page = paginator.num_pages

        context = {
            'categories': categories,
            'category': category,
            'articles': page_articles,
            'page_size': page_size,
            'total_page': total_page,
            'page_num': page_num,
        }
        # return render(request, 'index.html')
        return render(request, 'index.html', context=context)


"""
insert into tb_article(avatar,tags,title,sumary,content,total_views,comments_count,created,updated,author_id, category_id)
select avatar,tags,title,sumary,content,total_views,comments_count,created,updated,author_id, category_id from tb_article;
"""


class DetailView(View):

    """
    1、接收文章id信息
    2、根据文章id进行文章数据的查询
    3、查询分类数据
    4、获取分页请求参数
    5、根据文章信息查询评论数
    6、创建分页器
    7、进行分页处理
    8、组织模版数据
    """

    def get(self, request):
        # detail/?id=xxx&page_num=xxx&page_size=xxx
        # 1、获取文档id
        id = request.GET.get('id')

        # 2、根据文章id进行文章数据的查询
        try:
            article = Article.objects.get(id=id)
        except Article.DoesNotExist:
            return render(request, '404.html')
        else:
            article.total_views += 1
            article.save()

        # 获取分类信息
        categories = ArticleCategory.objects.all()

        # 获取热点数据，查询浏览量前10的文章数量
        # '-total_views' 表明数据应该按total_views以倒序排列
        hot_articles = Article.objects.order_by('-total_views')[:10]

        # 获取分页请求
        page_num = request.GET.get('page_num', 1)
        page_size = request.GET.get('page_size', 10)

        # 获取当前文章的评论数据
        comments = Comment.objects.filter(
            article=article
        ).order_by('-created')
        # 获取评论总数
        total_count = comments.count()

        # 创建分页器：每页N条记录
        paginator = Paginator(comments, page_size)
        # 获取每页评论数据
        try:
            page_comments = paginator.page(page_num)
        except EmptyPage:
            # 如果page_num不正确，默认给用户404
            return HttpResponseNotFound('empty page')
        # 获取列表页总页数
        total_page = paginator.num_pages

        # 组织模版数据
        context = {
            'categories': categories,
            'category': article.category,
            'article': article,
            'hot_articles': hot_articles,
            'total_count': total_count,
            'comments': page_comments,
            'page_size': page_size,
            'total_page': total_page,
            'page_num': page_num,
        }

        return render(request, 'detail.html', context=context)

    def post(self, request):
        """
        1、现接收用户信息
        2、判断用户是否登录
        3、登录用户可以接收form数据
            3、1 接收评论数据
            3、2 验证文章是否存在
            3、3 保存评论数据
            3、4 修改文章评论数量
        4、未登录用户则跳转到登录页面
        :param request:
        :return:
        """
        # 获取用户信息
        user = request.user

        # 判断用户是否登录
        if user and user.is_authenticated:
            # 接收数据
            id = request.POST.get('id')
            content = request.POST.get('content')

            # 判断文章id是否存在
            try:
                article = Article.objects.get(id=id)
            except Article.DoesNotExist:
                return HttpResponseNotFound('没有此文章')

            # 保存到数据
            Comment.objects.create(
                content=content,
                article=article,
                user=user
            )
            # 修改文章评论数量
            article.comments_count += 1
            article.save()
            # 拼接跳转路由
            path = reverse('home:detail') + '?id={}'.format(article.id)
            return redirect(path)
        else:
            # 没有登录则跳转到登录页面
            return redirect(reverse('users:login'))

"""
insert into tb_comment(content,created,article_id,user_id)
select content,created,article_id,user_id from tb_comment;
"""