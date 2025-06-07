from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from django.utils.text import slugify


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)



class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.ManyToManyField(Category)
    tags = TaggableManager()
    image = models.ImageField(upload_to="blog/", default="blog/default.jpg")
    content_view = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    login_require = models.BooleanField(default=False)
    Sponsored = models.BooleanField(default=False)
    publish_date = models.DateTimeField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    # class Meta:
    #     ordering = ['-publish_date']
    #     verbose_name_plural = "پست ها"
    #     #verbose_name = "پست"
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:single", kwargs={"pk": self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100, default='No subject')
    message = models.TextField()
    approved = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
