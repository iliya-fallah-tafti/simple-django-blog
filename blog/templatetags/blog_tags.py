from django import template
from blog.models import *
from django.utils.timezone import now

register = template.Library()


@register.inclusion_tag('blog/blog-popular-post.html')
def popular_posts(arg):
    posts = Post.objects.filter(status=1).order_by('-published_date')[:arg]
    return {'posts': posts}


@register.inclusion_tag('blog/blog-post-category.html')
def postcategories():
    posts = Post.objects.filter(status=1)
    categories = Category.objects.all()
    cat_dict = {}
    for name in categories:
        cat_dict[name] = posts.filter(category=name).count()
    return {'categories': cat_dict}

register = template.Library()


@register.simple_tag
def latest_posts():
    # ابتدا پست‌های اسپانسر شده را می‌آوریم
    sponsored_posts = Post.objects.filter(
        status=1,
        Sponsored=True,
        publish_date__lte=now()
    ).order_by('-publish_date')[:6]

    # اگر پست‌های اسپانسر شده کمتر از 6 تا بودند، با پست‌های معمولی تکمیل می‌کنیم
    remaining = 6 - sponsored_posts.count()
    if remaining > 0:
        normal_posts = Post.objects.filter(
            status=1,
            Sponsored=False,  # فقط پست‌های غیر اسپانسر
            publish_date__lte=now()
        ).order_by('-publish_date')[:remaining]
        posts = list(sponsored_posts) + list(normal_posts)
    else:
        posts = sponsored_posts

    return posts
