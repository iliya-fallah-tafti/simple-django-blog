from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from taggit.models import Tag

from blog.models import *


# Register your models here.

# Admin panel customization https://docs.djangoproject.com/en/5.1/ref/contrib/admin/
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    date_hierarchy = 'publish_date'
    empty_value_display = '-empty-'
    list_display = ('author', 'title', 'status', 'login_require', 'publish_date', 'content_view')
    list_filter = ('status', 'author')
    ordering = ('publish_date',)
    search_fields = ('title', 'content')
    summernote_fields = 'content'
    # fields = ('title', 'content', 'publish_date')
    # admin.site.register(Post , PostAdmin)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated_date'
    empty_value_display = '-empty-'
    list_display = ('name', 'post', 'approved','created_date')
    list_filter = ('approved', 'post')
    ordering = ('updated_date',)
    search_fields = ['name']