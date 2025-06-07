from django import template
from blog.models import *
from django.utils.timezone import now

register = template.Library()

@register.simple_tag
def latest_posts():
    posts = posts = Post.objects.filter(status=1, publish_date__lte=now()).order_by('-publish_date')[:6]
    return posts