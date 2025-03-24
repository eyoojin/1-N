from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # comment_set => article을 이용해 comment에 접근

class Comment(models.Model):
    content = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE) # 1:N relationship
    # on_delete: 게시글이 지워졌을 때, CASCADE: 댓글을 전부 지움
    # article_id => comment를 이용해 article에 접근
    # DB에는 article_id 저장/ article 객체를 저장할 필요 없기 때문에