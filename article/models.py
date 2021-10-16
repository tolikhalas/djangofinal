import datetime
from django.db import models
from django.template.defaultfilters import slugify
from random import randint
from transliterate.base import TranslitLanguagePack, registry
from transliterate import translit
from django.utils import timezone
from ckeditor.fields import RichTextField
# Create your models here.

class UkranianLanguagePack(TranslitLanguagePack):
    language_code = 'ukr'
    language_name = 'ukranian'
    mapping = (
        u'abvhgdejzyiklmnoprstufABVHGDEJZYIKLMNOPRSTUF',
        u'абвгґдежзиіклмнопрстуфАБВГҐДЕЖЗИІКЛМНОПРСТУФ'
    )

    pre_processor_mapping = {
        u"ye": u"є",
        u"yy": u"й",
        u"yi": u"ї",
        u"kh": u"х",
        u"ts": u"ц",
        u"ch": u"ч",
        u"sh": u"ш",
        u"shch": u"щ",
        u"yu": u"ю",
        u"ya": u"я",

        u"Ye": u"Є",
        u"Yy": u"Й",
        u"Yi": u"Ї",
        u"Kh": u"Х",
        u"Ys": u"Ц",
        u"Ch": u"Ч",
        u"Sh": u"Ш",
        u"Shch": u"Щ",
        u"Yu": u"Ю",
        u"Ya": u"Я",
    }

    reversed_specific_pre_processor_mapping = {
        u"ь": u""
    }

registry.register(UkranianLanguagePack)


class Article(models.Model):

    author = models.ForeignKey("auth.User",on_delete = models.CASCADE,verbose_name = "Автор ")
    title = models.CharField(max_length = 200,verbose_name = "Заголовок")
    content = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True,verbose_name="Дата створення")
    article_image = models.FileField(blank = True,null = True,verbose_name="Зображення")
    slug = models.SlugField(unique=True, max_length=100)

    random_index = randint(1000, 9999)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(translit(self.title, 'ukr', reversed=True) + " " + str(self.random_index))
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
