from django.contrib.sitemaps import Sitemap
from blog.models import Post
from django.utils.timezone import now


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Post.objects.filter(status=1, publish_date__lte=now()).order_by('-publish_date')

    def lastmod(self, obj):
        return obj.publish_date