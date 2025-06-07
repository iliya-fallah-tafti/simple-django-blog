from django.urls import path
from blog.views import *
from blog.feeds import LatestEntriesFeed

app_name = 'blog'

urlpatterns = [
    path('', blog_views, name='blog-index'),
    path('post/<int:pk>', single, name='single'),
    # در blog/urls.py
    path('blog/<slug:cat_name>/', blog_views, name='blog'),
    path('tag/<str:tag_name>', blog_views, name='tag'),
    path('author/<str:author_username>', blog_views, name='author'),
    path('search/', blog_search, name='search'),
    path("rss/feed", LatestEntriesFeed()),

]
