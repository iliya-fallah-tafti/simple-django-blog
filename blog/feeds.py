from django.contrib.syndication.views import Feed
from django.urls import reverse
from blog.models import Post
from django.utils.timezone import now


class LatestEntriesFeed(Feed):
    title = "Blog Posts"
    link = "/rss/feed"
    description = "None"

    def items(self):
        return Post.objects.filter(status=1, publish_date__lte=now()).order_by('-publish_date')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content[:150]
