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
