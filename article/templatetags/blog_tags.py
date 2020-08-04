# 创建了新的tags标签文件后必须重启服务器

from django import template
from ..models import ArticlePost, ArticleColumn,FriendLink
from django.db.models.aggregates import Count
from taggit.models import Tag

register = template.Library()



@register.simple_tag
def get_tag_list():
    '''返回标签列表'''
    return Tag.objects.annotate(total_num=Count('tags')).filter(total_num__gt=0)


@register.simple_tag
def get_category_list():
    '''返回分类列表'''
    return ArticleColumn.objects.annotate(total_num=Count('article')).filter(total_num__gt=0)

@register.simple_tag
def get_friends():
    '''获取活跃的友情链接'''
    return FriendLink.objects.filter(is_show=True, is_active=True)




