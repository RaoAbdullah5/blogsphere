from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Article, Comment
from .forms import ArticleForm, CommentForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created!')
            return redirect('login/')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def create_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.aauthor = request.user  # Associate the article with the current user
            article.save()
            return redirect('article_list')  # Redirect to the article list after creation
    else:
        form = ArticleForm()

    return render(request, 'create_article.html', {'form': form})

def article_list(request):
    articles = Article.objects.all()  # Retrieve all articles from the database
    return render(request, 'article_list.html', {'articles': articles})

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    
    # Handle new comment submission
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.user = request.user  # Associate the comment with the current user
            comment.save()
            return redirect('article_detail', article_id=article.id)
    else:
        comment_form = CommentForm()

    # Fetch comments for the article
    comments = article.comments.all()

    return render(request, 'article_detail.html', {
        'article': article,
        'comments': comments,
        'comment_form': comment_form
    })

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if the logged-in user is the one who posted the comment
    if comment.user == request.user:
        comment.delete()
        messages.success(request, 'Your comment has been deleted!')
    else:
        messages.error(request, 'You can only delete your own comments.')

    return redirect('article_detail', article_id=comment.article.id)

def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    # Check if the logged-in user is the author of the article
    if article.aauthor == request.user:
        article.delete()
        messages.success(request, 'Your article has been deleted!')
        return redirect('article_list')
    else:
        messages.error(request, 'You can only delete your own articles.')
        return redirect('article_detail', article_id=article.id)
