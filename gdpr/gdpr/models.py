from django.urls import reverse
from django.db import models
from hvad.models import TranslatableModel, TranslatedFields


class Chapter(TranslatableModel):

    index = models.SmallIntegerField()

    translations = TranslatedFields(
        label=models.CharField(
            'Label',
            max_length=500
        ),
        name=models.CharField(
            'name',
            max_length=500
        )
    )

    class Meta:
        ordering = ['index']


class Article(TranslatableModel):

    chapter = models.ForeignKey(
        Chapter,
        related_name='articles',
        on_delete=models.CASCADE
    )

    index = models.SmallIntegerField()

    translations = TranslatedFields(
        label=models.CharField(
            'Label',
            max_length=500
        ),
        name=models.CharField(
            'name',
            max_length=500
        ),
        slug=models.SlugField(
            'slug',
            max_length=500,
            blank=True,
            null=True
        )
    )

    def get_absolute_url(self):
        return reverse('article', kwargs={
            'id': self.index
        })

    def get_available_languages_code(self):
        return Article.objects.language('all').filter(
            index=self.index
        ).values_list(
            'language_code',
            flat=True
        )

    class Meta:
        ordering = ['chapter__index', 'index']


class Section(TranslatableModel):

    article = models.ForeignKey(
        Article,
        related_name='sections',
        on_delete=models.CASCADE
    )
    index = models.SmallIntegerField()
    parent_index = models.SmallIntegerField(
        null=True,
        blank=True
    )

    translations = TranslatedFields(
        label=models.CharField(
            'Label',
            max_length=500,
            null=True,
            blank=True
        ),
        content=models.TextField(
            'content'
        )
    )

    class Meta:
        ordering = ['index']


class Recital(TranslatableModel):

    index = models.SmallIntegerField()
    translations = TranslatedFields(
        text=models.TextField(
            'text'
        )
    )

    articles = models.ManyToManyField(
        Article,
        related_name='recitals',
    )

    class Meta:
        ordering = ['index']


class Definition(models.Model):
    language_code = models.CharField(
        max_length=2
    )

    term = models.CharField(
        max_length=550
    )
    definition = models.ForeignKey(
        Section,
        on_delete=models.CASCADE
    )
