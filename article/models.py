import datetime
from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
# Create your models here.

class Article(models.Model):

    author = models.ForeignKey("auth.User",on_delete = models.CASCADE,verbose_name = "Автор ")
    title = models.CharField(max_length = 200,verbose_name = "Заголовок")
    content = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True,verbose_name="Дата створення")
    article_image = models.FileField(blank = True,null = True,verbose_name="Зображення")
    slug = models.SlugField(unique=True, max_length=100)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Article, self).save(*args, **kwargs)

    def published_recently(self):
        return self.created_date >= (timezone.now() - datetime.timedelta(days = 7))

    class Meta:
        ordering = ['-created_date']
        verbose_name = 'Стаття'
        verbose_name_plural = 'Статті'

class Comment(models.Model):

    article = models.ForeignKey(Article,on_delete = models.CASCADE,verbose_name = "Стаття",related_name="comments")
    comment_author = models.CharField(max_length = 50,verbose_name = "Автор коментару")
    comment_content = models.CharField(max_length = 200,verbose_name = "Текст коментару")
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_content

    class Meta:
        ordering = ['-comment_date']
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'
