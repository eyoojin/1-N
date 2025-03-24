# 1:N

- 댓글은 게시물에 속해있음
- DB에서는 하나의 셀에 하나의 데이터만 저장함
- 데이터베이스 정규화(목적: 데이터를 쪼개고 중복을 피함)
- 게시글과 댓글을 분리

## 0. .gitignore 설정

- 가상환경 생성/ 활성화
- 장고 설치
- .gitignore

## 1. project, app 생성 및 등록
```shell
django-admin startproject board .
django-admin startapp articles
```
```python
# settings.py
INSTALLED_APPS = ['articles']
```

## 2. 공통 html 구조 작성
- ../templates.'base.html'
```python
# settings.py
TEMPLATES = [{'DIRS': [BASE_DIR / 'templates']}]
```
```html
<!-- base.html -->
{% block body %}
{% endblock %}
```

## 3. modeling, migration
- modeling
```python
# models.py
class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```
- migration
```shell
python manage.py makemigrations
python manage.py migrate
```

## 4. Create
- urls 설정
```python
# board/'urls.py'
from django.urls import include

urlpatterns = [path('articles/', include('articles.urls')),]
```
```python
# articles/'urls.py'
from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [path('create/', views.create, name='create')]
```
- ModelFomr(ArticleForm) 생성
```python
# articles/'forms.py'
from django.forms import ModelForm
from .models import Article

class ArticleForm(ModelForm):
    class Meta():
        model = Article
        fields = '__all__'
```
- GET 요청 Create
```python
# views.py
from .forms import ArticleForm

def create(request):
    if request.method == 'POST':
        pass
    else: # GET
        form = ArticleForm()
    
    context = {
        'form': form,
    }

    return render(request, 'create.html', context)
```
```html
<!-- articles/templates/'create.html' -->
{% extends 'base.html' %}

{% block body %}
    <form action="" method="POST">
        {% csrf_token %}
        <!-- 장고가 보증하는 -->
        {{form}}
        <input type="submit">
    </form>
{% endblock %}
```
- POST 요청 Create
```python
from django.shortcuts import redirect

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
```

## 5. Read
- Read all
```python
# urls.py
path('', views.index, name='index')
```
```python
# views.py
from .models import Article

def index(request):
    articles = Article.objects.all()

    context = {
        'articles': articles,
    }

    return render(request, 'index.html', context)
```
```html
<!-- index.html -->
{% extends 'base.html' %}

{% block body %}
    {% for article in articles %}
        <h3>{{article.title}}</h3>
        <hr>
    {% endfor %}
{% endblock %}
```

- Read 1
```html
<!-- index.html -->
<a href="{% url 'articles:detail' article.id %}">detail</a>
```
```python
# urls.py
path('<int:id>/', views.detail, name='detail')
```
```python
# views.py
def detail(detail, id):
    article = Article.objects.get(id=id)

    context = {
        'article': article,
    }

    return render(request, 'detail.html', context)
```
```html
<!-- detail.html -->
{% extends 'base.html' %}

{% block body %}
    <h3>{{article.title}}</h3>
    <p>{{article.content}}</p>
    <p>{{article.created_at}}</p>
    <p>{{article.updated_at}}</p>
{% endblock %}
```

## 6. Update
```html
<!-- detail.html -->
<a href="{% url 'articles:update' article.id %}">update</a>
```
```python
# urls.py
path('<int:id>/update/', views.update, name='update')
```
- 기존 정보 출력
```python
# views.py
def update(request, id):
    if request.method == 'POST':
        pass
    else: 
        article = Article.objects.get(id=id) # 이전에 있던 정보
        form = ArticleForm(instance=article)
    
    context = {
        'form': form,
    }

    return render(request, 'update.html', context)
```
```html
<!-- update.html -->
{% extends 'base.html' %}

{% block body %}
    <form action="" method="POST">
        {% csrf_token %}
        {{form}}
        <input type="submit">
    </form>
{% endblock %}
```
- 새로운 정보 저장
```python
# views.py
def update(request, id):
    article = Article.objects.get(id=id) # 이전에 있던 정보
    # 중복 코드 위로 빼기

    if request.method == 'POST':
        # article = Article.objects.get(id=id)
        form = ArticleForm(request.POST, instance=article)
        # (새로운 정보, 기존 정보)
        if form.is_valid():
            form.save()
            # return redirect('articles:index')
            return redirect('articles:detail', id=id)

    else: 
        # article = Article.objects.get(id=id)
        form = ArticleForm(instance=article)
    
    context = {
        'form': form,
    }

    return render(request, 'update.html', context)
```

## 7. Delete
```html
<!-- detail.html -->
<a href="{% url 'articles:delete' article.id %}">delete</a>
```
```python
# urls.py
path('<int:id>/delete/', views.delete, name='delete'),
```
```python
# views.py
def delete(request, id):
    article = Article.objects.get(id=id)
    article.delete()

    return redirect('articles:index')
```

# 댓글 기능 구현

## 8. Comment modeling, migration
- Comment modeling
```python
# model.py
class Comment(models.Model):
    content = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE) # 1:N relationship
    # on_delete: 게시글이 지워졌을 때, CASCADE: 댓글을 전부 지움
```
- migration
```shell
python manage.py makemigrations
python manage.py migrate
```

## 9. Comment Create
- GET 요청
```python
# forms.py
from .models import Comment

class CommentForm(ModelForm):
    class Meta():
        model = Comment
        fields = '__all__'
```
```python
# views.py
from .forms import CommentForm

# def detail(request, id):
#     article = Article.objects.get(id=id)
    form = CommentForm()

#     context = {
#         'article': article,
        'form': form,
#     }

#     return render(request, 'detail.html', context)
```
```html
<!-- detail.html -->
<hr>
{{form}}
```
```python
# forms.py
class CommentForm(ModelForm):
    class Meta():
        model = Comment
        # fields = '__all__'

        # 둘 중에 하나 선택
        fields = ('content', ) # 추가할 필드 목록
        exclude = ('article', ) # 제외할 필드 목록
```
```html
<!-- detail.html -->
<form action="{% url 'articles:comment_create' article.id %}" method="POST">
    {% csrf_token %}
    {{form}}
    <input type="submit">
</form>
```
- POST 요청
```python
# urls.py
path('<int:article_id>/comments/create/', views.comment_create, name='comment_create')
```
```python
# views.py
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
```

## 10. Comment Read
```python
# models.py
class Article(models.Model):
    # comment_set => article을 이용해 comment에 접근

class Comment(models.Model):
    # article_id => comment를 이용해 article에 접근
    # DB에는 article_id 저장/ article 객체를 저장할 필요 없기 때문에
```
```python
# views.py
def detail(request, id):
    comments = article.comment_set.all() # Comment Read

    context = {
        'comments': comments, # Comment Read
        }
```
```html
<!-- detail.html -->

<!-- for comment in article.comment_set.all -->
<!-- 게시물정보.하위항목 정보.모두 가져오기 -->
{% for comment in comments %}
    <li>{{comment.content}}</li>
{% endfor %}
```