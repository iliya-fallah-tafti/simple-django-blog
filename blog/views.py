from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.timezone import now
from blog.models import Post, Comment
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from blog.forms import CommentForm
from django.contrib import messages


def home(request):
    return render(request, 'main/index.html')


from django.db.models import Count, Q
from django.utils.timezone import now
from blog.models import Post, Category

def blog_views(request, cat_name=None, author_username=None, tag_name=None):
    posts = Post.objects.filter(status=1, publish_date__lte=now()).order_by('-publish_date')

    if cat_name:
        posts = posts.filter(category__slug=cat_name)
    if author_username:
        posts = posts.filter(author__username=author_username)
    if tag_name:
        posts = posts.filter(tags__name=tag_name)

    posts = Paginator(posts, 2)
    try:
        page_number = request.GET.get('page')
        posts = posts.get_page(page_number)
    except PageNotAnInteger:
        posts = posts.get_page(1)
    except EmptyPage:
        posts = posts.get_page(1)

    # ✅ اضافه کردن دسته‌بندی‌ها با تعداد پست‌ها
    categories = Category.objects.annotate(
        post_count=Count('post', filter=Q(post__status=True, post__publish_date__lte=now()))
    )

    context = {
        'posts': posts,
        'categories': categories,
    }
    return render(request, 'blog/blog-home.html', context)



def single(request, pk):
    post = get_object_or_404(Post, pk=pk, publish_date__lte=now(), status=1)

    # Handle comments
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post  # اتصال کامنت به پست جاری
            comment.save()
            messages.add_message(request, messages.SUCCESS, "Your comment has been sent.")
        else:
            messages.add_message(request, messages.ERROR, "Your comment was not sent.")

    # Get related posts
    previous_post = Post.objects.filter(publish_date__lt=post.publish_date, status=1).order_by('-publish_date').first()
    next_post = Post.objects.filter(publish_date__gt=post.publish_date, publish_date__lte=now(), status=1).order_by(
        'publish_date').first()

    # Get approved comments
    comments = Comment.objects.filter(post=post, approved=True)
    form = CommentForm()

    # Prepare context
    context = {
        'post': post,
        'previous_post': previous_post,
        'next_post': next_post,
        'comments': comments,
        'form': form,
    }

    # Increase view count
    post.content_view += 1
    post.save()

    return render(request, 'blog/blog-single.html', context)


def blog_search(request):
    posts = Post.objects.filter(status=1, publish_date__lte=now()).order_by('-publish_date')
    if request.method == 'GET':
        posts = posts.filter(content__contains=request.GET['s'])
    context = {'posts': posts}
    return render(request, 'blog/blog-home.html', context)
