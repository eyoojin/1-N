from django.shortcuts import render, redirect
from .forms import ArticleForm, CommentForm
from .models import Article

# Create your views here.
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST) # 사용자의 정보를 담은
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else: # GET
        form = ArticleForm() # 비어있는
    
    context = {
        'form': form,
    }

    return render(request, 'create.html', context)

def index(request):
    articles = Article.objects.all()

    context = {
        'articles': articles,
    }

    return render(request, 'index.html', context)

def detail(request, id):
    article = Article.objects.get(id=id)
    comments = article.comment_set.all() # Comment Read
    form = CommentForm() # Comment

    context = {
        'article': article,
        'form': form, # Comment
        'comments': comments, # Comment Read
    }

    return render(request, 'detail.html', context)

def update(request, id):
    article = Article.objects.get(id=id) # 이전에 있던 정보

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        # (새로운 정보, 기존 정보)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', id=id)

    else: 
        form = ArticleForm(instance=article)
    
    context = {
        'form': form,
    }

    return render(request, 'update.html', context)

def delete(request, id):
    article = Article.objects.get(id=id)
    article.delete()

    return redirect('articles:index')

def comment_create(request, article_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            # commit: 데이터베이스에 완전히 저장 -> False: 임시 저장
            # comment의 article_id 값이 비어있으므로 먼저 찾아야 함
            article = Article.objects.get(id=article_id)
            comment.article = article
            comment.save()

            return redirect('articles:detail', id=article_id)

    else:
        return redirect('articles:index')