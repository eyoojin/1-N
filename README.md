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

## 2. 공통 html
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

## 3.
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