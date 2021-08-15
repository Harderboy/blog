from django.db import models
from django.utils import timezone


# Create your models here.
class ArticleCategory(models.Model):
    '''
    文章分类
    '''

    # 文章标题
    title = models.CharField(max_length=100, blank=True)
    # 分类的创建时间
    created = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tb_category'  # 修改表名
        verbose_name = '类别管理'  # admin站点显示
        verbose_name_plural = verbose_name


from users.models import User


class Article(models.Model):
    """
    文章
    """
    # 定义文章作者。 author 通过 models.ForeignKey 外键与内建的 User 模型关联在一起
    # 参数 on_delete 用于指定数据删除的方式，当user表中的数据删除之后，文章信息也同步删除，避免两个关联表的数据不一致。
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 文章标题图
    avatar = models.ImageField(upload_to='article/%Y%m%d/', blank=True)
    # 文章栏目的 “一对多” 外键
    # 分类
    category = models.ForeignKey(
        ArticleCategory,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'  # 反向获取文章信息
    )
    # 文章标签
    tags = models.CharField(max_length=20, blank=True)
    # 文章标题
    title = models.CharField(max_length=100, null=False, blank=False)
    # 概要
    # summary
    sumary = models.CharField(max_length=200, null=False, blank=False)
    # 文章正文
    content = models.TextField()
    # 浏览量
    total_views = models.PositiveIntegerField(default=0)
    # 文章点赞数
    comments_count = models.PositiveIntegerField(default=0)
    # 文章创建时间
    # 参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now)
    # 文章更新时间
    # 参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)

    # 内部类 class Meta 用于给 model 定义元数据
    # 修改表明
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        ordering = ('-created',)
        db_table = 'tb_article'
        verbose_name = '文章管理'
        verbose_name_plural = verbose_name

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    # 它最常见的就是在Django管理后台中做为对象的显示值。因此应该总是为 __str__ 返回一个友好易读的字符串
    def __str__(self):
        # 将文章标题返回
        return self.title


class Comment(models.Model):
    # 评论内容
    content = models.TextField()
    # 评论的文章
    article = models.ForeignKey(Article,
                                on_delete=models.SET_NULL,
                                null=True)
    # 发表评论的用户
    # 等效于from users.models import User
    user = models.ForeignKey('users.User',
                             on_delete=models.SET_NULL,
                             null=True)
    # 评论发布时间
    # auto_now：无论添加还是修改，都会添加当前时间
    # auto_now_add：只有在添加时加入时间，修改不添加时间
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.article.title

    class Meta:
        db_table = 'tb_comment'
        verbose_name = '评论管理'
        verbose_name_plural = verbose_name
