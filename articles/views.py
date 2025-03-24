from django.shortcuts import render, redirect
from .forms import ArticleForm
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

    context = {
        'article': article,
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